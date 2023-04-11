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

    # When instanciating one of the following
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
        self.background = pg.image.load('assets/menu.png')
        self.background = pg.transform.scale(self.background,(pg.display.get_surface().get_size()))
        self.button_start = ui.Button("START", 200, 40, (300,300), function=self.game.transitionToLoad)
        self.button_settings = ui.Button("SETTINGS", 200, 40, (300,360), function=self.game.transitionToDifficulty)
        self.button_quit = ui.Button("QUIT", 200, 40, (300,420), function=self.game.quit)

        self.text = "Metal & Magic"
        self.text_surface = self.MenuFont.render(self.text,False,"#bce7fc")
    
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

    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = {}
        self.current_room = None

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
            # I was thinking of implementing a loop where the music gradually increases
            # once a new room is accessed instead of the music immediately being thrown
            # at the player
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

# Class for handling the loading screen
class Loading(GameState):
    
    def __init__(self, g):
        self.name = "MENU"
        self.progress = 0
        self.background = "#0c2a31"
        self.color = "#bce7fc"
        self.font = pygame.font.Font("assets/alagard.ttf", 40)
        self.game = g
        self.button_start = ui.Button("start", 220, 60, (300, 300), function=self.game.transitionToLoad)
        self.image = None
        self.healthbar = ui.HealthBar(0, 100, (220, 150))

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
                if self.game.getEncounters() < 3:
                    self.game.transitionToCombat()
                else:
                    self.game.transitionToBoss()

    def update(self):
        self.healthbar.update(self.progress, 100)
        self.healthbar.draw(self.surface)

        if self.progress < 100:
            self.progress += 1


# Class for handling the combat scenarios
class Combat(GameState):
    def __init__(self, g):
        self.name = "COMBAT"
        self.combatFont = pg.font.Font("assets/alagard.ttf",24)
        self.background = "#9a4ccf"
        self.enemy = classes.Enemy("Wretch",g.difficultyMods.get(g.difficulty)) #init enemy with appropriate difficulty mods
        self.game = g
        self.healthbar = ui.HealthBar(self.game.player.getHP(), self.game.player.getMaxHP(), (50,50))
        self.enemy_healthbar = ui.HealthBar(self.enemy.getHP(), self.enemy.getMaxHP(), (500,50))
        self.button_attack = ui.Button("attack", 220, 60, (300, 450), function=self.sliderQTE)
    
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

    # when a player presses the attack button:
    #   - corresponding QTE event will play for attack (will implement other attacks/QTEs later)
    #   - hp is decreased based on damage (damage is set to a fixed amount for now)
    #   - increase number of combat encounters
    #   - after enemy dies:
    #     - (will be implementing a pick up item screen later)
    #     - go to room selection screen
    def sliderQTE(self):
        numHits = QTE.handleTimeSliderQTE(3)
        total_damage = self.game.player.generateDamage()*numHits
        self.enemy.takeDamage(total_damage)
        # GAME STAT
        self.game.stats.set_damage_delt(total_damage)
        enemy_dmg = self.enemy.generateDamage()
        self.game.player.takeDamage(enemy_dmg)
        # GAME STAT
        self.game.stats.set_damage_taken(enemy_dmg)
        if (self.game.player.getHP() <= 0):
            self.cur = 0
            # GAME STAT
            self.game.stats.set_battles_lost()
            self.game.transitionToDefeat()
        if (self.enemy.getHP() <= 0):
            # GAME STAT
            self.game.stats.set_battles_won()
            self.game.increaseEncounters()
            self.game.transitionToReward()

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game.transitionToLoad()

# Class for handling boss battle
class Boss(GameState):
    
    def __init__(self, g):
        self.name = "BOSS BATTLE"
        self.background = "#590019"
        self.game = g
        self.enemy = classes.Enemy("Skeleton Boss",g.difficultyMods.get(g.difficulty), hp=200, atk=15)
        self.healthbar = ui.HealthBar(self.game.player.getHP(), self.game.player.getMaxHP(), (50,50))
        self.enemy_healthbar = ui.HealthBar(self.enemy.getHP(), self.enemy.getMaxHP(), (500,50))
        self.button_attack = ui.Button("attack", 220, 60, (300, 450), function=self.sliderQTE)

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
        self.enemy.drawBoss(surface, 600, 300)
        self.game.player_turn = True
        self.game.player_attack = 0
        self.enemy_attack = 0
        pass

    # when a player presses the attack button:
    #   - corresponding QTE event will play for attack (will implement other attacks/QTEs later)
    #   - hp is decreased based on damage (damage is set to a fixed amount for now)
    #   - (player taking damage from enemy will be implemented later)
    #   - after enemy dies:
    #     - reset total number of combat encounters
    #     - (will be implementing a pick up item screen later)
    #     - go to victory screen
    def sliderQTE(self):
        numHits = QTE.handleTimeSliderQTE(3)
        total_damage = self.game.player.generateDamage()*numHits
        self.enemy.takeDamage(total_damage)
        # GAME STAT
        self.game.stats.set_damage_delt(total_damage)
        enemy_dmg = self.enemy.generateDamage()
        self.game.player.takeDamage(enemy_dmg)
        # GAME STAT
        self.game.stats.set_damage_taken(enemy_dmg)
        if (self.game.player.getHP() <= 0):
            self.cur = 0
            # GAME STAT
            self.game.stats.set_battles_lost()
            self.game.transitionToDefeat()
        if (self.enemy.getHP() <= 0):
            # GAME STAT
            self.game.stats.set_bosses_defeated()
            self.game.stats.set_battles_won()
            self.game.transitionToVictory()

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_h:
                self.enemy.takeDamage(10)
            if event.key == pg.K_SPACE:
                self.game.transitionToLoad()


