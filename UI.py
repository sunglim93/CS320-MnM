import pygame as pg
import time

class Window:
    """A class for instantiating the game window."""
    def __init__(self, width, height, title):
        pg.init()
        pg.display.set_caption(title)
        self.width = width
        self.height = height
        size = (self.width, self.height)
        self.res = pg.display.set_mode(size)

def drawHealthBar(health, max_health, res, x, y, width, height):
    """A class for instantiating the health bars in combat mode."""
    health_percent = health / max_health
    pg.draw.rect(res, (255, 0, 0), (x, y, width, height))
    pg.draw.rect(res, (0, 100, 0), (x, y, width * health_percent, height))
    health_text = f"{health}/{max_health}"
    font = pg.font.SysFont('arial', 15)
    text = font.render(health_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(x + width / 2, y + height / 2))
    res.blit(text, text_rect)

def drawManaBar(mana, max_mana, res, x, y, width, height):
    """A class for instantiating the mana bars in combat mode."""
    mana_percent = mana / max_mana
    pg.draw.rect(res, (255, 0, 255), (x, y, width, height))
    pg.draw.rect(res, (90, 50, 255), (x, y, width * mana_percent, height))
    mana_text = f"{mana}/{max_mana}"
    font = pg.font.SysFont('arial', 15)
    text = font.render(mana_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(x + width / 2, y + height / 2))
    res.blit(text, text_rect)

def displayPopUp(window, font, text_col, message, x, y, width, height, duration=0.8):
    """A class for instantiating the damage and effect pop-ups in combat mode."""
    popup_rect = pg.Rect(x, y, width, height)
    pg.draw.rect(window.res, (0, 0, 0), popup_rect)
    text = font.render(message, True, text_col)
    window.res.blit(text, (x, y))
    pg.display.update()
    pg.time.wait(int(duration * 1000)) # Convert duration from seconds to milliseconds