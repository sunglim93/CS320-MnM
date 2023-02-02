import pygame
import game

#initializing the game state and such
pygame.init()
screen = pygame.display.set_mode((800,600))

#setting the text color and size 
TEXT_COL = ("#ffffff")
pygame.display.flip()
font = pygame.font.SysFont("arialblack",40)

#instanciating the game 
game = game.Game()

#method for displaying text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

while game.running():
    state = game.get_state()
    screen.fill(state.getBackground())
    draw_text(state.getName(), font, TEXT_COL, 160, 250)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()
        state.handleActions(event)


    pygame.display.update()