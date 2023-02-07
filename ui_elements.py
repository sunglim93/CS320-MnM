import pygame as pg

# Declare default font for UI elements
pg.font.init()
UI_font = pg.font.Font("assets/alagard.ttf",24)


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
    def __init__(self,text, width, height, pos, elevation=6, function=default_action):

        # button by default is not pressed
        self.pressed = False

        # create the rectangles that make up the button
        self.top_rect = pg.Rect(pos, (width, height))
        self.bot_rect = pg.Rect(pos, (width, height))
        self.top_rect_original_width = width
        self.top_rect_original_height = height
        self.top_color = "#dab785"
        self.bot_color = "#d6896f"

        # elevation is the distance between the top and button rectangles
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]

        # creates the text object that will be displayed with the button
        self.text = text
        self.text_surface = UI_font.render(text,False,"#00060e")
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)

        # set function pointer
        self.function = function

    # draw function takes the surface parameter
    def draw(self, surface):

        # set the position based on current button elevation
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        # display the elements on screen
        pg.draw.rect(surface, self.bot_color, self.bot_rect, border_radius=4)
        pg.draw.rect(surface,self.top_color,self.top_rect, border_radius=4)
        surface.blit(self.text_surface, self.text_rect)

        # check if button is pressed
        self.check_click()

    def check_click(self):

        # get mouse position
        pos = pg.mouse.get_pos()

        # check collision with button
        if self.top_rect.collidepoint(pos):
            
            # resize to indicate clickable object to user
            self.top_rect.width = self.top_rect_original_width + 3
            self.top_rect.height = self.top_rect_original_height + 3
            self.bot_rect.width = self.top_rect_original_width + 3
            self.bot_rect.height = self.top_rect_original_height + 3

            # if button is clicked (pressed and released) fire function and
            # change elevation to indicate button click to user
            if pg.mouse.get_pressed()[0] and not self.pressed:
                self.dynamic_elevation = 3
                self.pressed = True
                self.function()

            # otherwise, elevation is set to default
            if not pg.mouse.get_pressed()[0]:
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
    def __init__(self, cur, max, pos, height=30, width=200):
        self.cur = cur
        self.max = max
        self.pos = pos
        self.height = height
        self.width = width
        # delcaring the rectangles for display
        self.base_color = "#031d44"
        self.cur_color = "#d6896f"
        self.rect_base = pg.Rect(self.pos, (self.width, self.height))
        self.rect_cur = pg.Rect(self.pos, ((self.cur/self.max)*(self.width-3), self.height-3))
        # declaring the text object to display current values
        self.text = str(cur) + " / " + str(max)
        self.text_surface = UI_font.render(self.text,False,"#bce7fc")
        self.text_rect = self.text_surface.get_rect(center = self.rect_base.center)

    # use the update method to update the max and min health during combat
    def update(self, cur, max):
        self.cur = cur
        self.max = max
        self.rect_cur = pg.Rect(self.pos, ((cur/max)*(self.width-3), self.height-3))
        self.text = str(cur) + " / " + str(max)
        self.text_surface = UI_font.render(self.text,False,"#bce7fc")
        self.text_rect = self.text_surface.get_rect(center = self.rect_base.center)
        pass
        
    def draw(self, surface):
        #drawing the healthbar and current values onto the screen
        pg.draw.rect(surface, self.base_color, self.rect_base, border_radius=4)
        pg.draw.rect(surface, self.cur_color, self.rect_cur, border_radius=4)
        surface.blit(self.text_surface, self.text_rect)


class combatButtons:
    def __init__(self, game):
        self.game = game

    def drawButtons(self, surface):
        screen_width = 800
        screen_height = 600
        exit_color = (255, 0, 0)
        attack_color = (0, 255, 0)
        magic_color = (0, 0, 255)
        button_width, button_height = 75, 50

        exit_button_x, exit_button_y = int(screen_width * 0.8), int(screen_height * 0.68)
        attack_button_x, attack_button_y = int(screen_width * 0.01), int(screen_height * 0.68)
        magic_button_0_x, magic_button_0_y = int(screen_width * 0.16), int(screen_height * 0.68)
        magic_button_1_x, magic_button_1_y = int(screen_width * 0.31), int(screen_height * 0.68)
        magic_button_2_x, magic_button_2_y = int(screen_width * 0.46), int(screen_height * 0.68)
        magic_button_3_x, magic_button_3_y = int(screen_width * 0.61), int(screen_height * 0.68)

        exit_button = pg.Rect(exit_button_x, exit_button_y, button_width, button_height)
        attack_button = pg.Rect(attack_button_x, attack_button_y, button_width, button_height)
        magic_button_0 = pg.Rect(magic_button_0_x, magic_button_0_y, button_width, button_height)
        magic_button_1 = pg.Rect(magic_button_1_x, magic_button_1_y, button_width, button_height)
        magic_button_2 = pg.Rect(magic_button_2_x, magic_button_2_y, button_width, button_height)
        magic_button_3 = pg.Rect(magic_button_3_x, magic_button_3_y, button_width, button_height)

        pg.draw.rect(surface, exit_color, exit_button)
        pg.draw.rect(surface, attack_color, attack_button)
        pg.draw.rect(surface, magic_color, magic_button_0)
        pg.draw.rect(surface, magic_color, magic_button_1)
        pg.draw.rect(surface, magic_color, magic_button_2)
        pg.draw.rect(surface, magic_color, magic_button_3)


def drawHealthBar(health, max_health, res, x, y, width, height):
    health_percent = health / max_health
    pg.draw.rect(res, (255, 0, 0), (x, y, width, height))
    pg.draw.rect(res, (0, 255, 0), (x, y, width * health_percent, height))

def drawManaBar(mana, max_mana, res, x, y, width, height):
    mana_percent = mana / max_mana
    pg.draw.rect(res, (255, 0, 255), (x, y, width, height))
    pg.draw.rect(res, (90, 50, 255), (x, y, width * mana_percent, height))