# Class for handling the shop features
class Shop(GameState):
    
    def __init__(self, g):
        self.name = "SHOP"
        self.background = "#04395e"
        self.game = g
        self.button_enter = ui.Button("enter shop", 220, 60, (300,250), function=self.enterShop)
        self.button_leave = ui.Button("leave shop", 220, 60, (300,400), function=self.leaveShop)
    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
    def loadUI(self,surface):
        self.button_enter.draw(surface)
        self.button_leave.draw(surface)
        pass

    def enterShop(self):
        self.game.transitionToShopMenu()

    def leaveShop(self):
        self.game.transitionToLoad()

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game.transitionToLoad()


# Class for handling the player entering shop
class ShopMenu(GameState):
    
    def __init__(self, g):
        self.name = "SHOP MENU"
        self.background = "#04395e"
        self.game = g
        self.button_buy = ui.Button("buy items", 220, 60, (60,400), function=self.buyItems)
        self.button_sell = ui.Button("sell items", 220, 60, (300,400), function=self.sellItems)
        self.button_back = ui.Button("close menu", 220, 60, (540,400), function=self.closeMenu)
    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
    def loadUI(self,surface):
        self.button_buy.draw(surface)
        self.button_sell.draw(surface)
        self.button_back.draw(surface)
        pass

    def closeMenu(self):
        self.game.transitionToShop()

    def buyItems(self):
        pass

    def sellItems(self):
        pass

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game.transitionToLoad()


# Class for handling difficulty selection
class Difficulty(GameState):
    
    def __init__(self, g):
        self.name = "SELECT DIFFICULTY"
        self.background = "#0c2a31"
        self.game = g
        self.button_easy = ui.Button("easy", 220, 60, (60,450), function=self.setEasyDifficulty)
        self.button_normal = ui.Button("normal", 220, 60, (300,450), function=self.setNormalDifficulty)
        self.button_hard = ui.Button("hard", 220, 60, (540,450), function=self.setHardDifficulty)
    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
    def loadUI(self,surface):
        self.button_easy.draw(surface)
        self.button_normal.draw(surface)
        self.button_hard.draw(surface)
        pass

    def handleActions(self, event):
        pass

    def setEasyDifficulty(self):
        self.game.setDifficulty(0)
        self.game.transitionToMenu()

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
        self.background = "#0c2a31"
        self.game = g
        self.button_room_rd = ui.Button("???", 220, 60, (60,400), function=self.rdRoom)
        self.button_room_shop = ui.Button("shop", 220, 60, (540,400), function=self.shopRoom)

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
    def loadUI(self,surface):
        self.button_room_rd.draw(surface)
        self.button_room_shop.draw(surface)
        pass

    def handleActions(self, event):
        pass

    def rdRoom(self):
        if rd.random() > 0.5:
            self.game.transitionToLoad()
        else:
            self.game.transitionToShop()
        #self.game.transitionToLoad() if rd.random() > 0.5 else self.game.transitionToShop()

    def shopRoom(self):
        self.game.transitionToShop()


# Class for handling the victory screen
# Brings the player back to the main menu screen
class Victory(GameState):
    
    def __init__(self, g):
        self.name = "VICTORY"
        self.background = "#5A8B82"
        self.game = g
        self.button_restart = ui.Button("restart", 220, 60, (300,460), function=self.game.transitionToMenu)

    def displayAchievements(self, surface):
        completed = self.game.stats.achievements.getCompletedAchievements()
        start_pos = 140
        ui.drawText(surface, "Achievements:", (300,start_pos))
        for ach in completed:
            start_pos += 40
            ui.drawText(surface, ach, (300,start_pos))

    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
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
        self.background = "#00060e"
        self.game = g
        self.game.player.setHP()
        self.button_restart = ui.Button("restart", 220, 60, (300,460), function=self.game.transitionToMenu)

    def displayAchievements(self, surface):
        completed = self.game.stats.achievements.getCompletedAchievements()
        start_pos = 140
        ui.drawText(surface, "Achievements:", (300,start_pos))
        for ach in completed:
            start_pos += 40
            ui.drawText(surface, ach, (300,start_pos))

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
        self.background = "#BC88DF"
        self.game = g
        # initialize items
        activeItem = item.Item()
        activeItem.randomAbility("Active")
        activeItem.randomValueWideRange(10, 25, self.game.difficulty)
        passiveItem = item.Item()
        passiveItem.randomAbility("Passive")
        passiveItem.randomValueWideRange(10, 25, self.game.difficulty)
        self.item1 = activeItem.getItem()
        self.item2 = passiveItem.getItem()
        self.button_item1 = ui.Button("get "+self.item1[1], 220, 60, (60,300), function=self.getItem1)
        self.button_item2 = ui.Button("get "+self.item2[1], 220, 60, (540,300), function=self.getItem2)
    
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
    def loadUI(self,surface):
        self.button_item1.draw(surface)
        self.button_item2.draw(surface)

    def getItem1(self):
        # put item 1 into player class inventory
        self.game.player.items.append(self.item1)
        self.game.transitionToRoomSelection()

    def getItem2(self):
        # put item 2 into player class inventory
        self.game.player.items.append(self.item2)
        self.game.transitionToRoomSelection()

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()