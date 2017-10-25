"""
The menu of the game, should be loaded after the splash
"""

import pygame as pg

from .. import prepare, tools


class Menu(tools._State):
    """This State shows the menu until an option is selected"""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "SPLASH"