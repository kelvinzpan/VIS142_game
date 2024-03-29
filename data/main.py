"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

# WORKS WITH PYTHON 3

from . import prepare, tools
from .states import splash, menu, demo, game


def main():
    """Add states to control here."""
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {"SPLASH" : splash.Splash(),
                  "MENU"   : menu.Menu(),
                  "DEMO"   : demo.Demo(),
                  "GAME"   : game.Game()}
    run_it.setup_states(state_dict, "SPLASH")
    run_it.main()