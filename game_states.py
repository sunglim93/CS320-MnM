import pygame
import game
import UIElements
from random import random
import MnM


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
        self.button_start = UIElements.Button("start", 220, 60, (300,300), function=self.game.transitionToDifficulty)
    
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

    # after the player has encountered 3 combat states, transition to the boss combat state
    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.game.getEncounters() < 3:
                    self.game.transitionToCombat()
                else:
                    self.game.transitionToBoss()


#Class for handling the combat scenarios
class Combat(GameState):
    
    def __init__(self, g):
        self.name = "COMBAT"
        self.background = "#BC88DF"
        self.game = g
        self.cur = 100
        self.healthbar = UIElements.HealthBar(self.cur, 100, (50,50))
        self.button_attack = UIElements.Button("attack", 220, 60, (300,300), function=self.sliderQTE)

    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.healthbar.update(self.cur, 100)
        self.healthbar.draw(surface)
        self.button_attack.draw(surface)
        pass

    # when a player presses the attack button:
    #   - corresponding QTE event will play for attack (will implement other attacks/QTEs later)
    #   - hp is decreased based on damage (damage is set to a fixed amount for now)
    #   - increase number of combat encounters
    #   - (will be implementing a pick up item screen later)
    #   - go to room selection screen
    def sliderQTE(self):
        # temporarily taking out qte since there seems to be an issue with it taking mouse input
        #MnM.handleSliderQTE()
        self.healthbar = UIElements.HealthBar(self.cur -50, 100, (50,50))
        self.cur = self.cur - 50
        if (self.cur <= 0):
            self.game.increaseEncounters()
            self.game.transitionToRoomSelection()

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.cur -= 10
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()


#Class for handling boss battle
class Boss(GameState):
    
    def __init__(self, g):
        self.name = "BOSS BATTLE"
        self.background = "#590019"
        self.game = g
        self.cur = 100
        self.healthbar = UIElements.HealthBar(self.cur, 100, (50,50))
        self.button_attack = UIElements.Button("attack", 220, 60, (300,300), function=self.sliderQTE)

    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.healthbar.update(self.cur, 100)
        self.healthbar.draw(surface)
        self.button_attack.draw(surface)
        pass

    # when a player presses the attack button:
    #   - corresponding QTE event will play for attack (will implement other attacks/QTEs later)
    #   - hp is decreased based on damage (damage is set to a fixed amount for now)
    #   - (player taking damage from enemy will be implemented later)
    #   - reset total number of combat encounters
    #   - (will be implementing a pick up item screen later)
    #   - go to victory screen
    def sliderQTE(self):
        # temporarily taking out qte since there seems to be an issue with it taking mouse input
        #MnM.handleSliderQTE()
        self.healthbar = UIElements.HealthBar(self.cur -20, 100, (50,50))
        self.cur = self.cur - 20
        if (self.cur <= 0):
            self.game.resetEncounters()
            self.game.transitionToVictory()

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
        self.button_enter = UIElements.Button("enter shop", 220, 60, (300,250), function=self.enterShop)
        self.button_leave = UIElements.Button("leave shop", 220, 60, (300,400), function=self.leaveShop)
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.button_enter.draw(surface)
        self.button_leave.draw(surface)
        pass

    def enterShop(self):
        self.game.transitionToShopMenu()

    def leaveShop(self):
        self.game.transitionToLoad()

    def handleActions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()


#Class for handling the player entering shop
class ShopMenu(GameState):
    
    def __init__(self, g):
        self.name = "SHOP MENU"
        self.background = "#04395e"
        self.game = g
        self.button_buy = UIElements.Button("buy items", 220, 60, (60,400), function=self.buyItems)
        self.button_sell = UIElements.Button("sell items", 220, 60, (300,400), function=self.sellItems)
        self.button_back = UIElements.Button("close menu", 220, 60, (540,400), function=self.closeMenu)
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.transitionToLoad()


#Class for handling difficulty selection
class Difficulty(GameState):
    
    def __init__(self, g):
        self.name = "SELECT DIFFICULTY"
        self.background = "#0c2a31"
        self.game = g
        self.button_easy = UIElements.Button("easy", 220, 60, (60,400), function=self.setEasyDifficulty)
        self.button_normal = UIElements.Button("normal", 220, 60, (300,400), function=self.setNormalDifficulty)
        self.button_hard = UIElements.Button("hard", 220, 60, (540,400), function=self.setHardDifficulty)
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.button_easy.draw(surface)
        self.button_normal.draw(surface)
        self.button_hard.draw(surface)
        pass

    def handleActions(self, event):
        pass

    def setEasyDifficulty(self):
        self.game.setDifficulty(0)
        self.game.transitionToLoad()

    def setNormalDifficulty(self):
        self.game.setDifficulty(1)
        self.game.transitionToLoad()

    def setHardDifficulty(self):
        self.game.setDifficulty(2)
        self.game.transitionToLoad()


#Class for handling room selection
#  Allows player to select two different paths
class RoomSelection(GameState):
    
    def __init__(self, g):
        self.name = "Select a path"
        self.background = "#0c2a31"
        self.game = g
        self.button_room_random = UIElements.Button("???", 220, 60, (60,400), function=self.randomRoom)
        self.button_room_shop = UIElements.Button("shop", 220, 60, (540,400), function=self.shopRoom)

    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.button_room_random.draw(surface)
        self.button_room_shop.draw(surface)
        pass

    def handleActions(self, event):
        pass

    def randomRoom(self):
        self.game.transitionToCombat() if random() > 0.7 else self.game.transitionToShop()

    def shopRoom(self):
        self.game.transitionToShop()


#Class for handling the victory screen
#  Brings the player back to the main menu screen
class Victory(GameState):
    
    def __init__(self, g):
        self.name = "VICTORY"
        self.background = "#5A8B82"
        self.game = g
        self.button_restart = UIElements.Button("restart", 220, 60, (300,400), function=self.menu)
    
    def getName(self):
        return self.name
    
    def getBackground(self):
        return self.background
    
    def loadUI(self,surface):
        self.button_restart.draw(surface)
        pass

    def handleActions(self, event):
        pass

    def menu(self):
        self.game.transitionToMenu()