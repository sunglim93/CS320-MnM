import UI as ui
import pygame as pg
import random as rd
import time
import openai
import pygame.freetype
import time

openai.api_key = "YOUR_API_KEY"

def npcCollideWall(new_pos, walls, npc_rect):
    new_npc_rect = npc_rect.copy()
    new_npc_rect.topleft = new_pos
    for wall in walls:
        if new_npc_rect.colliderect(wall):
            return True
    return False

def random_point_within_map(map_size):
    x = rd.randint(0, map_size[0])
    y = rd.randint(0, map_size[1])
    return [x, y]

# def handleTextInput(event, text, font):
#     if event.type == pg.KEYUP:
#         if event.key == pg.K_BACKSPACE:
#             text = text[:-1]
#         elif event.unicode.isprintable():
#             text += event.unicode
#     return text
    
# def generate_npc_dialogue(prompt):
#     completions = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         max_tokens=50,
#         n=1,
#         stop=None,
#         temperature=0.9,
#     )
#     message = completions.choices[0].text.strip()
#     return message
    
class NPC:
    """A class representing a non-player character in the game."""
    def __init__(self, name, x, y, viewport_pos=(0, 0), prompt=''):
        self.name = name
        self.prompt = prompt
        # self.message = generate_npc_dialogue(prompt)
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((0, 255, 0))
        self.image = pg.image.load("assets/npc.png")
        self.size = pg.transform.scale(self.image, (96, 96))
        self.move_timer = pg.time.get_ticks()
        self.viewport_pos = viewport_pos

    def drawNPC(self, surface):
        surface.blit(self.size, (self.x - self.viewport_pos[0], self.y - self.viewport_pos[1]))


    def move_towards_point(self, point, walls, speed=0.33):
        new_pos = [self.x, self.y]
        dx = 0
        dy = 0

        if point[0] > self.x:
            dx = speed
        if point[0] < self.x:
            dx = -speed
        if point[1] > self.y:
            dy = speed
        if point[1] < self.y:
            dy = -speed

        new_pos[0] += dx
        new_pos[1] += dy

        if not npcCollideWall(new_pos, walls, self.rect):
            self.x, self.y = new_pos

class GameState:
    def __init__(self, state_name, state_function):
        self.state_name = state_name
        self.state_function = state_function

    def run(self, *args, **kwargs):
        return self.state_function(*args, **kwargs)

class EM_Rectangle:
    """A class for areas or goal states in the game."""
    def __init__(self, pos, width=300, height=300):
        self.pos = pos
        self.original_pos = pos.copy()
        self.width = width
        self.height = height
        self.rect = pg.Rect(pos[0], pos[1], width, height)

    def collides_with(self, rect):
        return self.rect.colliderect(rect)


class EM_Player:
    """A class to represent the player in exploration mode."""
    def __init__(self):
        self.pos = [200, 300]
        self.speed = 1
        self.rect = pg.Rect(self.pos[0], self.pos[1], 25, 25)
        self.image = pg.image.load('assets/player.png')
        self.size = pg.transform.scale(self.image, (64, 64))
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size.get_width(), self.size.get_height())

class EM_Enemy:
    """A class to represent an enemy in exploration mode."""
    def __init__(self, player_pos, image_path, image):
        self.pos = [player_pos[0]+500, player_pos[1]+500]
        self.speed = 0.33
        self.rect = pg.Rect(self.pos[0], self.pos[1], 25, 25)
        self.image_path = image_path
        self.image = image
        self.size = pg.transform.scale(self.image, (96, 96))
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size.get_width(), self.size.get_height())

    def move_towards(self, player, walls):
        new_pos = self.pos.copy()
        dx = 0
        dy = 0

        if player.pos[0] > self.pos[0]:
            dx = self.speed
        if player.pos[0] < self.pos[0]:
            dx = -self.speed
        if player.pos[1] > self.pos[1]:
            dy = self.speed
        if player.pos[1] < self.pos[1]:
            dy = -self.speed

        new_pos[0] += dx
        if enemyCollideWall(new_pos, walls, self.rect):
            dx = 20*int(rd.choice([-self.speed, self.speed]))
            new_pos[0] = self.pos[0] + dx

        new_pos[1] += dy
        if enemyCollideWall(new_pos, walls, self.rect):
            dy = 20*int(rd.choice([-self.speed, self.speed]))
            new_pos[1] = self.pos[1] + dy

        if not enemyCollideWall(new_pos, walls, self.rect):
            self.pos = new_pos

