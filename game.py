import pygame
from pygame.locals import *
from pygame import mixer 
import game_states
import MnM

# The Game class handles all the transitions and states the game
# can be in. This is how the main function will interract with 
# the game.
#                                                       -Travis

class Game():

    def __init__(self):
        #By default the game is initialized to the Main state
        self.cur_state = game_states.Menu(self)
        self.run = True

    #allows the current state to be changed
    def set_state(self,new_state=0):
        self.cur_state = new_state

    #returns the current state
    def get_state(self):
        return self.cur_state
    
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

    #allows main loop to check the game is still running
    def running(self):
        return self.run

    #allows the gmae to exit
    def quit(self):
        self.run = False