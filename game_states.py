import pygame
import game
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

    # When instanciating one of the following
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



#Class for handling the main menu
class Menu(GameState):

    def __init__(self, g):
        openai.api_key = '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'
        self.name = "MENU"
        self.background = "#0c2a31"
        self.color = "#bce7fc"
        self.font = pygame.font.Font("assets/alagard.ttf", 40)
        self.game = g
        self.button_start = UIElements.Button("start", 220, 60, (300,300), function=self.game.transitionToLoad)

    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.button_start.draw(surface)
        pass

    def handleActions(self, event):
        pass

    def draw(self, screen):
        img = self.font.render(self.name, True, self.color)
        screen.blit(img, (160, 250))


#Class for handling the loading screen
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
    
    def loadUI(self,surface):
        pass


    def ai_image(self):
        openai.api_key = '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'
        response = openai.Image.create(
            prompt="An armored roguelike character running away from enemies in a castle",
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


    def draw(self, screen):
        if self.image is None:
            image = self.ai_image()
            pixeled_image = self.pixelate_ai_image(image)
            #pixeled_image = pygame.image.load("C:\\Users\\Andy\\Desktop\\text image example.PNG")

            pygame.display.set_caption("Metal and Magic")

            screen = pygame.display.set_mode((pixeled_image.width, pixeled_image.height))

            self.image = pygame.image.fromstring(pixeled_image.tobytes(), (pixeled_image.width, pixeled_image.height), "RGB")

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

#Class for handling the combat scenarios
class Combat(GameState):
    
    def __init__(self, g):
        self.name = "COMBAT"
        self.background = "#dab785"
        self.game = g
        self.cur = 100
        self.healthbar = UIElements.HealthBar(self.cur, 100, (50,50))

    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.healthbar.update(self.cur, 100)
        self.healthbar.draw(surface)
        pass
    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.cur -= 10
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()

#Class for handling the shop features
class Shop(GameState):
    
    def __init__(self, g):
        self.name = "SHOP"
        self.background = "#04395e"
        self.game = g
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        pass

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()
