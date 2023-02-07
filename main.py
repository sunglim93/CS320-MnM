import pygame as pg
import classes as gc
import combat as cm
import pygame as pg
import random as rd
import game
import time

#initializing the game state and such
pg.init()
screen = pg.display.set_mode((800,600))
pg.display.set_caption("Metal & Magic")

#setting the text color and size 
TEXT_COL = ("#bce7fc")
pg.display.flip()
font = pg.font.Font("assets/alagard.ttf",40)

clock = pg.time.Clock()
FPS = 60

#instantiating the game 
game = game.Game()

#method for displaying text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

while game.running():
    state = game.get_state()
    screen.fill(state.getBackground())
    state.loadUI(screen)
    if state.getName() != 'COMBAT':
        draw_text(state.getName(), font, TEXT_COL, 160, 250)
    #event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                game.transitionToMenu()
        state.handleActions(event)
        if state.getName() == 'COMBAT':
            cm.combat()

    clock.tick(FPS)
    pg.display.update()