import pygame as pg
import time

class Window:
    def __init__(self, width, height, title):
        pg.init()
        pg.display.set_caption(title)
        self.width = width
        self.height = height
        size = (self.width, self.height)
        self.res = pg.display.set_mode(size)
        
def drawHealthBar(health, max_health, res, x, y, width, height):
    health_percent = health / max_health
    pg.draw.rect(res, (255, 0, 0), (x, y, width, height))
    pg.draw.rect(res, (0, 255, 0), (x, y, width * health_percent, height))

def drawManaBar(mana, max_mana, res, x, y, width, height):
    mana_percent = mana / max_mana
    pg.draw.rect(res, (255, 0, 255), (x, y, width, height))
    pg.draw.rect(res, (90, 50, 255), (x, y, width * mana_percent, height))

def displayPopUp(window, font, text_col, message, x, y, width, height, duration=1.2):
    popup_rect = pg.Rect(x, y, width, height)
    pg.draw.rect(window.res, (0, 0, 0), popup_rect)
    text = font.render(message, True, text_col)
    window.res.blit(text, (x, y))
    pg.display.update()
    time.sleep(duration)