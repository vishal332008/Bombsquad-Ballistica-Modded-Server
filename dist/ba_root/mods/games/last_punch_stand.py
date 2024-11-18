# ba_meta require api 8

from typing import Sequence
import random
import bascenev1, babase, baclassic, baplus, bauiv1
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.powerupbox import PowerupBoxFactory

class Player(bascenev1.Player['Team']):
	"""Our player type for this game."""

class Team(bascenev1.Team[Player]):
	"""Our team type for this game."""

	def __init__(self) -> None:
		super().__init__()
		self.score = 1

class ChoosingThingHitMessage:
	def __init__(self, hitter:Player) -> None:
		self.hitter = hitter

class ChoosingThingDieMessage:
	def __init__(self, how:bascenev1.DeathType) -> None:
		self.how = how

class ChoosingThing():
	def __init__(self, pos, color) -> None:
		pass

	def recolor(self, color:list[int | float], highlight:list[int, float] = (1,1,1)):
		raise NotImplementedError()

	def is_dead(self):
		raise NotImplementedError()
		
	def _is_dead(self):
		return self.is_dead()
	
	def create_locator(self, node:bascenev1.Node, pos, color):
		loc = bascenev1.newnode(
			'locator',
			attrs={
				'shape': 'circleOutline',
				'position': pos,
				'color': color,
				'opacity': 1,
				'draw_beauty': False,
				'additive': True,
			},
		)
		node.connectattr("position", loc, "position")
		bascenev1.animate_array(loc, "size", 1, keys={0:[0.5,], 1:[2,], 1.5:[0.5]}, loop=True)

		return loc

	dead = property(_is_dead)

class ChoosingSpaz(Spaz, ChoosingThing):
	def __init__(
		self,
		pos:Sequence[float],
		color: Sequence[float] = (1.0, 1.0, 1.0),
		highlight: Sequence[float] = (0.5, 0.5, 0.5),
	):
		super().__init__(color, highlight, "Spaz", None, True, True, False, False)
		self.stand(pos)
		self.loc = self.create_locator(self.node, pos, color)

	def handlemessage(self, msg):
		if isinstance(msg, bascenev1.FreezeMessage):
			return

		if isinstance(msg, bascenev1.PowerupMessage):
			if not(msg.poweruptype == "health"):
				return

		super().handlemessage(msg)

		if isinstance(msg, bascenev1.HitMessage):
			self.handlemessage(bascenev1.PowerupMessage("health"))

			player = msg.get_source_player(Player)
			if self.is_alive():
				self.activity.handlemessage(ChoosingThingHitMessage(player))

		elif isinstance(msg, bascenev1.DieMessage):
			self._dead = True
			self.activity.handlemessage(ChoosingThingDieMessage(msg.how))

			self.loc.delete()

	def stand(self, pos = (0,0,0), angle = 0):
		self.handlemessage(bascenev1.StandMessage(pos,angle))

	def recolor(self, color, highlight = (1,1,1)):
		self.node.color = color
		self.node.highlight = highlight
		self.loc.color = color

	def is_dead(self):
		return self._dead  

