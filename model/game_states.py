import os
from controller import QTE
from model import classes
from view import UIElements as ui
import pygame as pg
import random as rd
import game
import time
import pygame
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from model import item
#import requests
#import openai

# Abstract class that provides methods
# that each GameState method should have
# to ensure functionality
class GameState():

    # When instantiating one of the following
    # GameState classes, you should pass the current
    # Game class.
    def getName(self):
        pass
    def loadBackground(self, surface):
        pass
    def loadUI(self):
        pass
    def handleActions(self):
        pass

    def update(self):
        pass


# Class for handling the main menu
class Menu(GameState):
    
    def __init__(self, g):
        self.game = g
        self.name = "MENU"
        pg.font.init()
        self.MenuFont = pg.font.Font("assets/alagard.ttf",64)
        self.background = ui.adapt_image('assets/menu.png',g.getPalette())
        self.background = pg.transform.scale(self.background,(pg.display.get_surface().get_size()))
        self.button_start = ui.Button("START", 200, 40, (300,300), g.getPalette(), function=self.game.transitionToLoad)
        self.button_settings = ui.Button("SETTINGS", 200, 40, (300,360), g.getPalette(), function=self.game.transitionToSettings)
        self.button_quit = ui.Button("QUIT", 200, 40, (300,420), g.getPalette(), function=self.game.quit)
        pygame.mixer.music.set_volume(0)
        self.game.audio.play_theme_music(-1)
        self.text = "Metal & Magic"
        self.text_surface = self.MenuFont.render(self.text,False,g.getColor("midThree"))
    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.blit(self.background,(0,0))
    
    def loadUI(self,surface):
        self.button_start.draw(surface)
        self.button_settings.draw(surface)
        self.button_quit.draw(surface)
        surface.blit(self.text_surface,(200,100))
        pass

    def handleActions(self, event):
        pass

    def draw(self, screen):
        img = self.font.render(self.name, True, self.color)
        screen.blit(img, (160, 250))

# Class for handling the audio of the game
class Audio(GameState):
    button_sound = None


    def __init__(self):
        pygame.mixer.init()
        self.damage_sound = pygame.mixer.Sound("assets/damage.wav")
        self.button_sound = pygame.mixer.Sound("assets/buttonpress.wav")

        #pygame.mixer.music.load("assets/score.m4a")
        #pygame.mixer.music.load("assets/cerberus.m4a")
        self.theme_music = None

        self.current_room = None

    def play_damage_sound(self):
        self.damage_sound.play()

    def play_button_sound(self):
        self.button_sound.play()

    def play_theme_music(self, loop=-1):
        pygame.mixer.music.load("assets/cerberus.wav")
        pygame.mixer.music.play(loop)

    def stop_theme_music(self):
        pygame.mixer.music.stop()

    def load_sound_effect(self, sound_file, sound_id):
        sound = pygame.mixer.Sound(sound_file)
        self.sounds[sound_file] = sound

    def play_sound_effect(self, sound_id):
        sound = self.sounds.get(sound_id)
        if sound:
            sound.play()

    def load_music(self, music_file, room_id):
        self.music[room_id] = music_file

    def play_music(self, room_id, loop = -1):
        music_file = self.music.get(room_id)
        if music_file:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.0)
            pygame.mixer.music.play(loop)
            self.current_room = room_id
            for i in range(10):
                pygame.mixer.music.set_volume(0.1 * i)
                pygame.time.wait(100)
            pygame.mixer.music.set_volume(0.5)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_room = None

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
            pygame.mixer.music.unpause()

#class VolumeBar(GameState):


 # Class for handling the loading screen
