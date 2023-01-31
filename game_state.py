import pygame

class Game():

    def __init__(self):
        self.cur_state = 0
        self.states = (("menu", "#0c2a31"),("combat", "#420420"),("loading", "#70d1a1"))

    def set_state(self,new_state=0):
        self.cur_state = new_state

    def get_name(self):
        return self.states[self.cur_state][0]

    def get_color(self):
        return self.states[self.cur_state][1]
        
    def state_change(self):
        if self.cur_state == 0:
            return 1
        elif self.cur_state == 1:
            return 2
        elif self.cur_state == 2:
            return 1
        pass