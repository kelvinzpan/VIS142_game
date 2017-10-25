"""
The demo of the game, which will be presented in VIS 142.
Game development is intended to resume after class.
"""

import pygame as pg

from .. import prepare, tools


class Demo(tools._State):
    """This state is the demo gameplay."""
    def __init__(self):
        tools._State.__init__(self)