class Loading(GameState):
    
    def __init__(self, g):
        self.name = "MENU"
        self.progress = 0
        self.background = g.getColor('baseOne')
        self.font = pygame.font.Font("assets/alagard.ttf", 40)
        self.game = g
        self.button_start = ui.Button("start", 220, 60, (300, 300),g.getPalette(), function=self.game.transitionToLoad)
        self.image = None
        self.healthbar = ui.HealthBar(0, 100, (220, 150), g.getPalette())

    def getName(self):
        return self.name

    def getBackground(self):
        return self.background
    
    def loadBackground(self, surface):
        surface.fill(self.background)

    def ai_image(self):
        with open('game.config') as fp:
            line = next(fp)
            parts = line.split('=')
            openai.api_key = parts[1].strip()
            response = openai.Image.create(
                prompt="An armored knight running away from enemies in a dark illuminated castle",
                n=1,
                size="512x512"
            )

            image_url = response["data"][0]["url"]
            im = Image.open(BytesIO(requests.get(image_url).content))
            return im

    def pixelate_ai_image(self, im):
        org_size = im.size
        pixelate_lvl = 4
        im = im.resize(
            size=(org_size[0] // pixelate_lvl, org_size[1] // pixelate_lvl),
            resample=0)
        im = im.resize(org_size, resample=0)
        return im

    def display_screen(self, screen, image):
        font = ImageFont.truetype("pixelated.ttf", 36)
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize("Metal and Magic", font=font)

        x = (image.width - text_width) / 2
        y = (image.height - text_height) / 2
        draw.text((x, y), "Metal and Magic", fill=(255, 255, 255), font=font)

        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

        screen.blit(pygame_image, (0, 0))
        pygame.display.update()

    def fetch_remote(self):
        print('fetch remote called!')
        image = self.ai_image()
        pixeled_image = self.pixelate_ai_image(image)
        # pixeled_image = pygame.image.load("C:\\Users\\Andy\\Desktop\\text image example.PNG")
        seconds = int(time.time())
        file = f"image_cache/{seconds}.png"
        #pygame.display.set_mode((pixeled_image.width, pixeled_image.height))
        self.image = pygame.image.fromstring(pixeled_image.tobytes(),
                                             (pixeled_image.width, pixeled_image.height),
                                             "RGB")
        pixeled_image.save(file)

    def load_cache_or_remote(self):
        if self.image is None:
            choices = os.listdir("image_cache")
            if choices:
                file = random.choice(choices)
                pixeled_image = Image.open(f"image_cache/{file}")
                self.image = pygame.image.fromstring(pixeled_image.tobytes(),
                                                     (pixeled_image.width, pixeled_image.height),
                                                     "RGB")
                #pygame.display.set_mode((pixeled_image.width, pixeled_image.height))
                # p = mp.Process(target=self.fetch_remote)
                # p.start()
                return

            self.fetch_remote()

    def get_sprite(self, sheet, width, height, scale):
        sprite_sheet_image = pygame.image.load('knightanimation.png').convert_alpha()
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), (0, 0, width, height))

        return image

    def loadUI(self, surface):
        self.surface = surface
        self.load_cache_or_remote()
        pygame.display.set_caption("Metal and Magic")
        surface.blit(self.image, ( (800 - 512) // 2, (600-512) // 2))
        font = pygame.font.Font("assets/alagard.ttf", 33)


    def handleActions(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #print("HELLO" + str(self.progress))
                if self.progress == 100:
                    if self.game.getEncounters() < 3:
                        self.game.transitionToCombat()
                    else:
                        self.game.transitionToBoss()

    def update(self):
        self.healthbar.update(self.progress, 100)
        self.healthbar.draw(self.surface)

        if self.progress < 100:
            self.progress += 1

class Minigame(GameState):

    def __init__(self, g):
        self.name = "MINIGAME"
        self.game = g
        self.background = g.getColor('baseTwo')
        self.background = ui.adapt_image('assets/minegame.png', g.getPalette())
        self.background = pg.transform.scale(self.background, (pg.display.get_surface().get_size()))
        self.player_img = ui.adapt_image("assets/player.png",g.getPalette())
        self.player_img = pygame.transform.scale(self.player_img, (100, 100))  # scale down the player image

        self.obstacle_img = ui.adapt_image("assets/greenBoss_smol.png", g.getPalette())
        self.obstacle_img = pygame.transform.scale(self.obstacle_img, (75, 75))  # scale down the player image
        self.is_jumping = False
        self.reward = None

        self.player_x = 50
        self.player_y = 300
        self.player_dy = 0
        self.jump_height = 15
        self.obstacle_x = 800
        self.obstacle_y = 312
        self.obstacle_dx = 5
        self.gravity = 0.5
        self.game_start_time = time.time()  # get the start time of the game
        self.game_duration = 20  # set game duration to 20 seconds
        self.finish_line_x = 700  # set the x-coordinate of the finish line
        self.game_over = False  # initialize game over to False
        self.font = pygame.font.Font('assets/alagard.ttf', 32)  # set up font for text display
        self.jump_count = 0
        self.clock = pygame.time.Clock()

    def getName(self):
        return self.name

    def loadBackground(self, surface):
        #(self.background, surface)
        #surface.fill(self.background)
        #surface.blit(self.player_img, (0,0))
        pass

    def loadUI(self, surface):
        surface.fill((255, 255, 255))
        surface.blit(self.background, (0, 0))
        surface.blit(self.player_img, (self.player_x, self.player_y))
        surface.blit(self.obstacle_img, (self.obstacle_x, self.obstacle_y))
        pygame.draw.line(surface, (0, 0, 0), (self.finish_line_x, 0), (self.finish_line_x, 600), 5)  # draw finish line
        time_remaining = int(self.game_duration - (time.time() - self.game_start_time))  # calculate time remaining
        time_text = self.font.render('Time: ' + str(time_remaining), True, (0, 0, 0))
        surface.blit(time_text, (10, 10))  # display time remaining
        #pg.display.flip()
        #surface.blit(self.text_surface, (200, 100))
        pass

    def handleActions(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and not self.is_jumping:
                if not self.game_over:
                    if self.player_y >= 295:
                        self.player_dy = -self.jump_height

            #if event.key == pygame.K_ESCAPE:
            #    self.game.transitionToRoomSelection()
            # Update game state


    def update(self):
        if self.game_over:
            return
        self.player_y += self.player_dy
        self.player_dy += self.gravity
        if self.player_y > 300:
            self.player_y = 300
            self.player_dy = 0

        self.obstacle_x -= self.obstacle_dx
        if self.obstacle_x < -50:
            self.obstacle_x = 800

        # Check for collision

        if (self.obstacle_x < self.player_x + 75
                and self.obstacle_x > self.player_x
                and self.player_y > 225):

            self.game_over = True
            self.game.transitionToRoomSelection()

        # Check for game duration and finish line
        if time.time() - self.game_start_time >= self.game_duration and self.player_x < self.finish_line_x:
            print("you won")
            self.game_over = True
            self.game.transitionToReward()

# Class for handling the combat scenarios
class Combat(GameState):
    def __init__(self, g):
        self.name = "COMBAT"
        self.combatFont = pg.font.Font("assets/alagard.ttf",24)
        self.game = g
        if self.game.numBossEncounters == 0:
            self.background = g.getColor('midThree')
            self.game.player.setWorld(world=0)
            self.game.player.setMaxHP(hp=100)
            self.enemy = classes.Enemy("Wretch",g.difficultyMods.get(g.difficulty), g.getPalette(), hp=150, atk=10, world=0) #init enemy with appropriate difficulty mods
        elif self.game.numBossEncounters == 1:
            self.background = g.getColor('baseThree')
            self.game.player.setWorld(world=1)
            self.game.player.setMaxHP(hp=125)
            self.enemy = classes.Enemy("Radioactive Crab",g.difficultyMods.get(g.difficulty), g.getPalette(), hp=200, atk=13, world=1)
        else:
            self.background = g.getColor('lightOne')
            self.game.player.setWorld(world=2)
            self.game.player.setMaxHP(hp=150)
            self.enemy = classes.Enemy("Floating Monkey",g.difficultyMods.get(g.difficulty) ,g.getPalette(), hp=250, atk=17, world=2)
        self.healthbar = ui.HealthBar(self.game.player.getHP(), self.game.player.getMaxHP(), (50,50),g.getPalette())
        self.enemy_healthbar = ui.HealthBar(self.enemy.getHP(), self.enemy.getMaxHP(), (550,50), g.getPalette())
        self.button_attack = ui.Button("Use " + self.game.player.weapon[1], 220, 60, (300, 450), g.getPalette(), function=self.sliderQTE)
        #item bars
        self.name1 = "Eat " + self.game.player.item1[1] if self.game.player.item1 else "Empty"
        self.item1 = ui.Button(self.name1, 220, 60, (50, 110), g.getPalette(), function=self.useItem1)
        self.name2 = "Eat " + self.game.player.item2[1] if self.game.player.item2 else "Empty"
        self.item2 = ui.Button(self.name2, 220, 60, (280, 110), g.getPalette(), function=self.useItem2)
    
    def getName(self):
        return self.name

    def loadBackground(self, surface):
        surface.fill(self.background)

    def loadUI(self,surface):
        self.healthbar.update(self.game.player.getHP(), self.game.player.getMaxHP())
        self.healthbar.draw(surface)
        self.enemy_healthbar.update(self.enemy.getHP(), self.enemy.getMaxHP())
        self.enemy_healthbar.draw(surface)
        self.button_attack.draw(surface)
        self.game.player.drawPlayer(surface, 100, 300)
        self.enemy.drawEnemy(surface, 600, 300)
        self.game.player_turn = True
        self.game.player_attack = 0
        self.enemy_attack = 0
        self.item1.draw(surface)
        self.item2.draw(surface)

    def useItem1(self):
        # if item is empty chicking does nothing
        if self.name1 != "Empty":
            if self.game.player.item1[0] == "Consumable":
                # add hp back to player according to item, then make item disappear
                self.game.player.heal(self.game.player.item1[2])
            #elif self.game.player.item1[0] == "Defense":
            self.name1 = "Empty"
            self.game.player.removeItem(1)
            self.item1 = ui.Button(self.name1, 220, 60, (50, 110), self.game.getPalette(), function=self.useItem1)

    def useItem2(self):
        # if item is empty chicking does nothing
        if self.name2 != "Empty":
            if self.game.player.item2[0] == "Consumable":
                # add hp back to player according to item, then make item disappear
                self.game.player.heal(self.game.player.item2[2])
            #elif self.game.player.item1[0] == "Defense":
            self.name2 = "Empty"
            self.game.player.removeItem(2)
            self.item2 = ui.Button(self.name2, 220, 60, (280, 110), self.game.getPalette(), function=self.useItem2)

    # when a player presses the attack button:
    #   - corresponding QTE event will play for attack (will implement other attacks/QTEs later)
    #   - hp is decreased based on damage (damage is set to a fixed amount for now)
    #   - increase number of combat encounters
    #   - after enemy dies:
    #     - (will be implementing a pick up item screen later)
    #     - go to room selection screen
    def sliderQTE(self):
        numHits = QTE.handleTimeSliderQTE(3, self.game.getPalette())
        total_damage = self.game.player.generateDamage()*numHits
        self.enemy.takeDamage(total_damage)
        # GAME STAT
        self.game.stats.set_damage_delt(total_damage)
        enemy_dmg = self.enemy.generateDamage()
        self.game.player.takeDamage(enemy_dmg)
        # GAME STAT
        self.game.stats.set_damage_taken(enemy_dmg)
        if (self.game.player.getHP() <= 0):
            # GAME STAT
            self.game.stats.set_battles_lost()
            self.game.transitionToDefeat()
        elif (self.enemy.getHP() <= 0):
            # GAME STAT
            self.game.stats.set_battles_won()
            self.game.increaseEncounters()
            self.game.transitionToReward()

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pass
                #print("combat")
                #self.game.transitionToLoad()

# Class for handling boss battle
class Boss(Combat, GameState):
    
    def __init__(self, g):
        Combat.__init__(self, g)
        self.name = "BOSS"
        self.game = g
        if self.game.numBossEncounters == 0:
            self.background = g.getColor('midThree')
            self.game.player.setWorld(world=0)
            self.game.player.setMaxHP(hp=100)
            self.enemy = classes.Enemy("Skeleton Boss",g.difficultyMods.get(g.difficulty), g.getPalette(), hp=200, atk=15, world=0)
        elif self.game.numBossEncounters == 1:
            self.background = g.getColor('baseThree')
            self.game.player.setWorld(world=1)
            self.game.player.setMaxHP(hp=125)
            self.enemy = classes.Enemy("Wasteland Boss",g.difficultyMods.get(g.difficulty), g.getPalette(), hp=250, atk=20, world=1)
        else:
            self.background = g.getColor('lightOne')
            self.game.player.setWorld(world=2)
            self.game.player.setMaxHP(hp=150)
            self.enemy = classes.Enemy("Floating Boss",g.difficultyMods.get(g.difficulty), g.getPalette(), hp=300, atk=25, world=2)
        self.healthbar = ui.HealthBar(self.game.player.getHP(), self.game.player.getMaxHP(), (50,50),g.getPalette())
        self.enemy_healthbar = ui.HealthBar(self.enemy.getHP(), self.enemy.getMaxHP(), (550,50),g.getPalette())
        self.button_attack = ui.Button("Use " + self.game.player.weapon[1], 220, 60, (300, 450), g.getPalette(), function=self.sliderQTE)
        self.name1 = "Eat " + self.game.player.item1[1] if self.game.player.item1 else "Empty"
        self.item1 = ui.Button(self.name1, 220, 60, (50, 110), g.getPalette(), function=self.useItem1)
        self.name2 = "Eat " + self.game.player.item2[1] if self.game.player.item2 else "Empty"
        self.item2 = ui.Button(self.name2, 220, 60, (280, 110), g.getPalette(), function=self.useItem2)

        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, g.getColor('midThree'))

    def loadBackground(self, surface):
        surface.fill(self.background)
        surface.blit(self.text_surface, (370, 50))

    def loadUI(self,surface):
        self.healthbar.update(self.game.player.getHP(), self.game.player.getMaxHP())
        self.healthbar.draw(surface)
        self.enemy_healthbar.update(self.enemy.getHP(), self.enemy.getMaxHP())
        self.enemy_healthbar.draw(surface)
        self.button_attack.draw(surface)
        self.game.player.drawPlayer(surface, 100, 300)
        self.enemy.drawBoss(surface, 600, 300)
        self.game.player_turn = True
        self.game.player_attack = 0
        self.enemy_attack = 0
        self.item1.draw(surface)
        self.item2.draw(surface)

    def useItem1(self):
        # if item is empty chicking does nothing
        if self.name1 != "Empty":
            if self.game.player.item1[0] == "Consumable":
                # add hp back to player according to item, then make item disappear
                self.game.player.heal(self.game.player.item1[2])
            #elif self.game.player.item1[0] == "Defense":
            self.name1 = "Empty"
            self.game.player.removeItem(1)
            self.item1 = ui.Button(self.name1, 220, 60, (50, 110), self.game.getPalette(), function=self.useItem1)

    def useItem2(self):
        # if item is empty chicking does nothing
        if self.name2 != "Empty":
            if self.game.player.item2[0] == "Consumable":
                # add hp back to player according to item, then make item disappear
                self.game.player.heal(self.game.player.item2[2])
            #elif self.game.player.item1[0] == "Defense":
            self.name2 = "Empty"
            self.game.player.removeItem(2)
            self.item2 = ui.Button(self.name2, 220, 60, (280, 110), self.game.getPalette(), function=self.useItem2)


    def sliderQTE(self):
        numHits = QTE.handleTimeSliderQTE(3,self.game.getPalette())
        total_damage = self.game.player.generateDamage()*numHits
        self.enemy.takeDamage(total_damage)
        # GAME STAT
        self.game.stats.set_damage_delt(total_damage)
        enemy_dmg = self.enemy.generateDamage()
        self.game.player.takeDamage(enemy_dmg)
        # GAME STAT
        self.game.stats.set_damage_taken(enemy_dmg)
        if (self.game.player.getHP() <= 0):
            # GAME STAT
            self.game.stats.set_battles_lost()
            self.game.transitionToDefeat()
        elif (self.enemy.getHP() <= 0):
            # GAME STAT
            self.game.stats.set_bosses_defeated()
            self.game.stats.set_battles_won()
            self.game.resetEncounters()
            self.game.increaseBossEncounters()
            self.game.player.heal( round(10*(self.game.numBossEncounters+1)*self.game.difficultyMods.get(self.game.difficulty)) )
            if self.game.numBossEncounters == 3:
                self.game.transitionToVictory()
            else:
                x = random.randint(0, 10)
                if x <= 5:
                    self.game.transitionToMinigame()
                else:
                    self.game.transitionToReward()


# Class for handling the shop features
class Shop(GameState):
    
    def __init__(self, g):
        self.name = "Welcome to the shop!"
        self.background = g.getColor('baseThree')
        self.game = g
        self.button_enter = ui.Button("Enter shop", 220, 60, (300,250), g.getPalette(), function=self.enterShop)
        self.button_leave = ui.Button("Leave shop", 220, 60, (300,400), g.getPalette(), function=self.leaveShop)

        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, g.getColor('midThree'))

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        surface.blit(self.text_surface, (190, 150))
    
    def loadUI(self,surface):
        self.button_enter.draw(surface)
        self.button_leave.draw(surface)
        pass

    def enterShop(self):
        # skipping shop menu for now, no selling items yet
        self.game.transitionToBuy()

    def leaveShop(self):
        self.game.transitionToLoad()

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pass
                #self.game.transitionToLoad()


# Class for handling the player entering shop
class ShopMenu(GameState):
    
    def __init__(self, g):
        self.name = "What would you like to buy?"
        self.background = g.getColor('baseThree')
        self.game = g
        self.button_buy = ui.Button("Buy items", 220, 60, (60,500), g.getPalette(), function=self.buyItems)
        self.button_sell = ui.Button("Sell items", 220, 60, (300,500), g.getPalette(), function=self.sellItems)
        self.button_back = ui.Button("Leave shop menu", 220, 60, (540,500), g.getPalette(), function=self.closeMenu)

        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, g.getColor['midThree'])

    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        surface.blit(self.text_surface, (75,50))
    
    def loadUI(self,surface):
        self.button_buy.draw(surface)
        self.button_sell.draw(surface)
        self.button_back.draw(surface)
        pass

    def closeMenu(self):
        self.game.transitionToShop()

    def buyItems(self):
        self.game.transitionToBuy()
        pass

    def sellItems(self):
        pass

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pass
                #self.game.transitionToLoad()


# Class for handling difficulty selection
class Settings(GameState):
    
    def __init__(self, g):
        self.name = "Select difficulty"
        self.volName = "Select Volume"
        self.background = g.getColor('baseTwo')
        self.game = g
        self.bg = pygame.image.load("assets/vol_bar.png")
        self.knob = pygame.image.load("assets/vol_knob.png")
        self.load_palettes = False
        self.button_load_palettes = ui.Button("Change Palette", 220, 60, (300,500), g.getPalette(), function=self.set_palette_menu)
        self.button_save_palettes = ui.Button("Save", 220,60, (300,500), g.getPalette(), function=self.save_palette_func)
        self.possibile_palettes = []

        self.button_easy = ui.Button("Easy", 220, 60, (60,400), g.getPalette(), function=self.setEasyDifficulty)
        self.button_normal = ui.Button("Normal", 220, 60, (300,400), g.getPalette(), function=self.setNormalDifficulty)
        self.button_hard = ui.Button("Hard", 220, 60, (540,400), g.getPalette(), function=self.setHardDifficulty)

        self.volumes = [0, 0.25, 0.5, 0.75, 0.99]
        self.knob_state = 0
        self.knob_pos = (265, 50)

        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, g.getColor('midThree'))
        self.text_volume_surface = self.textFont.render(self.volName,False, g.getColor('midThree'))
    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        if self.load_palettes:
            pass
        else: 
            surface.blit(self.text_surface, (215, 300))
            surface.blit(self.text_volume_surface, (265, 50))

    def set_palette_menu(self):
        pos_pals = os.listdir("assets/palettes/")
        but_level = 100
        for pal in pos_pals:
                pal_but = ui.Button(pal, 220, 60, (300,but_level),self.game.getPalette(),function=self.game.load_palette,parameter=pal)
                self.possibile_palettes.append(pal_but)
                but_level += 100
        self.load_palettes = True
    
    def save_palette_func(self):
        self.load_palettes = False
    
    def loadUI(self,surface):
        if self.load_palettes:
            for but in self.possibile_palettes:
                but.draw(surface)
        else:
            self.button_easy.draw(surface)
            self.button_normal.draw(surface)
            self.button_hard.draw(surface)
            self.button_load_palettes.draw(surface)
            surface.blit(self.bg, (265, 50))
            pos = [self.knob_pos[0] + self.knob_state * 60, self.knob_pos[1]]
            surface.blit(self.knob, pos)

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #print("LEFT ")
                if self.knob_state > 0:
                    self.knob_state -= 1

            elif event.key == pygame.K_RIGHT:
                #print("RIGHT")
                if self.knob_state < 4:
                    self.knob_state += 1

           # if self.knob_state == 0:
               # pygame.mixer.music.set_volume(0)
            #else:
               # pygame.mixer.music.set_volume(1 / self.knob_state)
            pygame.mixer.music.set_volume(self.volumes[self.knob_state])
            print(self.volumes[self.knob_state])
            print(pygame.mixer.music.get_volume())

    def setEasyDifficulty(self):
        self.game.setDifficulty(0)
        self.game.transitionToMenu()
        print(self.volumes[self.knob_state])
        print(pygame.mixer.music.get_volume())

    def setNormalDifficulty(self):
        self.game.setDifficulty(1)
        self.game.transitionToMenu()

    def setHardDifficulty(self):
        self.game.setDifficulty(2)
        self.game.transitionToMenu()


