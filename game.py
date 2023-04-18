import pygame
from PIL import Image
from pygame.locals import *
from pygame import mixer 
from model import game_states
from controller import QTE
from model import classes
from model import achievement
from model.game_states import Audio
from view import UIElements as ui

# The Game class handles all the transitions and states the game
# can be in. This is how the main function will interract with 
# the game.
#                                                       -Travis

class Game():
    audio = Audio()
    def __init__(self):
        # By default the game is initialized to the Main state
        pal = Image.open('assets/palettes/Default.png').getcolors()
        self.colors = {
            'lightTwo' : pal[0][1],
            'lightOne' : pal[1][1],
            'midThree' : pal[2][1],
            'midTwo' : pal[3][1],
            'midOne' : pal[4][1],
            'baseThree' : pal[5][1],
            'baseTwo' : pal[6][1],
            'baseOne' : pal[7][1],
        }
        self.cur_state = game_states.Menu(self)
        self.run = True
        self.difficulty = 0
        self.numEncounters = 0
        self.numBossEncounters = 0
        self.player = classes.Player("Armored Soul", self)
        self.stats = achievement.GameStats()
        self.difficultyMods = { #dictionary containing modifiers
            0 : 0.5, #easy
            1 : 1.0, #medium
            2 : 1.5 #hard
        }
    
    def load_palette(self,pal_name):
        pal = Image.open('assets/palettes/'+pal_name).getcolors()
        self.colors = {
            'lightTwo' : pal[0][1],
            'lightOne' : pal[1][1],
            'midThree' : pal[2][1],
            'midTwo' : pal[3][1],
            'midOne' : pal[4][1],
            'baseThree' : pal[5][1],
            'baseTwo' : pal[6][1],
            'baseOne' : pal[7][1],
        }
        self.player.update_sprite(self.colors)

    # difficulty settings
    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def getDifficulty(self):
        return self.difficulty

    # keep track of battles that the player has encountered
    def getEncounters(self):
        return self.numEncounters

    def getColor(self, color):
        return self.colors[color]
    
    def getPalette(self):
        return self.colors

    def increaseEncounters(self):
        self.numEncounters += 1

    def increaseBossEncounters(self):
        self.numBossEncounters += 1

    def resetEncounters(self):
        self.numEncounters = 0

    def resetBossEncounters(self):
        self.numBossEncounters = 0

    # allows the current state to be changed
    def set_state(self, new_state=0):
        self.cur_state = new_state

    # returns the current state
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

    # allows main loop to check the game is still running
    def transitionToSettings(self):
        self.cur_state = game_states.Settings(self)
    def transitionToRoomSelection(self):
        self.cur_state = game_states.RoomSelection(self)
    def transitionToShopMenu(self):
        self.cur_state = game_states.ShopMenu(self)
    def transitionToVictory(self):
        self.cur_state = game_states.Victory(self)
    def transitionToBoss(self):
        self.cur_state = game_states.Boss(self)
    def transitionToMinigame(self):
        self.cur_state = game_states.Minigame(self)
    def transitionToDefeat(self):
        self.cur_state = game_states.Defeat(self)
    def transitionToReward(self):
        self.cur_state = game_states.Reward(self)
    def transitionToBuy(self):
        self.cur_state = game_states.Buy(self)
    def transitionToTreasure(self):
        self.cur_state = game_states.Treasure(self)
    def transitionToGetTreasure(self):
        self.cur_state = game_states.GetTreasure(self)

    #allows main loop to check the game is still running
    def running(self):
        return self.run

    # allows the gmae to exit
    def quit(self):
        self.run = False
