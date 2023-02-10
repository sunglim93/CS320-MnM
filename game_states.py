import os
import multiprocessing as mp
import pygame
import game
import time
import UIElements
from random import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
import openai


# Abstract class that provides methods
# that each GameState method should have
# to ensure functionality
class GameState():

    # When instantiating one of the following
    # GameState classes, you should pass the current
    # Game class.
    def getName(self):
        pass

    def getBackground(self):
        pass

    def loadUI(self):
        pass

    def handleActions(self):
        pass


# Class for handling the main menu
class Menu(GameState):

    def __init__(self, g):
        self.name = "MENU"
        self.background = "#0c2a31"
        self.color = "#bce7fc"
        self.font = pygame.font.Font("assets/alagard.ttf", 40)
        self.game = g
        self.button_start = UIElements.Button("start", 220, 60, (300, 300), function=self.game.transitionToLoad)

    def getName(self):
        return self.name

    def getBackground(self):
        return self.background

    def loadUI(self, surface):
        self.button_start.draw(surface)
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
            self.current_room =room_id
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
        self.background = "#0c2a31"
        self.color = "#bce7fc"
        self.font = pygame.font.Font("assets/alagard.ttf", 40)
        self.game = g
        self.button_start = UIElements.Button("start", 220, 60, (300, 300), function=self.game.transitionToLoad)
        self.image = None

    def getName(self):
        return self.name

    def getBackground(self):
        return self.background

    def loadUI(self, surface):
        pass

    def ai_image(self):
        with open('game.config') as fp:
            line = next(fp)
            parts = line.split('=')
            openai.api_key = parts[1].strip()
            response = openai.Image.create(
                prompt="An armored character running away from enemies in a castle",
                n=1,
                size="512x512"
            )

            image_url = response["data"][0]["url"]
            im = Image.open(BytesIO(requests.get(image_url).content))
            return im

    def pixelate_ai_image(self, im, size=16):
        #  im = im.resize((im.width // 4, im.height // 4), resample=Image.NEAREST)
        im = im.resize((im.width, im.height), resample=Image.NEAREST)
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
        pygame.display.set_mode((pixeled_image.width, pixeled_image.height))
        self.image = pygame.image.fromstring(pixeled_image.tobytes(),
                                             (pixeled_image.width, pixeled_image.height),
                                             "RGB")
        image.save(file)

    def load_cache_or_remote(self):
        if self.image is None:
            for file in os.listdir("image_cache"):
                pixeled_image = Image.open(f"image_cache/{file}")
                self.image = pygame.image.fromstring(pixeled_image.tobytes(),
                                                     (pixeled_image.width, pixeled_image.height),
                                                     "RGB")
                pygame.display.set_mode((pixeled_image.width, pixeled_image.height))
                # p = mp.Process(target=self.fetch_remote)
                # p.start()
                return

            self.fetch_remote()



    def draw(self, screen):
        self.load_cache_or_remote()
        pygame.display.set_caption("Metal and Magic")
        screen.blit(self.image, (0, 0))

        font = pygame.font.Font(None, 36)
        text = font.render("LOADING", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.image.get_width() // 2, self.image.get_height() // 2)
        pygame.draw.rect(screen, (0, 0, 0), (text_rect.left - 20, text_rect.top - 20,
                                             text_rect.width + 40, text_rect.height + 40), 0)
        screen.blit(text, text_rect)

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToCombat() if random() > 0.5 else self.game.transitionToShop()


# Class for handling the combat scenarios
class Combat(GameState):

    def __init__(self, g):
        self.name = "COMBAT"
        self.background = "#dab785"
        self.game = g
        self.cur = 100
        self.healthbar = UIElements.HealthBar(self.cur, 100, (50, 50))

    def getName(self):
        return self.name

    def getBackground(self):
        return self.background

    def loadUI(self, surface):
        self.healthbar.update(self.cur, 100)
        self.healthbar.draw(surface)
        pass

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.cur -= 10
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()


# Class for handling the shop features
class Shop(GameState):

    def __init__(self, g):
        self.name = "SHOP"
        self.background = "#04395e"
        self.game = g

    def getName(self):
        return self.name

    def getBackground(self):
        return self.background

    def loadUI(self, surface):
        pass

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()
