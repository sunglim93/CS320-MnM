import random as rd
import pygame as pg

class Player:
    def __init__(self, name, hp=100, atk=20, weapon="rusty dagger"):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.actions = ["Attack"]
        self.items = []
        self.weapon = weapon
        if self.hp < 0:
            self.hp = 0

    def drawPlayer(self, surface, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"assets/player.png")
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
    def __init__(self, name, difficultyMod, hp=150, atk=10, weapon="claws"):
        self.name = name
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
        self.image = pg.image.load(f"assets/bones-0001.png")
        self.size = pg.transform.scale(self.image, (128, 128))
        surface.blit(self.size, self.rect)

    def drawBoss(self, surface, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"assets/purpleBoss.png")
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