class ChoosingBall(bascenev1.Actor, ChoosingThing):
	def __init__(self, pos, color = (0.5,0.5,0.5)) -> None:
		super().__init__()
		shared = SharedObjects.get()

		pos = (pos[0], pos[1] + 2, pos[2])

		# We want the puck to kill powerups; not get stopped by them
		self.puck_material = bascenev1.Material()
		self.puck_material.add_actions(
			conditions=('they_have_material',
						PowerupBoxFactory.get().powerup_material),
			actions=(('modify_part_collision', 'physical', False),
					 ('message', 'their_node', 'at_connect', bascenev1.DieMessage())))
	
		#fontSmall0 jumpsuitColor menuBG operaSingerColor rgbStripes zoeColor
		self.node = bascenev1.newnode('prop',
								delegate=self,
								attrs={
								   'mesh': bascenev1.getmesh('frostyPelvis'),
								   'color_texture':
										bascenev1.gettexture('gameCenterIcon'),
								   'body': 'sphere',
								   'reflection': 'soft',
								   'reflection_scale': [0.2],
								   'shadow_size': 0.5,
								   'is_area_of_interest': True,
								   'position': pos,
								   "materials": [shared.object_material, self.puck_material]
  					   })
		#seince this ball allways jumps a specefic direction when it spawned, we just jump it randomly
		self.node.handlemessage(
						'impulse',
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						0,
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
						random.uniform(-10, 10),
					)

		self.loc = self.create_locator(self.node, pos, color)

		self._died = False

	def handlemessage(self, msg):
		if isinstance(msg, bascenev1.HitMessage):
			player = msg.get_source_player(Player)
			self.activity.handlemessage(ChoosingThingHitMessage(player))

			mag = msg.magnitude
			velocity_mag = msg.velocity_magnitude

			self.node.handlemessage(
						'impulse',
						msg.pos[0],
						msg.pos[1],
						msg.pos[2],
						msg.velocity[0],
						msg.velocity[1],
						msg.velocity[2],
						mag,
						velocity_mag,
						msg.radius,
						1,
						msg.force_direction[0],
						msg.force_direction[1],
						msg.force_direction[2],
					)
			
		elif isinstance(msg, bascenev1.DieMessage):
			if self.node.exists():
				self.node.delete()
			self.loc.delete()

			self._died = True
			self.activity.handlemessage(ChoosingThingDieMessage(msg.how))

		return super().handlemessage(msg)
	
	def exists(self) -> bool:
		return not self.dead
	
	def is_alive(self) -> bool:
		return not self.dead

	def recolor(self, color: list[int | float], highlight: list[int] = (1, 1, 1)):
		self.loc.color = color

	def is_dead(self):
		return self._died

class ChooseBilbord(bascenev1.Actor):
	def __init__(self, player:Player, delay = 0.1) -> None:
		super().__init__()

		icon = player.get_icon()
		self.scale = 100

		self.node = bascenev1.newnode(
			'image',
			delegate=self,
			attrs={
				"position":(60,-125),
				'texture': icon['texture'],
				'tint_texture': icon['tint_texture'],
				'tint_color': icon['tint_color'],
				'tint2_color': icon['tint2_color'],
				'opacity': 1.0,
				'absolute_scale': True,
				'attach': "topLeft"
			},
		)

		self.name_node = bascenev1.newnode(
			'text',
			owner=self.node,
			attrs={
				'position': (60,-185),
				'text': bascenev1.Lstr(value=player.getname()),
				'color': bascenev1.safecolor(player.team.color),
				'h_align': 'center',
				'v_align': 'center',
				'vr_depth': 410,
				'flatness': 1.0,
				'h_attach': 'left',
				'v_attach': 'top',
				'maxwidth':self.scale
			},
		)
		
		bascenev1.animate_array(self.node, "scale", keys={0 + delay:[0,0], 0.05 + delay:[self.scale, self.scale]}, size=1)
		bascenev1.animate(self.name_node, "scale", {0 + delay:0, 0.07 + delay:1})

	def handlemessage(self, msg):
		super().handlemessage(msg)
		if isinstance(msg, bascenev1.DieMessage):
			bascenev1.animate_array(self.node, "scale", keys={0:self.node.scale, 0.05:[0,0]}, size=1)
			bascenev1.animate(self.name_node, "scale", {0:self.name_node.scale, 0.07:0})

			def __delete():
				self.node.delete()
				self.name_node.delete()
				
			bascenev1.timer(0.2, __delete)

