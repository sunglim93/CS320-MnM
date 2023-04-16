import random as rd
import pygame as pg
from view import UIElements as ui

class Player:
    def __init__(self, name, g, hp=100, atk=20):
        self.image = ui.adapt_image('assets/player.png', g.getPalette())
        self.name = name
        self.max_hp = hp
        self.hp = hp
        # weapon gets an attack item whick controls the atk values
        self.weapon = ("Attack", "Rusty Dagger", [atk])
        # item1 and item2 get defense or consumables, start out empty
        self.item1 = None
        self.item2 = None
        self.atk = self.weapon[2][0]
        self.atk_low = self.atk - 10
        self.atk_high = self.atk + 10
        self.actions = ["Attack"]
        if self.hp < 0:
            self.hp = 0

    def removeItem(self, pos):
        # sets extra items to None
        if pos == 1:
            self.item1 = None
        if pos == 2:
            self.item2 = None

    def addItem(self, pos, item):
        # attack item goes in weapon slot, change attack values
        if item[0] == "Attack":
            self.weapon = item
            self.atk = item[2][0]
            self.atk_low = item[2][0]-10
            self.atk_high = item[2][0]+10
        #if item[0] == "Defense":
        # other items go in pos 1 or 2
        elif pos == 1:
            self.item1 = item
        elif pos == 2:
            self.item2 = item

    def resetPlayer(self):
        # restore hp to full
        self.setHP()
        # reset weapon to original and remove extra items
        self.removeItem(1)
        self.removeItem(2)
        self.weapon = ("Active", "Rusty Dagger", [20])
        self.atk_low = 10
        self.atk_high = 30

    def drawPlayer(self, surface, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.size = pg.transform.scale(self.image, (128, 128))
        surface.blit(self.size, self.rect)

    def generateDamage(self):
        return rd.randrange(self.atk_low, self.atk_high)

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, heal_amt):
        self.hp += heal_amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def getHP(self):
        return self.hp

    def getMaxHP(self):
        return self.max_hp

    def chooseAction(self):
        i = 1
        print("Actions")
        for item in self.actions:
            print(str(i) + ":", item)
            i += 1
    
    def setHP(self):
        self.hp = self.max_hp

class Enemy:
    def __init__(self, name, difficultyMod, palette, hp=150, atk=10, weapon="claws"):
        self.palette = palette
        self.name = name
        self.image = ui.adapt_image("assets/bones-0001.png",palette)
        self.max_hp = int(hp*difficultyMod) #modify hp and atk according to difficulty
        self.hp = self.max_hp
        self.atk = int(atk*difficultyMod)
        self.atk_low = atk - 5
        self.atk_high = atk + 5
        self.actions = ["Attack"]
        self.weapon = weapon

    def drawEnemy(self, surface, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.size = pg.transform.scale(self.image, (128, 128))
        surface.blit(self.size, self.rect)

    def drawBoss(self, surface, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = ui.adapt_image("assets/greenBoss_smol.png",self.palette)
        self.size = pg.transform.scale(self.image, (128, 128))
        surface.blit(self.size, self.rect)

    def generateDamage(self):
        return rd.randrange(self.atk_low, self.atk_high)

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, heal_amt):
        self.hp += heal_amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def getHP(self):
        return self.hp

    def getMaxHP(self):
        return self.max_hp

    def chooseAction(self):
        i = 1
        print("Actions")
        for item in self.actions:
            print(str(i) + ":", item)
            i += 1