# Class for handling room selection
# Allows player to select two different paths
class RoomSelection(GameState):
    
    def __init__(self, g):
        self.name = "Select a path"
        self.background = g.getColor('baseTwo')
        self.game = g
        self.button_room_rd = ui.Button("???", 220, 60, (60,400), g.getPalette(), function=self.randomRoom)
        self.button_combat = ui.Button("Next Battle", 220, 60, (300,400), g.getPalette(), function=self.loadCombat)
        self.button_room_shop = ui.Button("Shop", 220, 60, (540,400), g.getPalette(), function=self.shopRoom)

        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, g.getColor('midThree'))

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        surface.blit(self.text_surface, (230, 200))
    
    def loadUI(self,surface):
        self.button_room_rd.draw(surface)
        self.button_combat.draw(surface)
        self.button_room_shop.draw(surface)
        pass

    def handleActions(self, event):
        pass

    def loadCombat(self):
        self.game.transitionToLoad()

    def randomRoom(self):
        random_value = rd.random()
        if random_value >= 0.75:
            self.game.transitionToTreasure()       
        elif random_value <= 0.05:
            self.game.transitionToBoss()
        else:
            self.game.transitionToLoad()

    def shopRoom(self):
        self.game.transitionToShop()


# Class for handling the victory screen
# Brings the player back to the main menu screen
class Victory(GameState):
    
    def __init__(self, g):
        self.name = "VICTORY!!! Play again?"
        self.background = g.getColor('midTwo')
        self.game = g
        self.button_restart = ui.Button("Restart", 220, 60, (300,460), g.getPalette(), function=self.playAgain)
        
        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, g.getColor('midThree'))

    def displayAchievements(self, surface):
        completed = self.game.stats.achievements.getCompletedAchievements()
        start_pos = 140
        ui.drawText(surface, "Achievements:", (300,start_pos))
        for ach in completed:
            start_pos += 40
            ui.drawText(surface, ach, (300,start_pos))
        
    def playAgain(self):
        # reset game stats, achivements, player items and health, and encounters
        self.game.stats.resetStatsAndAchievements()
        self.game.resetEncounters()
        self.game.resetBossEncounters()
        self.game.player.resetPlayer()
        self.game.transitionToMenu()

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        surface.blit(self.text_surface, (175, 75))
    
    def loadUI(self,surface):
        self.button_restart.draw(surface)
        # Display all completed achievements
        self.displayAchievements(surface)
        pass

    def handleActions(self, event):
        pass

