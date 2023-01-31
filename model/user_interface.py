import pygame as pg

def drawHealthBar(health, max_health, res, x, y, width, height):
    health_percent = health / max_health
    pg.draw.rect(res, (255, 0, 0), (x, y, width, height))
    pg.draw.rect(res, (0, 255, 0), (x, y, width * health_percent, height))

def drawManaBar(mana, max_mana, res, x, y, width, height):
    mana_percent = mana / max_mana
    pg.draw.rect(res, (255, 0, 255), (x, y, width, height))
    pg.draw.rect(res, (90, 50, 255), (x, y, width * mana_percent, height))