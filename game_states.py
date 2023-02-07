import pygame as pg
import ui_elements as ui
import classes as gc
from random import random
import game

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
        self.game = g
        self.button_start = ui.Button("start", 220, 60, (300,300), function=self.game.transitionToLoad)
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.button_start.draw(surface)
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
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        pass

    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game.transitionToCombat() if random() > 0.5 else self.game.transitionToShop()

#Class for handling the combat scenarios
class Combat(GameState):
    
    def __init__(self, g):
        self.name = "COMBAT"
        self.background = (0,0,0)
        self.game = g
        # self.cur = 100
        # self.healthbar = ui.HealthBar(self.cur, 100, (50,50))

    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        # self.healthbar.update(self.cur, 100)
        # self.healthbar.draw(surface)
        pass
        
    def handleActions(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_h:
                self.cur -= 10
            if event.key == pg.K_SPACE:
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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game.transitionToLoad()