class Defeat(GameState):

    def __init__(self, g):
        self.name = "Defeat"
        self.background = g.getColor('baseOne')
        self.game = g
        self.game.player.setHP()
        self.button_restart = ui.Button("Restart", 220, 60, (300,460), g.getPalette(), function=self.playAgain)

    def displayAchievements(self, surface):
        completed = self.game.stats.achievements.getCompletedAchievements()
        start_pos = 140
        ui.drawText(surface, "Achievements:", (300,start_pos))
        for ach in completed:
            start_pos += 40
            ui.drawText(surface, ach, (300,start_pos))

    def playAgain(self):
        # reset game stats, achivements, player items and health, and encounters
        self.game.stats.resetStatsAndAchievements()
        self.game.resetEncounters()
        self.game.resetBossEncounters()
        self.game.player.resetPlayer()
        self.game.transitionToMenu()

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
    def loadUI(self,surface):
        ui.drawText(surface, "YOU DIED", (350,100))
        self.button_restart.draw(surface)
        # Display all completed achievements
        self.displayAchievements(surface)
        pass

    def handleActions(self, event):
        pass

#Class for handling the item drops
class Reward(GameState):
    
    def __init__(self, g):
        self.name = "ENEMY DIED. Select an item."
        self.background = g.getColor('baseTwo')
        self.game = g
        # initialize items
        difMod = 1+ (5*(self.game.numBossEncounters+1)*g.difficultyMods.get(g.difficulty)/10)
        attackItem = item.Item()
        attackItem.randomAbility("Attack", world=self.game.numBossEncounters)
        attackItem.randomValueWideRange(17*difMod, 23*difMod, self.game.difficulty)
        foodItem = item.Item()
        foodItem.randomAbility("Consumable", world=self.game.numBossEncounters)
        foodItem.randomValueWideRange(10*difMod, 15*difMod, self.game.difficulty)
        self.item1 = attackItem.getItem()
        self.item2 = foodItem.getItem()
        self.button_item1 = ui.Button("Get " + self.item1[1], 220, 60, (60,300), g.getPalette(), function=self.getItem1)
        self.button_item2 = ui.Button("Get " + self.item2[1], 220, 60, (540,300), g.getPalette(), function=self.getItem2)
        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, (0, 0, 0))
    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        #adjust text position here
        surface.blit(self.text_surface, (90, 100))
    
    def loadUI(self,surface):
        self.button_item1.draw(surface)
        self.button_item2.draw(surface)

    def getItem1(self):
        # put item 1 into player inventory
        self.game.player.addItem(0, self.item1)
        self.game.transitionToRoomSelection()

    def getItem2(self):
        # put item 2 into player inventory, choose random slot
        self.game.player.addItem(random.choice([1,2]), self.item2)
        self.game.transitionToRoomSelection()

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()

