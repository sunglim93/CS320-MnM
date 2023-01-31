import pygame as pg
import random as rd
import time

class Window:
    def __init__(self, width, height):
        pg.init()
        pg.display.set_caption("Metal & Magic")
        self.width = width
        self.height = height
        size = (self.width, self.height)
        self.res = pg.display.set_mode(size)

class Player:
    def __init__(self, name, x, y, hp, mp, atk, df, magic, weapon):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.df = df
        self.magic = magic
        self.actions = ["Attack", "Magic"]
        self.weapon = weapon
        self.rect = pg.Rect(x, y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"../view/player.png")
        self.size = pg.transform.scale(self.image, (64, 64))

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

    def getMP(self):
        return self.mp

    def getMaxMP(self):
        return self.max_mp

    def drainMP(self, cost):
        self.mp -= cost

    def chooseAction(self):
        i = 1
        print("Actions")
        for item in self.actions:
            print(str(i) + ":", item)
            i += 1

    def chooseMagic(self):
        i = 1
        print("Magic")
        for spell in self.magic:
            print(str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

class Enemy:
    def __init__(self, name, x, y, hp, mp, atk, df, magic):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk = atk
        self.df = df
        self.magic = [Fire("Fire", 20, 100)]
        self.rect = pg.Rect(x, y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"../view/enemy.png")
        self.size = pg.transform.scale(self.image, (128, 128))

    def generateDamage(self):
        return rd.randint(self.atk // 2, self.atk)

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def getHP(self):
        return self.hp

    def getMP(self):
        return self.mp

    def getMaxMP(self):
        return self.max_mp

    def drainMP(self, cost):
        self.mp -= cost

    def enemyAI(self):
        enemy_choice = rd.choice(["Attack", "Magic"])
        if enemy_choice == "Attack":
            return "Attack"
        elif enemy_choice == "Magic" and self.mp >= self.magic[0].cost:
            return "Magic"

class Spell:
    def __init__(self, name, cost, damage, type):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.type = type

    def generateDamage(self):
        low = self.damage - 15
        high = self.damage + 15
        return rd.randrange(low, high)

class Fire(Spell):
    def __init__(self, name, cost, dmg):
        super().__init__(name, cost, dmg, "Fire")
        
class Shock(Spell):
    def __init__(self, name, cost, dmg):
        super().__init__(name, cost, dmg, "Shock")

class KarateKick(Spell):
    def __init__(self, name, cost, dmg):
        super().__init__(name, cost, dmg, "Karate Kick")
        