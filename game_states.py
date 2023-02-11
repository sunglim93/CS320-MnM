import pygame
import game
import UIElements
from random import random


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
    def loadUI(self, surface):
        pass
    def handleActions(self):
        pass


#Class for handling the main menu
class Menu(GameState):

    def __init__(self, g):
        self.game = g
        self.name = "MENU"
        pygame.font.init()
        self.MenuFont = pygame.font.Font("assets/alagard.ttf",64)
        self.background = pygame.image.load('assets/menu.png')
        self.background = pygame.transform.scale(self.background,(pygame.display.get_surface().get_size()))
        self.button_start = UIElements.Button("START", 200, 40, (300,300), function=self.game.transitionToLoad)
        self.button_settings = UIElements.Button("SETTINGS", 200, 40, (300,360), function=self.game.transitionToLoad)
        self.button_quit = UIElements.Button("QUIT", 200, 40, (300,420), function=self.game.quit)

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

#Class for handling the loading screen
class Loading(GameState):
    
    def __init__(self, g):
        self.name = "LOADING"
        self.background = "#70a288"
        self.game = g
    def getName(self):
        return self.name
    
    def loadBackground(self, surface):
        surface.fill(self.background)

    def loadUI(self,surface):
        pass

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
    
    def loadBackground(self, surface):
        surface.fill(self.background)

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
    
    def loadBackground(self, surface):
        surface.fill(self.background)
    
    def loadUI(self,surface):
        pass

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()