class Buy(GameState):
    def __init__(self, g):
        self.name = "Choose an Item"
        self.background = g.getColor('baseTwo')
        self.game = g
        # create 3 random items
        difMod = 1+ (5*(self.game.numBossEncounters+1)*g.difficultyMods.get(g.difficulty)/10)
        attackItem = item.Item()
        attackItem.randomAbility("Attack", world=self.game.numBossEncounters)
        attackItem.randomValueWideRange(20*difMod, 27*difMod, self.game.difficulty)
        foodItem1 = item.Item()
        foodItem1.randomAbility("Consumable", world=self.game.numBossEncounters)
        foodItem1.randomValueWideRange(12*difMod, 18*difMod, self.game.difficulty)
        foodItem2 = item.Item()
        foodItem2.randomAbility("Consumable", world=self.game.numBossEncounters)
        foodItem2.randomValueWideRange(12*difMod, 18*difMod, self.game.difficulty)
        self.item1 = attackItem.getItem()
        self.item2 = foodItem1.getItem()
        self.item3 = foodItem2.getItem()
        self.button_item1 = ui.Button(self.item1[1], 220, 60, (60,300), g.getPalette(), function=self.tradeItem1)
        self.button_item2 = ui.Button(self.item2[1], 220, 60, (300,300), g.getPalette(), function=self.tradeItem2)
        self.button_item3 = ui.Button(self.item3[1], 220, 60, (540,300), g.getPalette(), function=self.tradeItem3)

        self.button_cancel = ui.Button("Leave Shop", 220, 60, (300,500), g.getPalette(), function=self.cancel)
        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, g.getColor('midThree'))

    def tradeItem1(self):
        # trade out weapon
        self.game.player.addItem(0, self.item1)
        self.game.transitionToLoad()

    def tradeItem2(self):
        # trade random slot
        self.game.player.addItem(random.choice([1,2]), self.item2)
        self.game.transitionToLoad()

    def tradeItem3(self):
        # trade random slot
        self.game.player.addItem(random.choice([1,2]), self.item3)
        self.game.transitionToLoad()

    def cancel(self):
        self.game.transitionToShop()

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        #adjust text position here
        surface.blit(self.text_surface, (250, 100))
    
    def loadUI(self,surface):
        self.button_item1.draw(surface)
        self.button_item2.draw(surface)
        self.button_item3.draw(surface)
        self.button_cancel.draw(surface)

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()


