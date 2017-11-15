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
                     "PLAYER_SPEED": 300,
                     "PLAYER_FIRERATE": 1000,
                     "PLAYER_HP": 3,
                     "BOSS_IMG": GFX["ph_red"],
                     "BOSS_SPEED": 100,
                     "BOSS_HIT_RECT": pg.Rect(0, 0, 32, 32),
                     "BOSS_TALK_RANGE": 500,
                     "BULLET_IMG": GFX["bullet"],
                     "BULLET_SPEED": 450,
                     "BULLET_LIFETIME": 1000,
                     "BOSS_BULLET_IMG": GFX["bossBullet"],
                     "BOSS_BULLET_SPEED": 450,
                     "MAP_1": os.path.join("resources", "maps", "default.tmx"),
                     "DEBUG_COLOR": pg.Color("cyan"),
                     "TEXT_BOX": pg.Rect(10, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 20, 140),
                     "TEXT_BOX_COLOR": pg.Color("black"),
                     "TEXT_IMG_BOX": pg.Rect(10, SCREEN_HEIGHT - 150 - 52, 42, 42 ),
                     "TEXT_FONT": pg.font.Font(FONTS["Fixedsys500c"], 20),
                     "TEXT_COLOR": pg.Color("white") }

DEMO_STORY = [(SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Use space key to attack, or continue dialogue.",
                 "Use WASD keys for movement.",
                 "Use T to talk."]),  #0
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["You feel an ominous presence ahead."]),  #1
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["WHO DARES DISTURB MY SLUMBER!"]),  #2
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["YOU SHALL BE DECIMATED!"]),  #3
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["BURN IN THE FIRES OF HELL!"]),  #4
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["You have lost in your final battle and died.",
                 "Press Space to return to the main menu.",
                 "Thank you for playing, and better luck next time!"]),  #5
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["There's no one nearby to talk to."]),  #6
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Vile demon! I have come to slay you!",
                 "Surrender at once and I will spare your life.",
                 "Or something like that..."]),  #7
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Zzz..."]),  #8
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Hmm?",
                 "You have quite the nerve to awaken me.",
                 "Prepare for your inevitable demise!"]),  #9
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Shit, his attacks are quite powerful.",
                 "I'm not sure how many more I can take.",
                 "I can probably survive one more."]),  #10

                # Random messages for whittling down required talks
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Wait, I think we can talk this one out..."]),  #11
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["I changed my mind! Let's be civil..."]),  #12
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["I only accepted this quest because I needed the gold..."]),  #13
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["The villagers told me you were a murderer..."]),  #14,
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["I'll be exiled if I don't come back with your head..."]),  #15
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Wait a second, you don't look like a demon..."]),  #16

                # Random replies to the above
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Enough words! You shall die!"]),  #17
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["This is how humans always repay their debts. With betrayal!"]),  #18
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Who sent you? Was it the Magister?",
                 "I should have never trusted humans!"]),  #19
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["A demon? I have never unjustly sacrificed human life.",
                 "I shall begin with you!"]),  #20
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Turn back while you still can!"]),  #21
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Capitalizing on my wounded state! Humans are truly vicious!"]),  #22


                # Final dialogue
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["I think there's a misunderstanding here. Let's talk!"]),  # 23
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["...",
                 "...",
                 "Talk, but I am watching you."]),  #24
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["So I was sent here the the Citadel Captain, to kill you.",
                 "I was coerced into accepting this quest, because no one else did.",
                 "The nearby villagers are convinced you've been murdering their folk."]),  # 25
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Preposterous! Humans can go murder each other if they wish.",
                 "I have no desire to uselessly take their lives.",
                 "Now that you understand, begone."]),  #26
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Err, yeah! Except the Citadel Captain will exile me.",
                 "You see, he wants your head.",
                 "And uh, I don't want to kill you. But I need your help"]),  # 27
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Humans, always asking for help when they need it most.",
                 "I cannot do anything for you.",
                 "Now, begone!"]),  #28
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Look, if I get exiled, my family will starve!",
                 "I'm the only one fit to work!",
                 "Please, you have to understand this is quite the misunderstanding."]),  # 29
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Who is this captain of yours?"]),  #30
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Captain Resari of the Thousand Sword Citadel."]),  # 31
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["Captain Resari."]),  #32
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["..."]),  # 33
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["..."]),  #34
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["..."]),  # 35
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["... Do you know of a Magister Nemus Resari?"]),  #36
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Neums Resari? The founder of the Citadel?",
                 "Of COURSE not. He's long dead!",
                 "Wait. Why do you ask?"]),  # 37
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["He's not dead. I would know.",
                 "It looks like I have some unfinished business to take care of.",
                 "Lead me to your Captain Resari."]),  #38
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Can you stop me from being exiled?"]),  # 39
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["... Yes."]),  #40
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["Well, let's get going! Wait.",
                 "What's your name?"]),  # 41
                (SETTINGS["DEMO"]["BOSS_IMG"],
                ["..."]),  #42
                (SETTINGS["DEMO"]["PLAYER_IMG"],
                ["CONGRATULATIONS! You have beat the game!",
                 "As you might have guessed, violence is not always the answer.",
                 "Thank you for playing! Press ENTER to return to the menu."]),  # 43
              ]