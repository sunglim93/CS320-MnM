import pygame
import game_states

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
    
    #lists all states and allows a transition to the next state
    def transitionToNext(self, state):
        if state == "MENU":
            self.cur_state = game_states.Menu(self)
        elif state == "LOAD":
            self.cur_state = game_states.Loading(self)
        elif state == "COMBAT":
            self.cur_state = game_states.Combat(self)
        elif state == "SHOP":
            self.cur_state = game_states.Shop(self)
    
    #allows main loop to check the game is still running
    def running(self):
        return self.run

    #allows the gmae to exit
    def quit(self):
        self.run = False