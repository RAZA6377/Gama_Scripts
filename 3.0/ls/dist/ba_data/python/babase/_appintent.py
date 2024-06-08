# Released under the MIT License. See LICENSE for details.
#
"""Provides AppIntent functionality."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class AppIntent:
    """A high level directive given to the app.

    Category: **App Classes**
    """


class AppIntentDefault(AppIntent):
    """Tells the app to simply run in its default mode."""


class AppIntentExec(AppIntent):
    """Tells the app to exec some Python code."""

    def __init__(self, code: str):
        self.code = code
