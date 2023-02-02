import pygame
import game_states

class Game():

    def __init__(self):
        self.cur_state = game_states.Menu(self)
        self.run = True

    def set_state(self,new_state=0):
        self.cur_state = new_state

    def get_state(self):
        return self.cur_state
    
    def transitionToNext(self, state):
        if state == "MENU":
            self.cur_state = game_states.Menu(self)
        elif state == "LOAD":
            self.cur_state = game_states.Loading(self)
        elif state == "COMBAT":
            self.cur_state = game_states.Combat(self)
        elif state == "SHOP":
            self.cur_state = game_states.Shop(self)
    
    def running(self):
        return self.run

    def quit(self):
        self.run = False