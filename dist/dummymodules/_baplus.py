# Released under the MIT License. See LICENSE for details.
#
"""A dummy stub module for the real _baplus.

The real _baplus is a compiled extension module and only available
in the live engine. This dummy-module allows Pylint/Mypy/etc. to
function reasonably well outside of that environment.

Make sure this file is never included in dirs seen by the engine!

In the future perhaps this can be a stub (.pyi) file, but we will need
to make sure that it works with all our tools (mypy, pylint, pycharm).

NOTE: This file was autogenerated by batools.dummymodule; do not edit by hand.
"""

# I'm sorry Pylint. I know this file saddens you. Be strong.
# pylint: disable=useless-suppression
# pylint: disable=unnecessary-pass
# pylint: disable=use-dict-literal
# pylint: disable=use-list-literal
# pylint: disable=unused-argument
# pylint: disable=missing-docstring
# pylint: disable=too-many-locals
# pylint: disable=redefined-builtin
# pylint: disable=too-many-lines
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=no-value-for-parameter

from __future__ import annotations

from typing import TYPE_CHECKING, override, TypeVar

if TYPE_CHECKING:
    from typing import Any, Callable


_T = TypeVar('_T')


def _uninferrable() -> Any:
    """Get an "Any" in mypy and "uninferrable" in Pylint."""
    # pylint: disable=undefined-variable
    return _not_a_real_variable  # type: ignore


def add_v1_account_transaction(
    transaction: dict, callback: Callable | None = None
) -> None:
    """(internal)"""
    return None


def can_show_ad() -> bool:
    """(internal)"""
    return bool()


def game_service_has_leaderboard(game: str, config: str) -> bool:
    """(internal)

    Given a game and config string, returns whether there is a leaderboard
    for it on the game service.
    """
    return bool()


def get_master_server_address(source: int = -1, version: int = 1) -> str:
    """(internal)

    Return the address of the master server.
    """
    return str()


def get_news_show() -> str:
    """(internal)"""
    return str()


def get_price(item: str) -> str | None:
    """(internal)"""
    return ''


def get_purchased(item: str) -> bool:
    """(internal)"""
    return bool()


def get_purchases_state() -> int:
    """(internal)"""
    return int()


def get_v1_account_display_string(full: bool = True) -> str:
    """(internal)"""
    return str()


def get_v1_account_misc_read_val(name: str, default_value: Any) -> Any:
    """(internal)"""
    return _uninferrable()


def get_v1_account_misc_read_val_2(name: str, default_value: Any) -> Any:
    """(internal)"""
    return _uninferrable()


def get_v1_account_misc_val(name: str, default_value: Any) -> Any:
    """(internal)"""
    return _uninferrable()


def get_v1_account_name() -> str:
    """(internal)"""
    return str()


def get_v1_account_public_login_id() -> str | None:
    """(internal)"""
    return ''


def get_v1_account_state() -> str:
    """(internal)"""
    return str()


def get_v1_account_state_num() -> int:
    """(internal)"""
    return int()


def get_v1_account_ticket_count() -> int:
    """(internal)

    Returns the number of tickets for the current account.
    """
    return int()


def get_v1_account_type() -> str:
    """(internal)"""
    return str()


def get_v2_fleet() -> str:
    """(internal)"""
    return str()


def has_video_ads() -> bool:
    """(internal)"""
    return bool()


def have_incentivized_ad() -> bool:
    """(internal)"""
    return bool()


def have_outstanding_v1_account_transactions() -> bool:
    """(internal)"""
    return bool()


def in_game_purchase(item: str, price: int) -> None:
    """(internal)"""
    return None


def is_blessed() -> bool:
    """(internal)"""
    return bool()


def mark_config_dirty() -> None:
    """(internal)

    Category: General Utility Functions
    """
    return None


def on_app_loading() -> None:
    """(internal)"""
    return None


def power_ranking_query(callback: Callable, season: Any = None) -> None:
    """(internal)"""
    return None


def purchase(item: str) -> None:
    """(internal)"""
    return None


def report_achievement(achievement: str, pass_to_account: bool = True) -> None:
    """(internal)"""
    return None


def reset_achievements() -> None:
    """(internal)"""
    return None


def restore_purchases() -> None:
    """(internal)"""
    return None


def run_v1_account_transactions() -> None:
    """(internal)"""
    return None


def show_ad(
    purpose: str, on_completion_call: Callable[[], None] | None = None
) -> None:
    """(internal)"""
    return None


def show_ad_2(
    purpose: str, on_completion_call: Callable[[bool], None] | None = None
) -> None:
    """(internal)"""
    return None


def show_game_service_ui(
    show: str = 'general',
    game: str | None = None,
    game_version: str | None = None,
) -> None:
    """(internal)"""
    return None


def sign_in_v1(account_type: str) -> None:
    """(internal)

    Category: General Utility Functions
    """
    return None


def sign_out_v1(v2_embedded: bool = False) -> None:
    """(internal)

    Category: General Utility Functions
    """
    return None


def submit_score(
    game: str,
    config: str,
    name: Any,
    score: int | None,
    callback: Callable,
    order: str = 'increasing',
    tournament_id: str | None = None,
    score_type: str = 'points',
    campaign: str | None = None,
    level: str | None = None,
) -> None:
    """(internal)

    Submit a score to the server; callback will be called with the results.
    As a courtesy, please don't send fake scores to the server. I'd prefer
    to devote my time to improving the game instead of trying to make the
    score server more mischief-proof.
    """
    return None


def tournament_query(
    callback: Callable[[dict | None], None], args: dict
) -> None:
    """(internal)"""
    return None
