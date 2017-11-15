"""
The menu of the game, should be loaded after the splash
"""

import pygame as pg

from .. import prepare, tools

SETTINGS = prepare.SETTINGS["MAIN_MENU"]


class Menu(tools._State):
    """This State shows the menu until an option is selected"""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "SPLASH"
        self.bgm = SETTINGS["BGM"]

        self.titleFont = SETTINGS["TITLE_FONT"]
        self.titleMargin = SETTINGS["TITLE_MARGIN"]
        self.menuTitle = self.render_font(self.titleFont, prepare.ORIGINAL_CAPTION,
                                          SETTINGS["TITLE_COLOR"],
                                          (prepare.SCREEN_RECT.centerx,
                                           prepare.SCREEN_MARGIN + self.titleMargin +
                                           self.titleFont.get_height() / 2))

        self.itemMargin = SETTINGS["ITEM_MARGIN"]
        self.itemList = [
            MenuItem(name="Play", state="DEMO"),
            MenuItem(name="Credits", state="GAME"),
            MenuItem(name="Quit", state="DEMO") ]
        self.currItem = 0

        currHeight = self.menuTitle[1].y + self.titleMargin
        for ind in range(len(self.itemList)):
            item = self.itemList[ind]
            item.itemPosY = currHeight + item.itemFont.get_height() / 2
            currHeight += self.itemMargin + item.itemFont.get_height()

        self.blink = False
        self.timer = 0.0

    def startup(self, current_time, persistent):
        """Load and play the music on scene start."""
        pg.mixer.music.load(self.bgm)
        pg.mixer.music.play(-1)
        return tools._State.startup(self, current_time, persistent)

    def cleanup(self):
        """Stop the music when scene is done."""
        #pg.mixer.music.stop()
        return tools._State.cleanup(self)

    def draw(self, surface):
        """Blit all elements to surface."""
        surface.fill(SETTINGS["BG_COLOR"])
        surface.blit(*self.menuTitle)

        for ind in range(len(self.itemList)):
            item = self.itemList[ind]
            if ind == self.currItem:
                if self.blink:
                    item.Text = self.render_font(
                        item.itemFont, item.itemName, SETTINGS["ITEM_SELECT_COLOR"],
                        (prepare.SCREEN_RECT.centerx, item.itemPosY) )
                    surface.blit(*item.Text)
            else:
                item.Text = self.render_font(
                    item.itemFont, item.itemName, item.itemColor,
                    (prepare.SCREEN_RECT.centerx, item.itemPosY))
                surface.blit(*item.Text)


    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.current_time = current_time

        # Blink timer to flash the current item
        if self.current_time-self.timer > 1000.0/5.0:
            self.blink = not self.blink
            self.timer = self.current_time
        self.draw(surface)

    def get_event(self, event):
        """Go back to splash on escape key."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = "SPLASH"
                self.done = True
            elif event.key == pg.K_s or event.key == pg.K_DOWN:
                self.currItem = (self.currItem + 1) % len(self.itemList)
            elif event.key == pg.K_w or event.key == pg.K_UP:
                self.currItem = self.currItem - 1
                if self.currItem < 0:
                    self.currItem = len(self.itemList) - 1
            elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                if (self.itemList[self.currItem].itemName == "Quit"):
                    self.quit = True
                self.next = self.itemList[self.currItem].itemState
                self.done = True


class MenuItem():
    """Make Menu code more flexible and readable"""
    def __init__(self, name="MenuItem", state="MENU",
                 color=SETTINGS["ITEM_COLOR"],
                 font=SETTINGS["ITEM_FONT"]):
        self.itemName = name
        self.itemState = state
        self.itemColor = color
        self.itemFont = font
        self.itemPosY = None
        self.Text = None