class Treasure(GameState):

    def __init__(self, g):
        self.name = "You've encountered a chest"
        self.background = "#251d2b"
        self.game = g
        self.button_combat = ui.Button("Leave Chest", 220, 60, (530,320), g.getPalette(), function=self.loadCombat)
        self.button_open_chest = ui.Button("Open Chest", 220, 60, (40,320), g.getPalette(), function=self.treasureRoom)
        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",50)
        self.text_surface = self.textFont.render(self.name, False, "#bce7fc")
        self.image = pg.image.load(f"assets/chest_closed.png")
        self.size = pg.transform.scale(self.image, (120,100))

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
        surface.blit(self.text_surface, (85, 75))
        surface.blit(self.size, (320, 210))
    
    def loadUI(self,surface):
        self.button_combat.draw(surface)
        self.button_open_chest.draw(surface)

    def handleActions(self, event):
        pass

    def loadCombat(self):
        self.game.transitionToLoad()

    def treasureRoom(self):
        self.game.transitionToGetTreasure()


class GetTreasure(GameState):

    def __init__(self, g):
        self.background = "#251d2b"
        self.game = g
        # create a random item
        difMod = 1+ (5*(self.game.numBossEncounters+1)*g.difficultyMods.get(g.difficulty)/10)
        random_value = rd.random()
        if random_value >= 0.7:
            attackItem = item.Item()
            attackItem.randomAbility("Attack", world=self.game.numBossEncounters)
            attackItem.randomValueTopOfRange(22*difMod, 29*difMod, self.game.difficulty)
            self.item = attackItem.getItem()
        else:
            foodItem1 = item.Item()
            foodItem1.randomAbility("Consumable", world=self.game.numBossEncounters)
            foodItem1.randomValueTopOfRange(11*difMod, 16*difMod, self.game.difficulty)
            self.item = foodItem1.getItem()

        self.button_item1 = ui.Button("Take " + self.item[1], 220, 60, (530,400), g.getPalette(), function=self.getItem)
        self.button_leave = ui.Button("Leave " + self.item[1], 220, 60, (40,400), g.getPalette(), function=self.loadCombat)
        self.image = pg.image.load(f"assets/chest_opened.png")
        self.size = pg.transform.scale(self.image, (130,110))
        self.name = "Chest contained " + self.item[1]
        pg.font.init()
        self.textFont = pg.font.Font("assets/alagard.ttf",40)
        self.text_surface = self.textFont.render(self.name, False, "#bce7fc")

    def getItem(self):
        # trade out weapon
        if self.item[0] == "Attack":
            self.game.player.addItem(0, self.item)
            self.game.transitionToLoad()
        else: 
            self.game.player.addItem(random.choice([1,2]), self.item)
            self.game.transitionToLoad()

    def getName(self):
        return self.name

    def loadBackground(self, surface):
        surface.fill(self.background)
        #adjust text position here
        surface.blit(self.text_surface, (85, 75))
        surface.blit(self.size, (320, 210))
    
    def loadUI(self,surface):
        self.button_item1.draw(surface)
        self.button_leave.draw(surface)

    def tradeItem1(self):
        # trade out weapon
        self.game.player.addItem(0, self.item)
        self.game.transitionToLoad()

    def loadCombat(self):
        self.game.transitionToLoad()

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()