class Player:
    """A class representing the main player character in the game."""
    def __init__(self, name, x, y, hp, mp, atk, df, magic, weapon, inv=None, bonus_hp=0):
        self.name = name
        self.x = x
        self.y = y
        self.max_hp = hp + bonus_hp
        self.hp = self.max_hp
        self.max_mp = mp
        self.mp = mp
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.df = df
        self.magic = magic
        self.actions = ["Attack", "Magic"]
        self.effects = []
        self.inventory = inv
        self.weapon = weapon
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load("assets/player.png")
        self.size = pg.transform.scale(self.image, (64, 64))

    def drawPlayer(self, surface):
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load("assets/player.png")
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
                    if effect["duration"] % 1 == 0:
                        self.hp -= effect["strength"]
                        damage_popup = f"{self.name} takes {effect['strength']} poison damage!"
            if effect["duration"] != None and effect["duration"] <= 0:
                self.effects.remove(effect)
        return damage_popup

    def useItem(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                item.use(self)
                return True
        return False

    def hasPassiveItem(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                return True
        return False

class Enemy:
    """A class representing an enemy character in the game."""
    def __init__(self, name, x, y, hp, mp, atk, df, magic, image_path, image):
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
        self.image_path = image_path
        self.image = image
        self.size = pg.transform.scale(self.image, (128, 128))

    def drawEnemy(self, surface):
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = select_enemy_image()
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
                    if effect["duration"] % 1 == 0:
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

class Item:
    """A class representing an item that can be used by characters in the game."""
    def __init__(self, name, pos, item_type, effect, effect_strength, effect_duration, description):
        self.name = name
        self.pos = pos
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

fire_blast = Spell("Fire Blast", 20, 50, "Flame")
shock_blast = Spell("Shocking Blast", 30, 80, "Electricity")
ice_blast = Spell("Ice Blast", 25, 35, "Ice", effect="Slow", effect_strength=0.5, effect_duration=3)
poison_dart = Spell("Poison Dart", 15, 40, "Poison", effect="Poison", effect_strength=7, effect_duration=5)
healing_light = Spell("Healing Light", 10, 60, "Healing", effect="Heal", is_healing=True)
earthquake = Spell("Earthquake", 50, 80, "Earth", effect="Stun", effect_strength=1, effect_duration=2)
mind_control = Spell("Mind Control", 70, 0, "Psychic", effect="Control", effect_duration=4)
energy_drain = Spell("Energy Drain", 30, 10, "Dark", effect="Drain", effect_strength=5, effect_duration=3)

SPELL_LIST = [
    Spell("Fire Blast", 20, 50, "Flame"),
    Spell("Shocking Blast", 30, 80, "Electricity"),
    Spell("Ice Blast", 25, 35, "Ice", effect="Slow", effect_strength=0.5, effect_duration=3),
    Spell("Poison Dart", 15, 40, "Poison", effect="Poison", effect_strength=7, effect_duration=5),
    Spell("Healing Light", 10, 60, "Healing", effect="Heal", is_healing=True),
    Spell("Earthquake", 50, 80, "Earth", effect="Stun", effect_strength=1, effect_duration=2),
    Spell("Mind Control", 70, 0, "Psychic", effect="Control", effect_duration=4),
    Spell("Energy Drain", 30, 10, "Dark", effect="Drain", effect_strength=5, effect_duration=3)
]

def createSpells():
    fire_blast = Spell("Fire Blast", 20, 100, "Flame")
    shocking_blast = Spell("Shocking Blast", 30, 125, "Electricity")
    poison_dart = Spell("Poison Dart", 15, 20, "Poison", effect="Poison", effect_strength=7, effect_duration=5)
    healing_light = Spell("Healing Light", 40, 60, "Healing", effect="Heal", is_healing=True)
    return [fire_blast, shocking_blast, poison_dart, healing_light]

def select_enemy_image():
    enemy_index = rd.randint(0, 2)
    enemy_image_path = f'assets/enemy{enemy_index}.png'
    enemy_image = pg.image.load(enemy_image_path).convert_alpha()
    return enemy_image_path, enemy_image

def updateViewportPos(viewport_pos, player, viewport_size):
    viewport_pos[0] = player.pos[0] + player.rect.width / 2 - viewport_size[0] / 2
    viewport_pos[1] = player.pos[1] + player.rect.height / 2 - viewport_size[1] / 2
    return viewport_pos

def keepViewportInMap(viewport_pos, map_size, viewport_size):
    if viewport_pos[0] < 0:
        viewport_pos[0] = 0
    elif viewport_pos[0] > map_size[0] - viewport_size[0]:
        viewport_pos[0] = map_size[0] - viewport_size[0]
    if viewport_pos[1] < 0:
        viewport_pos[1] = 0
    elif viewport_pos[1] > map_size[1] - viewport_size[1]:
        viewport_pos[1] = map_size[1] - viewport_size[1]
    return viewport_pos

def handlePlayerInput(player, keys):
    new_pos = player.pos.copy()
    if keys[pg.K_LEFT]:
        new_pos[0] -= player.speed
    if keys[pg.K_RIGHT]:
        new_pos[0] += player.speed
    if keys[pg.K_UP]:
        new_pos[1] -= player.speed
    if keys[pg.K_DOWN]:
        new_pos[1] += player.speed
    return new_pos

def keepPlayerInMap(player, map_size):
    if player.pos[0] < 0:
        player.pos[0] = 0
    elif player.pos[0] > map_size[0] - player.rect.width:
        player.pos[0] = map_size[0] - player.rect.width
    if player.pos[1] < 0:
        player.pos[1] = 0
    elif player.pos[1] > map_size[1] - player.rect.height:
        player.pos[1] = map_size[1] - player.rect.height
    return player

def drawBackground(window, color_tuple_0):
    window.fill(color_tuple_0)

def drawWalls(window, walls, viewport_pos, color_tuple_1):
    for wall in walls:
        wall_rect = pg.Rect(wall.x - viewport_pos[0], wall.y - viewport_pos[1], wall.width, wall.height)
        window.fill(color_tuple_1, wall_rect)

def updateGoalPos(goal, window_size, viewport_pos):
    goal.pos = [goal.original_pos[0] - viewport_pos[0], goal.original_pos[1] - viewport_pos[1]]
    return goal

def checkPlayerCollideGoal(window, window_size, goal, player, enemy):
    player_rect = pg.Rect(player.pos[0], player.pos[1], player.rect.width, player.rect.height)
    goal_rect = pg.Rect(goal.pos[0], goal.pos[1], goal.width, goal.height)

    if player_rect.colliderect(goal_rect):
        font = pg.font.Font(None, 100)
        TEXT_COL = ("#bce7fc")
        font = pg.font.Font("assets/alagard.ttf", 40)
        text = font.render("ZONE COMPLETE!", True, (255, 255, 255))
        window.blit(text, (window_size[0] // 2 - text.get_width() // 2, window_size[1] // 2 - text.get_height() // 2))
        return True
    return False

def drawMinimap(minimap, map_size, minimap_size, player, enemy, enemy_defeated, walls):
    minimap.fill((0, 0, 0))

    # Draw walls on minimap
    for wall in walls:
        wall_rect_minimap = pg.Rect(wall.x * minimap_size[0] // map_size[0], wall.y * minimap_size[1] // map_size[1],
                                     wall.width * minimap_size[0] // map_size[0], wall.height * minimap_size[1] // map_size[1])
        pg.draw.rect(minimap, (128, 128, 128), wall_rect_minimap)

    # Draw player on minimap
    player_rect_minimap = pg.Rect(player.pos[0] * minimap_size[0] // map_size[0], player.pos[1] * minimap_size[1] // map_size[1], 5, 5)
    pg.draw.rect(minimap, (255, 0, 0), player_rect_minimap)

    # Draw enemy on minimap if not defeated
    if not enemy_defeated:
        enemy_rect_minimap = pg.Rect(enemy.pos[0] * minimap_size[0] // map_size[0], enemy.pos[1] * minimap_size[1] // map_size[1], 5, 5)
        pg.draw.rect(minimap, (0, 0, 255), enemy_rect_minimap)

def createWindow(window_height, window_width):
    return ui.Window(window_height, window_width, "Metal & Magic")

def createButtons(window_width, window_height):
    button_width, button_height = 75, 50
    exit_button_x, exit_button_y = int(window_width * 0.99), int(window_height * 0.68)
    attack_button_x, attack_button_y = int(window_width * 0.01), int(window_height * 0.68)
    magic_button_0_x, magic_button_0_y = int(window_width * 0.16), int(window_height * 0.68)
    magic_button_1_x, magic_button_1_y = int(window_width * 0.31), int(window_height * 0.68)
    magic_button_2_x, magic_button_2_y = int(window_width * 0.46), int(window_height * 0.68)
    magic_button_3_x, magic_button_3_y = int(window_width * 0.61), int(window_height * 0.68)

    exit_button = pg.Rect(exit_button_x, exit_button_y, button_width, button_height)
    attack_button = pg.Rect(attack_button_x, attack_button_y, button_width, button_height)
    magic_button_0 = pg.Rect(magic_button_0_x, magic_button_0_y, button_width, button_height)
    magic_button_1 = pg.Rect(magic_button_1_x, magic_button_1_y, button_width, button_height)
    magic_button_2 = pg.Rect(magic_button_2_x, magic_button_2_y, button_width, button_height)
    magic_button_3 = pg.Rect(magic_button_3_x, magic_button_3_y, button_width, button_height)

    return exit_button, attack_button, magic_button_0, magic_button_1, magic_button_2, magic_button_3

def PlayerCollideWall(new_pos, walls, player_rect):
    new_player_rect = player_rect.copy()
    new_player_rect.topleft = new_pos
    for wall in walls:
        if new_player_rect.colliderect(wall):
            return True
    return False

def enemyCollideWall(new_pos, walls, enemy_rect):
    new_enemy_rect = enemy_rect.copy()
    new_enemy_rect.topleft = new_pos
    for wall in walls:
        if new_enemy_rect.colliderect(wall):
            return True
    return False

def setMapSize(width, height):
    return (width, height)

def setVPSize(width, height):
    return (width, height)

def setVPPos(player, viewport_size):
    return [player.pos[0] - viewport_size[0]/2, player.pos[1] - viewport_size[1]/2]

def createGrid(map_size, wall_size, player, enemy, prob):
    wall_grid = [[0 for _ in range(map_size[0]//wall_size[0])] for _ in range(map_size[1]//wall_size[1])]
    for i in range(map_size[1]//wall_size[1]):
        for j in range(map_size[0]//wall_size[0]):
            if (i, j) == (player.pos[1]//wall_size[1], player.pos[0]//wall_size[0]) or \
                    (i, j) == (enemy.pos[1]//wall_size[1], enemy.pos[0]//wall_size[0]):
                wall_grid[i][j] = 0
            elif i % 2 == 0 and j % 2 == 0 and rd.random() < prob and \
                ((i-1, j) == (player.pos[1]//wall_size[1], player.pos[0]//wall_size[0]) or \
                (i, j+1) == (player.pos[1]//wall_size[1], player.pos[0]//wall_size[0]) or \
                (i-1, j) == (enemy.pos[1]//wall_size[1], enemy.pos[0]//wall_size[0]) or \
                (i, j+1) == (enemy.pos[1]//wall_size[1], enemy.pos[0]//wall_size[0])) :
                wall_grid[i][j] = 0
            elif i % 2 == 0 and j % 2 == 0 and rd.random() < prob:
                wall_grid[i][j] = 1
                if rd.randint(1,2) == 1:
                    wall_grid[i-1][j] = 1
                else:
                    wall_grid[i][j+1] = 1
    return wall_grid

def createWalls(wall_grid, wall_size):
    walls = []
    for i in range(len(wall_grid)):
        for j in range(len(wall_grid[i])):
            if wall_grid[i][j] == 1:
                wall = pg.Rect(j*wall_size[0], i*wall_size[1], wall_size[0], wall_size[1])
                walls.append(wall)
    return walls

def draw_wall_rects(wall_grid, wall_size, minimap, color_tuple):
    for i in range(len(wall_grid)):
        for j in range(len(wall_grid[i])):
            if wall_grid[i][j] == 1:
                wall_rect = pg.Rect(j*wall_size[0]//16, i*wall_size[1]//16, wall_size[0]//16, wall_size[1]//16)
                pg.draw.rect(minimap, color_tuple, wall_rect)

def handleItemObtainment(player, item, item_obtained):
    if not item_obtained:
        item_obtained = True
    return item_obtained

def displayMessage(window, font, color, message, x, y, width, height):
    message_surface = font.render(message, True, color)
    message_rect = message_surface.get_rect()
    message_rect.topleft = (x, y)
    window.blit(message_surface, message_rect)
    pg.display.update(message_rect)

def combat(enemy, enemy_image_path, enemy_image, item_obtained=False):
    """A function to hold combat logic for the combat mode."""
    enemy_defeated = False
    window_width = 800
    window_height = 600
    window = createWindow(window_width, window_height)
    TEXT_COL = ("#bce7fc")
    font = pg.font.Font("assets/alagard.ttf",20)

    fire_blast, shocking_blast, poison_dart, healing_light = createSpells()

    extra_hp_item = Item(name="Helm of Constitution", pos=(window_width - 50, window_height - 50), \
    item_type="healing", effect=None, effect_strength=50, effect_duration=None, description=None)

    if item_obtained:
        player = Player("Armored Soul", (window_width * 0.1), (window_height * 0.75), 400, 120, 60, 34, \
    [fire_blast, shocking_blast, poison_dart, healing_light], 'longsword', extra_hp_item, extra_hp_item.effect_strength)
    else:
        player = Player("Armored Soul", (window_width * 0.1), (window_height * 0.75), 400, 120, 60, 34, \
    [fire_blast, shocking_blast, poison_dart, healing_light], 'longsword')

    enemy = Enemy("Wretch", (window_width * 0.65), (window_height * 0.68), 350, 60, 50, 34, [fire_blast], enemy_image_path, enemy_image)

    exit_button, attack_button, magic_button_0, magic_button_1, \
    magic_button_2, magic_button_3 = createButtons(window_height, window_width)

    exit_color = (255, 0, 0)
    attack_color = (0, 100, 0)
    magic_color = (0, 0, 255)
    clear_text = pg.Rect(0, 100, 800, 200)

    turn = 0
    running = True

    # Combat game loop
    while running:
        player_damage_popup = player.processEffects()
        enemy_damage_popup = enemy.processEffects()
        poison_damage_popup = enemy.getEffectsPopUp()

        if poison_damage_popup:
            ui.displayPopUp(window, font, TEXT_COL, poison_damage_popup, window.width/2 - 250, window.height/2 - 50, 500, 100)

        pg.draw.rect(window.res, exit_color, exit_button)
        pg.draw.rect(window.res, attack_color, attack_button)
        pg.draw.rect(window.res, magic_color, magic_button_0)
        pg.draw.rect(window.res, magic_color, magic_button_1)
        pg.draw.rect(window.res, magic_color, magic_button_2)
        pg.draw.rect(window.res, magic_color, magic_button_3)

        # create button text (janky AF)
        text = font.render('ATK          FB           SB           PD          HL', True, (255, 255, 255))

        # get the position to center the text on the screen
        text_x = window_width // 3.9 - text.get_width() // 2
        text_y = window_height // 1.05 - text.get_height() // 2

        # blit the text surface to the screen
        window.res.blit(text, (text_x, text_y))

        ui.drawHealthBar(player.hp, player.max_hp, window.res, 10, 10, 100, 20)
        ui.drawManaBar(player.mp, player.max_mp, window.res, 10, 40, 100, 20)
        ui.drawHealthBar(enemy.hp, enemy.max_hp, window.res, 680, 10, 100, 20)
        ui.drawManaBar(enemy.mp, enemy.max_mp, window.res, 680, 40, 100, 20)

        player.drawPlayer(window.res)
        window.res.blit(enemy.size, enemy.rect)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if turn == 0:
                if event.type == pg.MOUSEBUTTONUP:
                    mouse_pos = event.pos
                    c = -1
                    if exit_button.collidepoint(mouse_pos):
                        running = False
                        return True
                    elif attack_button.collidepoint(mouse_pos):
                        pg.draw.rect(window.res, (0,0,0), clear_text)
                        dmg = player.generateDamage()
                        enemy.takeDamage(dmg)
                        ui.displayPopUp(window, font, TEXT_COL, "You attacked the " + enemy.name + " with your " + player.weapon + \
                        " and deal " + str(dmg) + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                        turn = 1
                    elif magic_button_0.collidepoint(mouse_pos):
                        c = 0
                    elif magic_button_1.collidepoint(mouse_pos):
                        c = 1
                    elif magic_button_2.collidepoint(mouse_pos):
                        c = 2
                    elif magic_button_3.collidepoint(mouse_pos):
                        c = 3
                    if c >= 0 and c <= 3:
                        magic_choice = player.magic[c]
                        magic_dmg = player.magic[c].generateDamage()
                        magic_cost = player.magic[c].cost
                        heal_bool = player.magic[c].isHealing()
                        if player.magic[c].effect != None:
                            effect_type = player.magic[c].effect
                            effect_strength = player.magic[c].effect_strength
                            effect_duration = player.magic[c].effect_duration
                            if effect_type:
                                enemy.applyEffect(effect_type, effect_strength, effect_duration)
                        if player.getMP() >= magic_cost:
                            player.drainMP(magic_cost)
                            if heal_bool == False:
                                enemy.takeDamage(magic_dmg)
                                ui.displayPopUp(window, font, TEXT_COL, "You cast " + player.magic[c].name + " and deal " \
                                + str(magic_dmg) + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)

                            else:
                                player.heal(magic_dmg)
                                ui.displayPopUp(window, font, TEXT_COL, "You cast " + player.magic[c].name + " and heal for " \
                                + str(magic_dmg) + " health!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            turn = 1
                        else:
                            ui.displayPopUp(window, font, TEXT_COL, "Not enough MP!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            continue
                        ui.drawHealthBar(player.hp, player.max_hp, window.res, 10, 10, 100, 20)
                        ui.drawManaBar(player.mp, player.max_mp, window.res, 10, 40, 100, 20)

                    if turn == 1:
                        time.sleep(0.5)    
                        pg.draw.rect(window.res, (0,0,0), clear_text)
                        if enemy.getHP() <= 0:
                            ui.drawHealthBar(enemy.hp, enemy.max_hp, window.res, 680, 10, 100, 20)
                            ui.drawManaBar(enemy.mp, enemy.max_mp, window.res, 680, 40, 100, 20)
                            ui.displayPopUp(window, font, TEXT_COL, enemy.name + " has been defeated! " + player.name
                            + " is Victorious!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            time.sleep(2.5)
                            running = False
                            return True
                        else:
                            enemy_choice = enemy.enemyAI()
                            if enemy_choice == "Attack":
                                enemy_dmg = enemy.generateDamage()
                                player.takeDamage(enemy_dmg)
                                ui.displayPopUp(window, font, TEXT_COL, "The " + enemy.name + " attacks you and deals " \
                                + str(enemy_dmg) + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            elif enemy_choice == "Magic":
                                enemy_magic_cost = fire_blast.cost
                                if enemy.getMP() >= enemy_magic_cost:
                                    enemy.drainMP(enemy_magic_cost)
                                    enemy_magic_dmg = enemy.magic[0].generateDamage()
                                    player.takeDamage(enemy_magic_dmg)
                                    ui.displayPopUp(window, font, TEXT_COL, enemy.name + " casts "+ enemy.magic[0].name + \
                                    " and deals " + str(enemy_magic_dmg)  + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)

                                else:
                                    enemy_dmg = enemy.generateDamage()
                                    player.takeDamage(enemy_dmg)
                                    ui.displayPopUp(window, font, TEXT_COL, enemy.name + " attacks you and deals "+ str(enemy_dmg) \
                                    + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            ui.drawHealthBar(enemy.hp, enemy.max_hp, window.res, 680, 10, 100, 20)
                            ui.drawManaBar(enemy.mp, enemy.max_mp, window.res, 680, 40, 100, 20)
                        pg.display.update(clear_text)            
                        if player.getHP() == 0:
                            ui.displayPopUp(window, font, TEXT_COL,"GAME OVER!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            time.sleep(2.5)
                        turn = 0
    return True