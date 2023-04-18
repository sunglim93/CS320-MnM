import pygame as pg
import random as rd

class Player:
    """A class representing the main player character in the game."""
    def __init__(self, name, x, y, hp, mp, atk, df, magic, weapon):
        self.name = name
        self.x = x
        self.y = y
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.df = df
        self.magic = magic
        self.actions = ["Attack", "Magic"]
        self.effects = []
        self.weapon = weapon
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"rd/player.png")
        self.size = pg.transform.scale(self.image, (64, 64))

    def drawPlayer(self, surface):
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"rd/player.png")
        self.size = pg.transform.scale(self.image, (64, 64))
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
            print(str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")", "(", spell.spell_type, ")")
            i += 1

    def applyEffect(self, effect=None, effect_strength=None, effect_duration=None):
        self.effects.append({"effect": effect, "strength": effect_strength, "duration": effect_duration})

    def processEffects(self):
        damage_popup = ""
        for effect in self.effects:
            if effect["duration"] != None and effect["duration"] > 0:
                effect["duration"] -= 1
                if effect["effect"] == "Poison":
                    self.hp -= effect["strength"]
                    damage_popup = f"{self.name} takes {effect['strength']} poison damage!"
                if effect["duration"] != None and effect["duration"] <= 0:
                    self.effects.remove(effect)
        return damage_popup

class Enemy:
    """A class representing an enemy character in the game."""
    def __init__(self, name, x, y, hp, mp, atk, df, magic):
        self.name = name
        self.x = x
        self.y = y
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk = atk
        self.df = df
        self.magic = [fire_blast]
        self.effects = []
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"rd/enemy.png")
        self.size = pg.transform.scale(self.image, (128, 128))

    def drawEnemy(self, surface):
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load(f"rd/enemy.png")
        self.size = pg.transform.scale(self.image, (128, 128))
        surface.blit(self.size, self.rect)


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

    def applyEffect(self, effect=None, effect_strength=None, effect_duration=None):
        self.effects.append({"effect": effect, "strength": effect_strength, "duration": effect_duration})

    def processEffects(self):
        damage_popup = ""
        for effect in self.effects:
            if effect["duration"] != None and effect["duration"] > 0:
                effect["duration"] -= 1
                if effect["effect"] == "Poison":
                    self.hp -= effect["strength"]
                    damage_popup = f"{self.name} takes {effect['strength']} poison damage!"
                if effect["duration"] != None and effect["duration"] <= 0:
                    self.effects.remove(effect)
        return damage_popup

    def getEffectsPopUp(self):
        poison_damage_popup = ""
        for effect in self.effects:
            if effect["effect"] == "Poison" and effect["duration"] > 0:
                poison_damage_popup = f"{self.name} takes {effect['strength']} poison damage!"
        return poison_damage_popup

class Spell:
    """A class representing a spell that can be cast by characters in the game."""
    def __init__(self, name, cost, damage, spell_type, effect=None, effect_strength=None, effect_duration=None, is_healing=False):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.spell_type = spell_type
        self.effect = effect
        self.effect_strength = effect_strength
        self.effect_duration = effect_duration
        self.is_healing = is_healing

    def generateDamage(self):
        low = self.damage - 15
        high = self.damage + 15
        dmg = rd.randrange(low, high)
        return dmg

    def isHealing(self):
        return self.is_healing

fire_blast = Spell("Fire Blast", 20, 30, "Flame")
shock_blast = Spell("Shocking Blast", 30, 80, "Electricity")
ice_blast = Spell("Ice Blast", 25, 35, "Ice", effect="Slow", effect_strength=0.5, effect_duration=3)
poison_dart = Spell("Poison Dart", 15, 30, "Poison", effect="Poison", effect_strength=2, effect_duration=5)
healing_light = Spell("Healing Light", 10, 60, "Healing", effect="Heal", is_healing=True)
earthquake = Spell("Earthquake", 50, 80, "Earth", effect="Stun", effect_strength=1, effect_duration=2)
mind_control = Spell("Mind Control", 70, 0, "Psychic", effect="Control", effect_duration=4)
energy_drain = Spell("Energy Drain", 30, 10, "Dark", effect="Drain", effect_strength=5, effect_duration=3)

SPELL_LIST = [
    Spell("Fire Blast", 20, 30, "Flame"),
    Spell("Shocking Blast", 30, 80, "Electricity"),
    Spell("Ice Blast", 25, 35, "Ice", effect="Slow", effect_strength=0.5, effect_duration=3),
    Spell("Poison Dart", 15, 20, "Poison", effect="Poison", effect_strength=2, effect_duration=5),
    Spell("Healing Light", 10, 60, "Healing", effect="Heal", is_healing=True),
    Spell("Earthquake", 50, 80, "Earth", effect="Stun", effect_strength=1, effect_duration=2),
    Spell("Mind Control", 70, 0, "Psychic", effect="Control", effect_duration=4),
    Spell("Energy Drain", 30, 10, "Dark", effect="Drain", effect_strength=5, effect_duration=3)
]

class Item:
    """A class representing an item that can be used by characters in the game."""
    def __init__(self, name, item_type, effect, effect_strength, effect_duration, description):
        self.name = name
        self.item_type = item_type
        self.effect = effect
        self.effect_strength = effect_strength
        self.effect_duration = effect_duration
        self.description = description

    def use(self, target):
        if self.item_type == "healing":
            target.heal(self.effect_strength)
        elif self.item_type == "status":
            target.applyEffect(effect=self.effect, effect_strength=self.effect_strength, effect_duration=self.effect_duration)

class Weapon:
    """A class representing a weapon that can be equipped by characters in the game."""
    def __init__(self, name, weapon_type, atk_bonus, effect=None, effect_strength=None, effect_duration=None):
        self.name = name
        self.weapon_type = weapon_type
        self.atk_bonus = atk_bonus
        self.effect = effect
        self.effect_strength = effect_strength
        self.effect_duration = effect_duration

    def equip(self, target):
        target.atk_low += self.atk_bonus
        target.atk_high += self.atk_bonus

    def unequip(self, target):
        target.atk_low -= self.atk_bonus
        target.atk_high -= self.atk_bonus

class NPC:
    """A class representing a non-player character in the game."""
    def __init__(self, name, x, y, dialogue):
        self.name = name
        self.x = x
        self.y = y
        self.dialogue = dialogue
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((0, 255, 0))
        self.image = pg.image.load(f"rd/npc.png")
        self.size = pg.transform.scale(self.image, (64, 64))

    def drawNPC(self, surface):
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((0, 255, 0))
        self.image = pg.image.load(f"rd/npc.png")
        self.size = pg.transform.scale(self.image, (64, 64))
        surface.blit(self.size, self.rect)

    def interact(self):
        print(self.dialogue)

