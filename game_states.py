import pygame
import game
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
    def getBackground(self):
        pass
    def loadUI(self):
        pass
    def handleActions(self):
        pass


#Class for handling the main menu
class Menu(GameState):
    
    def __init__(self, g):
        self.name = "MENU"
        self.background = "#0c2a31"
        self.game = g
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self):
        pass

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:                    self.game.transitionToNext("LOAD")
            elif event.key == pygame.K_ESCAPE:
                self.game.transitionToNext("MENU")

#Class for handling the loading screen
class Loading(GameState):
    
    def __init__(self, g):
        self.name = "LOADING"
        self.background = "#70d1a1"
        self.game = g
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self):
        pass

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ns = "COMBAT" if random() > 0.5 else "SHOP"
                self.game.transitionToNext(ns)
            elif event.key == pygame.K_ESCAPE:
                self.game.transitionToNext("MENU")

#Class for handling the combat scenarios
class Combat(GameState):
    
    def __init__(self, g):
        self.name = "COMBAT"
        self.background = "#420420"
        self.game = g

    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self):
        pass
    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToNext("LOAD")
            elif event.key == pygame.K_ESCAPE:
                self.game.transitionToNext("MENU")

#Class for handling the shop features
class Shop(GameState):
    
    def __init__(self, g):
        self.name = "SHOP"
        self.background = "#e9c46a"
        self.game = g
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self):
        pass

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToNext("LOAD")
            elif event.key == pygame.K_ESCAPE:
                self.game.transitionToNext("MENU")
