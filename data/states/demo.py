"""
The demo of the game, which will be presented in VIS 142.
Game development is intended to resume after class.
"""

import pygame as pg
import pytmx
import random

from .. import prepare, tools

SETTINGS = prepare.SETTINGS["DEMO"]
STORY = prepare.DEMO_STORY
vec = pg.math.Vector2


class Demo(tools._State):
    """This state is the demo gameplay."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "MENU"

        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bossBullets = pg.sprite.Group()

        self.map = TiledMap(SETTINGS["MAP_1"])
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'Boss':
                self.boss = Boss(self, tile_object.x, tile_object.y)
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

        self.isDialogue = False
        self.speakerImg = None
        self.speakerText = None
        self.nextText = True
        self.currStory = 0
        self.endGame = False

    def draw(self, surface):
        """Blit all elements to surface."""
        prepare.SCREEN.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            prepare.SCREEN.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(prepare.SCREEN, SETTINGS["DEBUG_COLOR"], self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(prepare.SCREEN, SETTINGS["DEBUG_COLOR"], self.camera.apply_rect(wall.rect), 1)

        if self.isDialogue == True:
            # Display current text
            imgRect = pg.draw.rect(prepare.SCREEN, SETTINGS["TEXT_BOX_COLOR"], SETTINGS["TEXT_IMG_BOX"], 0)
            prepare.SCREEN.blit(self.speakerImg, (imgRect.centerx - self.speakerImg.get_width()/2, imgRect.centery - self.speakerImg.get_height()/2))
            txtRect = pg.draw.rect(prepare.SCREEN, SETTINGS["TEXT_BOX_COLOR"], SETTINGS["TEXT_BOX"], 0)
            for ind, text in enumerate(self.speakerText):
                txtHeight = SETTINGS["TEXT_FONT"].get_height()
                txtSpacing = ( 140 - txtHeight * len(self.speakerText) ) / len(self.speakerText) + txtHeight
                renderTxt = self.render_font(SETTINGS["TEXT_FONT"], text, SETTINGS["TEXT_COLOR"],
                                             (txtRect.centerx, txtRect.y + txtHeight/2 + 10 + ind*txtSpacing) )
                surface.blit(*renderTxt)

        pg.display.flip()

    def update(self, surface, keys, current_time, time_delta):
        """Update variables and draw everything."""
        self.current_time = current_time
        self.time_delta = time_delta

        if self.isDialogue == False:
            self.all_sprites.update()
            self.camera.update(self.player)

        if self.nextText == True:
            self.renderText(*STORY[self.currStory])
            self.isDialogue = True

            # CONTROL MULTIPLE DIALOG HERE
            if self.currStory in [0, 7, 8, 11, 12, 13, 14, 15, 16] or self.currStory in range(23, 44):
                self.nextText = True
            else:
                self.nextText = False

        # bullets hit mobs
        hits = pg.sprite.spritecollide(self.boss, self.bullets, True)
        for hit in hits:
            hit.kill()
            if self.boss.isAwake is False:
                self.boss.isAwake = True
                self.boss.reqTalks = 26
                self.currStory = 2
                self.nextText = True
            elif self.boss.isAngry is False:
                self.boss.isAngry = True
                self.boss.reqTalks = 39
                self.boss.attackSpeed = 1000.0
                self.currStory = 3
                self.nextText = True
            elif self.boss.isKilling is False:
                self.boss.isKilling = True
                self.boss.reqTalks = 52
                self.boss.attackSpeed = 500.0
                self.currStory = 4
                self.nextText = True

        # bossBullets hit player
        damages = pg.sprite.spritecollide(self.player, self.bossBullets, True)
        for damage in damages:
            damage.kill()
            self.player.health -= 1
            if self.player.health == SETTINGS["PLAYER_HP"] - 1:
                self.currStory = 10
                self.nextText = True
            elif self.player.health < 1:
                self.currStory = 5
                self.nextText = True

        self.draw(surface)

    def get_event(self, event):
        """Take in key input."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
            elif event.key == pg.K_SPACE:
                if self.isDialogue == True:
                    # CONTROL DIRECTION OF STORY HERE DEPENDING ON CURRENT VARIABLE
                    if self.currStory == 0:
                        self.currStory = 1
                    elif self.currStory == 5:
                        self.done = True
                    elif self.currStory == 7:
                        self.currStory = 8
                    elif self.currStory == 8:
                        self.currStory = 9
                    elif self.currStory in range(11, 17):
                        self.currStory = random.randint(17, 22)
                    elif self.currStory >= 23:
                        self.currStory += 1 # Straight progression
                        if self.currStory > 42: # End game
                            self.currStory = 43
                            self.endGame = True
                    self.isDialogue = False
            elif event.key == pg.K_t and self.player.canTalk:
                self.player.canTalk = False
                # print("Required talks left: ", self.boss.reqTalks)
                if self.player.pos.distance_to(self.boss.pos) < 300:
                    # PROGRESS THE GAME BY TALKING
                    if self.boss.reqTalks > 0:
                        self.boss.reqTalks -= 1
                        if self.boss.isAwake is False:
                            # Awaken boss by talking
                            self.boss.isAwake = True
                            self.currStory = 7
                            self.nextText = True
                        else:
                            # Boss is still unwilling to talk
                            self.currStory = random.randint(11, 16)
                            self.nextText = True
                    elif self.boss.reqTalks == 0:
                        # Boss is willing to talk
                        self.boss.reqTalks -= 1
                        self.boss.isAngry = False
                        self.boss.isKilling = False
                        self.boss.attackSpeed = 2000.0

                        self.currStory = 23
                        self.nextText = True
                else:
                    self.currStory = 6
                    self.nextText = True
            elif event.key == pg.K_k:
                self.draw_debug = not self.draw_debug
            elif event.key == pg.K_l:
                print("Lowering required talks for the boss to 1.")
                self.boss.reqTalks = 1
            elif event.key == pg.K_RETURN and self.endGame:
                self.done = True


    def draw_grid(self):
        for x in range(0, prepare.SCREEN_WIDTH, SETTINGS["TILE_SIZE"]):
            pg.draw.line(prepare.SCREEN, SETTINGS["GRID_COLOR"], (x, 0), (x, prepare.SCREEN_HEIGHT))
        for y in range(0, prepare.SCREEN_HEIGHT, SETTINGS["TILE_SIZE"]):
            pg.draw.line(prepare.SCREEN, SETTINGS["GRID_COLOR"], (0, y), (prepare.SCREEN_WIDTH, y))

    def cleanup(self):
        """Stop the music when scene is done."""
        self.__init__()
        return tools._State.cleanup(self)

    def renderText(self, img, txt):
        """Show a text box, and pause the gameplay loop"""
        self.isDialogue = True
        self.speakerImg = img
        self.speakerText = txt


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    """Player-controlled character."""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = SETTINGS["PLAYER_IMG"]
        self.rect = self.image.get_rect()
        self.hit_rect = SETTINGS["PLAYER_HIT_RECT"]
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.last_shot = 0
        self.health = SETTINGS["PLAYER_HP"]
        self.canTalk = True
        self.talkTimer = 0.0

    def get_keys(self):
        if self.game.nextText == False:
            self.vel = vec(0, 0)
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel.x = -SETTINGS["PLAYER_SPEED"]
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel.x = SETTINGS["PLAYER_SPEED"]
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel.y = -SETTINGS["PLAYER_SPEED"]
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel.y = SETTINGS["PLAYER_SPEED"]
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
            if keys[pg.K_SPACE]:
                now = pg.time.get_ticks()
                if now - self.last_shot > SETTINGS["PLAYER_FIRERATE"]:
                    self.last_shot = now
                    pos = self.pos
                    mousex, mousey = pg.mouse.get_pos()
                    originX = prepare.SCREEN_WIDTH / 2
                    originY = prepare.SCREEN_HEIGHT / 2

                    dir = vec(mousex+16-originX, mousey+16-originY).normalize()
                    Bullet(self.game, pos, dir)

    def update(self):
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.time_delta
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.mobs, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.mobs, 'y')
        self.rect.center = self.hit_rect.center

        # Prevent talk spam
        if self.game.current_time - self.talkTimer > 2000.0:
            self.canTalk = True
            self.talkTimer = self.game.current_time


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = SETTINGS["BULLET_IMG"]
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * SETTINGS["BULLET_SPEED"]
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.time_delta
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > SETTINGS["BULLET_LIFETIME"]:
            self.kill()


class BossBullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bossBullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = SETTINGS["BOSS_BULLET_IMG"]
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * SETTINGS["BOSS_BULLET_SPEED"]
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.time_delta
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > SETTINGS["BULLET_LIFETIME"]:
            self.kill()


class Boss(pg.sprite.Sprite):
    """Character will fight this boss"""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = SETTINGS["BOSS_IMG"]
        self.rect = self.image.get_rect()
        self.hit_rect = SETTINGS["BOSS_HIT_RECT"]
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

        self.isAwake = False
        self.isAngry = False
        self.isKilling = False
        self.reqTalks = 13

        self.attackTimer = 0.0
        self.attackSpeed = 1500.0
        self.attackDir = 0.0

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        # Keep shooting bullets while awake
        self.current_time = self.game.current_time
        if self.current_time - self.attackTimer > self.attackSpeed:
            if self.isAwake:
                BossBullet(self.game, self.pos, vec(1, 0).rotate(self.attackDir))
                BossBullet(self.game, self.pos, vec(-1, 0).rotate(self.attackDir))
                BossBullet(self.game, self.pos, vec(0, 1).rotate(self.attackDir))
                BossBullet(self.game, self.pos, vec(0, -1).rotate(self.attackDir))
                if self.isAngry:
                    BossBullet(self.game, self.pos, vec(1, 1).rotate(self.attackDir))
                    BossBullet(self.game, self.pos, vec(-1, 1).rotate(self.attackDir))
                    BossBullet(self.game, self.pos, vec(1, -1).rotate(self.attackDir))
                    BossBullet(self.game, self.pos, vec(-1, -1).rotate(self.attackDir))
                self.attackDir += 30.0
                if self.attackDir >= 360.0:
                    self.attackDir = 0.0
            self.attackTimer = self.current_time


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Camera:
    """Camera is what the screen displays, should be locked onto the character"""
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(prepare.SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(prepare.SCREEN_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - prepare.SCREEN_WIDTH), x)  # right
        y = max(-(self.height - prepare.SCREEN_HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface