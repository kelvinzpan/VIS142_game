"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg

from . import tools

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_MARGIN = 20
ORIGINAL_CAPTION = "Final Battle"


#Initialization
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


#Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
#MOV   = tools.load_all_movies(os.path.join("resources", "movies"))


#Dictionaries of hard-coded variables
SETTINGS = {}

SETTINGS["MAIN_MENU"] = { "BGM": MUSIC["Anitek_-_07_-_Contact"],
                          "TITLE_FONT": pg.font.Font(FONTS["Fixedsys500c"], 50),
                          "TITLE_MARGIN": 120,
                          "TITLE_COLOR": pg.Color("white"),
                          "ITEM_FONT": pg.font.Font(FONTS["Fixedsys500c"], 30),
                          "ITEM_MARGIN": 30,
                          "ITEM_COLOR": pg.Color("white"),
                          "ITEM_SELECT_COLOR": pg.Color("yellow"),
                          "BG_COLOR": pg.Color("black") }

SETTINGS["DEMO"] = { "BG_COLOR": pg.Color("black"),
                     "TILE_SIZE": 32,
                     "GRID_COLOR": (100, 100, 100),
                     "PLAYER_IMG": GFX["ph_green"],
                     "PLAYER_HIT_RECT": pg.Rect(0, 0, 32, 32),
                     "PLAYER_SPEED": 200,
                     "PLAYER_FIRERATE": 1000,
                     "PLAYER_HP": 3,
                     "BOSS_IMG": GFX["ph_red"],
                     "BOSS_SPEED": 100,
                     "BOSS_HIT_RECT": pg.Rect(0, 0, 32, 32),
                     "BULLET_IMG": GFX["bullet"],
                     "BULLET_SPEED": 500,
                     "BULLET_LIFETIME": 1000,
                     "BOSS_BULLET_IMG": GFX["bossBullet"],
                     "MAP_1": os.path.join("resources", "maps", "default.tmx"),
                     "DEBUG_COLOR": pg.Color("cyan"),
                     "TEXT_BOX": pg.Rect(10, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 20, 140),
                     "TEXT_BOX_COLOR": pg.Color("black"),
                     "TEXT_IMG_BOX": pg.Rect(10, SCREEN_HEIGHT - 150 - 52, 42, 42 ),
                     "TEXT_FONT": pg.font.Font(FONTS["Fixedsys500c"], 20),
                     "TEXT_COLOR": pg.Color("white") }

DEMO_STORY = [ (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Use space key to attack, or continue dialogue.",
                 "Use WASD keys for movement.",
                 "Use T to talk."]), #0
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["You feel an ominous presence ahead."]), #1
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["WHO DARES DISTURB MY SLUMBER!"]), #2
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["YOU SHALL BE DECIMATED!"]), #3
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["BURN IN THE FIRES OF HELL!"]), #4
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Hello?"]), #5
            ]