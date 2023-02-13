import pygame
from pygame.locals import *
from pygame import mixer
import game

#initializing the game state and such
pygame.init()
screen = pygame.display.set_mode((800,600))

#setting the text color and size 
TEXT_COL = ("#bce7fc")
pygame.display.flip()
font = pygame.font.Font("assets/alagard.ttf",40)

clock = pygame.time.Clock()
FPS = 60

#instanciating the game 
game = game.Game()

#method for displaying text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

while game.running():
    state = game.get_state()
    state.loadBackground(screen)
    state.loadUI(screen)
    draw_text(state.getName(), font, TEXT_COL, 160, 250)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.transitionToMenu()
        state.handleActions(event)
  

    clock.tick(FPS)
    pygame.display.update()