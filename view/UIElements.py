import pygame
from PIL import Image
from pygame.locals import *
from pygame import mixer
from model import game_states as game_states

# Declare default font for UI elements
pygame.font.init()
UI_font = pygame.font.Font("assets/alagard.ttf",24)
mixer.init()

#method for displaying text on screen
def drawText(surface, text, pos, text_col="#bce7fc"):
    img = UI_font.render(text, True, text_col)
    surface.blit(img,(pos))


def adapt_image(img_file, palette):
    def_palette = Image.open('assets/palettes/Default.png').getcolors()
    render_img = Image.open(img_file)
    pixels = render_img.load()
    for i in range(render_img.size[0]):
        for j in range (render_img.size[1]):
            if pixels[i,j] == def_palette[0][1]:
                pixels[i,j] = palette['lightTwo']
            elif pixels[i,j] == def_palette[1][1]: 
                pixels[i,j] = palette['lightOne']
            elif pixels[i,j] == def_palette[2][1]: 
                pixels[i,j] = palette['midThree']
            elif pixels[i,j] == def_palette[3][1]: 
                pixels[i,j] = palette['midTwo']
            elif pixels[i,j] == def_palette[4][1]: 
                pixels[i,j] = palette['midOne']
            elif pixels[i,j] == def_palette[5][1]: 
                pixels[i,j] = palette['baseThree']
            elif pixels[i,j] == def_palette[6][1]: 
                pixels[i,j] = palette['baseTwo']
            elif pixels[i,j] == def_palette[7][1]: 
                pixels[i,j] = palette['baseOne']
            elif pixels[i,j] == (0,0,0,0):
                pixels[i,j] = (0,0,0,0)
    return pygame.image.fromstring(render_img.tobytes(),render_img.size,render_img.mode)


class Button():
    #If no aciton is passed to a button, this function will fire
    def default_action():
        print("no action was assigned to button")
    
    #Constructor for a button takes the following parameters
    # text - What the button displays
    # width - width of the button object
    # height - height of the button object
    # pos - position of the button on screen starting with the top left corner
    # (optional)
    # elevation - the distance the button collapses when pressed
    # function - a function pointer that will be called when the button is pressed
    def __init__(self,text, width, height, pos, palette, elevation=6, function=default_action, parameter=None):

        # button by default is not pressed
        self.pressed = False
        self.parameters = parameter
        # create the rectangles that make up the button
        self.top_rect = pygame.Rect(pos, (width, height))
        self.bot_rect = pygame.Rect(pos, (width, height))
        self.top_rect_original_width = width
        self.top_rect_original_height = height
        self.top_color = palette['lightTwo']
        self.bot_color = palette['lightOne']

        # elevation is the distance between the top and button rectangles
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]

        # creates the text object that will be displayed with the button
        self.text = text
        self.text_surface = UI_font.render(text,False,palette['baseOne'])
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)

        # set function pointer
        self.function = function

    # draw function takes the surface parameter
    def draw(self, surface):

        # set the position based on current button elevation
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        # display the elements on screen
        pygame.draw.rect(surface, self.bot_color, self.bot_rect, border_radius=4)
        pygame.draw.rect(surface,self.top_color,self.top_rect, border_radius=4)
        surface.blit(self.text_surface, self.text_rect)

        # check if button is pressed
        self.check_click()

    def check_click(self):

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check collision with button
        if self.top_rect.collidepoint(pos):
            
            # resize to indicate clickable object to user
            self.top_rect.width = self.top_rect_original_width + 3
            self.top_rect.height = self.top_rect_original_height + 3
            self.bot_rect.width = self.top_rect_original_width + 3
            self.bot_rect.height = self.top_rect_original_height + 3

            # if button is clicked (pressed and released) fire function and
            # change elevation to indicate button click to user
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                #button_press_sfx = mixer.Sound('assets/buttonpress.wav')
                audio = game_states.Audio()
                audio.button_sound.set_volume(0.25)
                audio.button_sound.play()

                self.dynamic_elevation = 3
                self.pressed = True
                if self.parameters == None:
                    self.function()
                else:
                    self.function(self.parameters)

            # otherwise, elevation is set to default
            if not pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = self.elevation
                self.pressed = False
        # if no collison, set to default state
        else:
            self.top_rect.width = self.top_rect_original_width
            self.top_rect.height = self.top_rect_original_height
            self.bot_rect.width = self.top_rect_original_width
            self.bot_rect.height = self.top_rect_original_height            
            self.dynamic_elevation = self.elevation

class HealthBar():

    # Constructor for a HealthBar takes the following parameters:
    # cur - the current health value of the entity
    # max - the maximum health value the entity could have
    # pos - the (x,y) coordinate of where the healthbar should be displayed
    # [Height and Width are optional values. If left blank, the object will
    #  be assumed to be for a player or a boss and instanciate itself as a
    #  30px by 200px HealthBar]
    # height - the height of the healthbar
    # width - the width of the healthbar
    def __init__(self, cur, max, pos, palette, height=30, width=200):
        self.cur = cur
        self.max = max
        self.pos = pos
        self.height = height
        self.width = width
        # delcaring the rectangles for display
        self.base_color = palette['midOne']
        self.cur_color = palette['lightOne']
        self.text_color = palette['midThree']
        self.rect_base = pygame.Rect(self.pos, (self.width, self.height))
        self.rect_cur = pygame.Rect(self.pos, ((self.cur/self.max)*(self.width-3), self.height-3))
        # declaring the text object to display current values
        self.text = str(cur) + " / " + str(max)
        self.text_surface = UI_font.render(self.text,False,palette['midThree'])
        self.text_rect = self.text_surface.get_rect(center = self.rect_base.center)

    # use the update method to update the max and min health during combat
    def update(self, cur, max):
        if self.cur != cur:
            if self.cur > cur:
                mixer.Sound('assets/damage.wav').play()
            self.cur = cur
            self.max = max
            self.rect_cur = pygame.Rect(self.pos, ((cur/max)*(self.width-3), self.height-3))
            self.text = str(cur) + " / " + str(max)
            self.text_surface = UI_font.render(self.text,False,self.text_color)
            self.text_rect = self.text_surface.get_rect(center = self.rect_base.center)

        
    def draw(self, surface):
        #drawing the healthbar and current values onto the screen
        pygame.draw.rect(surface, self.base_color, self.rect_base, border_radius=4)
        pygame.draw.rect(surface, self.cur_color, self.rect_cur, border_radius=4)
        surface.blit(self.text_surface, self.text_rect)

