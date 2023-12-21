# Released under the MIT License. See LICENSE for details.
#
"""A dummy stub module for the real _batemplatefs.

The real _batemplatefs is a compiled extension module and only available
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

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from typing import Any, Callable


_T = TypeVar('_T')


def _uninferrable() -> Any:
    """Get an "Any" in mypy and "uninferrable" in Pylint."""
    # pylint: disable=undefined-variable
    return _not_a_real_variable  # type: ignore


class Hello:
    """Simple example."""

    def testmethod(self, val: int = 0) -> None:
        """Just testing."""
        return None


def hello_again_world() -> None:
    """Another hello world print."""
    return None