# ba_meta export bascenev1.GameActivity
class LastPunchStand(bascenev1.TeamGameActivity[Player, Team]):
	name = "Last Punch Stand"
	description = "Last one punchs the choosing thing wins"
	tips = [
		'keep punching the choosing thing to be last punched player at times up!',
		'you can not frezz the choosing spaz',
		"evry time you punch the choosing thing, you will get one point",
	]

	default_music = bascenev1.MusicType.TO_THE_DEATH

	def get_instance_display_string(self) -> bascenev1.Lstr:
		name = self.name
		if self.settings_raw["Ball Mode"]:
			name += " Ball Mode"

		return name

	def get_instance_description_short(self) -> str | Sequence:
		if self.settings_raw["Ball Mode"]:
			return "Punch the Ball"
		else:
			return "Punch the Spaz"

	available_settings = [
		bascenev1.BoolSetting("Ball Mode", False),
		bascenev1.FloatSetting("min time limit (in seconds)", 50.0, min_value=30.0),
		bascenev1.FloatSetting("max time limit (in seconds)", 160.0, 60),
	]

	def __init__(self, settings: dict):
		super().__init__(settings)
		self._min_timelimit = settings["min time limit (in seconds)"]
		self._max_timelimit = settings["max time limit (in seconds)"]
		self.ball_mod:bool = settings["Ball Mode"]
		if (self._min_timelimit > self._max_timelimit):
			self._max_timelimit = self._min_timelimit

		self._choosing_thing_defcolor = (0.5,0.5,0.5)
		self.choosing_thing:ChoosingThing = None
		self.choosed_player = None
		self.times_uped = False
		self.scoreboard = Scoreboard()

	@classmethod
	def get_supported_maps(cls, sessiontype: type[bascenev1.Session]) -> list[str]:
		assert bascenev1.app.classic is not None
		return bascenev1.app.classic.getmaps('team_flag')

	def times_up(self):
		self.times_uped = True
		self.end_game()

		for player in self.players:
			try:
				if self.choosed_player and player and (player.team.id != self.choosed_player.team.id):
					player.actor._cursed = True
					player.actor.curse_explode()
			except AttributeError:
				pass

	def __get_thing_spawn_point(self):
		if len(self.map.flag_points_default) > 0:
			return self.map.get_flag_position(None)
		elif len(self.map.tnt_points) > 0:
			return self.map.tnt_points[random.randint(0, len(self.map.tnt_points)-1)]
		else:
			return (0, 6, 0)

	def spaw_bot(self):
		"spawns a choosing bot"
		if self.ball_mod:
			self.choosing_thing = ChoosingBall(self.__get_thing_spawn_point())
		else:
			self.choosing_thing = ChoosingSpaz(self.__get_thing_spawn_point())
		self.choose_bilbord = None

	def on_begin(self) -> None:
		super().on_begin()
		time_limit = random.randint(self._min_timelimit, self._max_timelimit)
		self.spaw_bot()
		bascenev1.timer(time_limit, self.times_up)

		self.setup_standard_powerup_drops(False)
  
	def end_game(self) -> None:
		results = bascenev1.GameResults()
		total = 0

		for team in self.teams:
			total = team.score

		for team in self.teams:
			if self.choosed_player and (team.id == self.choosed_player.team.id): team.score += total
			results.set_team_score(team, team.score)

		self.end(results=results)

	def change_choosed_player(self, hitter:Player):
		if hitter == self.choosed_player:
			return
		
		if hitter:
			self.choosing_thing.recolor(hitter.color, hitter.highlight)
			self.choosed_player = hitter
			hitter.team.score += 1
			self.choose_bilbord = ChooseBilbord(hitter)
			self.hide_score_board()
		else:
			self.choosing_thing.recolor(self._choosing_thing_defcolor)
			self.choosed_player = None
			self.choose_bilbord = None
			self.show_score_board()

	def show_score_board(self):
		self.scoreboard = Scoreboard()
		for team in self.teams:
			self.scoreboard.set_team_value(team, team.score)
	
	def hide_score_board(self):
		self.scoreboard = None

	def _watch_dog_(self):
		"checks if choosing spaz exists"
		#choosing spaz wont respawn if death type if generic
		#this becuse we dont want to keep respawn him when he dies because of losing referce
		#but sometimes "choosing spaz" dies naturaly and his death type is generic! so it wont respawn back again
		#thats why we have this function; to check if spaz exits in the case that he didnt respawned
		
		if self.choosing_thing:
			if self.choosing_thing.dead:
				self.spaw_bot()
		else:
			self.spaw_bot()

	def handlemessage(self, msg):
		super().handlemessage(msg)

		if isinstance(msg, ChoosingThingHitMessage):
			hitter = msg.hitter
			if hitter:
				self.change_choosed_player(hitter)

		elif isinstance(msg, ChoosingThingDieMessage):
			if msg.how.value != bascenev1.DeathType.GENERIC.value:
				self.spaw_bot()
				self.change_choosed_player(None)
		
		elif isinstance(msg, bascenev1.PlayerDiedMessage):
			player = msg.getplayer(Player)
			if not (self.has_ended() or self.times_uped):
				self.respawn_player(player, 0)
			
			if self.choosed_player and (player.getname(True) == self.choosed_player.getname(True)):
				self.change_choosed_player(None)

		self._watch_dog_()