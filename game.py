import pygame
from pygame.locals import *
from pygame import mixer 
from model import game_states
from controller import QTE
from model import classes

# The Game class handles all the transitions and states the game
# can be in. This is how the main function will interract with 
# the game.
#                                                       -Travis

class Game():

    def __init__(self):
        #By default the game is initialized to the Main state
        self.cur_state = game_states.Menu(self)
        self.run = True
        self.difficulty = 0
        self.numEncounters = 0
        self.player = classes.Player("Armored Soul")
        self.difficultyMods = { #dictionary containing modifiers
            0 : 0.5, #easy
            1 : 1.0, #medium
            2 : 1.5 #hard
        }
        
    # difficulty settings
    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def getDifficulty(self):
        return self.difficulty

    # keep track of battles that the player has encountered
    def getEncounters(self):
        return self.numEncounters

    def increaseEncounters(self):
        self.numEncounters += 1

    def resetEncounters(self):
        self.numEncounters = 0

    #allows the current state to be changed
    def set_state(self, new_state=0):
        self.cur_state = new_state

    #returns the current state
    def get_state(self):
        return self.cur_state
    
    #state transitions
    def transitionToLoad(self):
        self.cur_state = game_states.Loading(self)
    def transitionToMenu(self):
        self.cur_state = game_states.Menu(self)
    def transitionToCombat(self):
        self.cur_state = game_states.Combat(self)
    def transitionToShop(self):
        self.cur_state = game_states.Shop(self)
    def transitionToDifficulty(self):
        self.cur_state = game_states.Difficulty(self)
    def transitionToRoomSelection(self):
        self.cur_state = game_states.RoomSelection(self)
    def transitionToShopMenu(self):
        self.cur_state = game_states.ShopMenu(self)
    def transitionToVictory(self):
        self.cur_state = game_states.Victory(self)
    def transitionToBoss(self):
        self.cur_state = game_states.Boss(self)

    #allows main loop to check the game is still running
    def running(self):
        return self.run

    #allows the gmae to exit
    def quit(self):
        self.run = False