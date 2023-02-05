import pygame
pygame.font.init()
UI_font = pygame.font.Font("assets/alagard.ttf",30)


def default_action():
    print("no action was assigned to button")

class Button():
    def __init__(self,text, width, height, pos, elevation=6, function=default_action):
        self.pressed = False
        self.top_rect = pygame.Rect(pos, (width, height))
        self.bot_rect = pygame.Rect(pos, (width, height))
        self.top_rect_original_width = width
        self.top_rect_original_height = height
        self.top_color = "#dab785"
        self.bot_color = "#d6896f"
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]
        self.text = text
        self.text_surface = UI_font.render(text,False,"#00060e")
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)
        self.function = function

    def draw(self, surface):
        #elevation logic
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        pygame.draw.rect(surface, self.bot_color, self.bot_rect, border_radius=4)
        pygame.draw.rect(surface,self.top_color,self.top_rect, border_radius=4)
        surface.blit(self.text_surface, self.text_rect)
        self.check_click()

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(pos):
            self.top_rect.width = self.top_rect_original_width + 3
            self.top_rect.height = self.top_rect_original_height + 3
            self.bot_rect.width = self.top_rect_original_width + 3
            self.bot_rect.height = self.top_rect_original_height + 3
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.dynamic_elevation = 3
                self.pressed = True
                self.function()
            if not pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = self.elevation
                self.pressed = False
        else:
            self.top_rect.width = self.top_rect_original_width
            self.top_rect.height = self.top_rect_original_height
            self.bot_rect.width = self.top_rect_original_width
            self.bot_rect.height = self.top_rect_original_height            
            self.dynamic_elevation = self.elevation
            UI_font.set_italic(False)
