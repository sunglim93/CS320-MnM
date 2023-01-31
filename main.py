import pygame
import game_state

pygame.init()
screen = pygame.display.set_mode((800,600))
TEXT_COL = ("#ffffff")
pygame.display.flip()

game = game_state.Game()
font = pygame.font.SysFont("arialblack",40)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

running = True
while running:
    screen.fill(game.get_color())
    draw_text(game.get_name(), font, TEXT_COL, 160, 250)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.set_state(game.state_change())
            elif event.key == pygame.K_ESCAPE:
                game.set_state(0)
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()