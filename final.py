import pygame as pg
import random as rd
import combat_interface as ui
import classes as gc
import pygame as pg
import random as rd
import time

window_width = 800
window_height = 600

class Rectangle:
    """A class for areas or goal states in the game."""
    def __init__(self, pos):
        self.pos = pos
        self.rect = pg.Rect(pos[0], pos[1], 300, 300)

    def collides_with(self, rect):
        return self.rect.colliderect(rect)

class Player:
    """A class to represent the player in exploration mode."""
    def __init__(self):
        self.pos = [200, 300]
        self.speed = 1
        self.rect = pg.Rect(self.pos[0], self.pos[1], 25, 25)
        self.image = pg.image.load('assets/player.png')
        self.size = pg.transform.scale(self.image, (64, 64))
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size.get_width(), self.size.get_height())

class Enemy:
    """A class to represent an enemy in exploration mode."""
    def __init__(self, player_pos):
        self.pos = [player_pos[0]+500, player_pos[1]+500]
        self.speed = 0.28
        self.rect = pg.Rect(self.pos[0], self.pos[1], 25, 25)
        self.image = pg.image.load('assets/enemy.png')
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
    goal.pos = [window_size[0] - 300 - viewport_pos[0], window_size[1] - 300 - viewport_pos[1]]
    return goal

def checkPlayerCollideGoal(window, window_size, goal, player, enemy):
    if goal.collides_with(player.rect):
        font = pg.font.Font(None, 100)
        TEXT_COL = ("#bce7fc")
        font = pg.font.Font("alagard.ttf", 40)
        text = font.render("ZONE COMPLETE!", True, (255, 255, 255))
        window.blit(text, (window_size[0] // 2 - text.get_width() // 2, window_size[1] // 2 - text.get_height() // 2))
        return True
    return False

def drawMinimap(minimap, map_size, minimap_size, player, enemy):
    player_rect_minimap = pg.Rect(player.pos[0] * minimap_size[0] // map_size[0], player.pos[1] * minimap_size[1] // map_size[1], 5, 5)
    pg.draw.rect(minimap, (255, 0, 0), player_rect_minimap)

    enemy_rect_minimap = pg.Rect(enemy.pos[0] * minimap_size[0] // map_size[0], enemy.pos[1] * minimap_size[1] // map_size[1], 5, 5)
    pg.draw.rect(minimap, (0, 0, 255), enemy_rect_minimap)

def createWindow(window_height, window_width):
    return ui.Window(window_height, window_width, "Metal & Magic")

def createSpells():
    fire_blast = gc.Spell("Fire Blast", 20, 100, "Flame")
    shocking_blast = gc.Spell("Shocking Blast", 30, 125, "Electricity")
    poison_dart = gc.Spell("Poison Dart", 15, 20, "Poison", effect="Poison", effect_strength=2, effect_duration=5)
    healing_light = gc.Spell("Healing Light", 40, 60, "Healing", effect="Heal", is_healing=True)
    return [fire_blast, shocking_blast, poison_dart, healing_light]

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


def combat(enemy):
    """A function to hold combat logic for the combat mode."""
    enemy_defeated = False
    window_width = 800
    window_height = 600

    window = createWindow(window_width, window_height)
    TEXT_COL = ("#bce7fc")
    font = pg.font.Font("alagard.ttf",20)

    fire_blast, shocking_blast, poison_dart, healing_light = createSpells()

    player = gc.Player("Armored Soul", (window_width * 0.1), (window_height * 0.75), 400, 120, 60, 34, \
    [fire_blast, shocking_blast, poison_dart, healing_light], 'longsword')
    enemy = gc.Enemy("Wretch", (window_width * 0.65), (window_height * 0.68), 300, 60, 25, 34, [fire_blast])

    exit_button, attack_button, magic_button_0, magic_button_1, \
    magic_button_2, magic_button_3 = createButtons(window_height, window_width)

    exit_color = (255, 0, 0)
    attack_color = (0, 255, 0)
    magic_color = (0, 0, 255)
    clear_text = pg.Rect(0, 100, 800, 200)

    turn = 0
    running = True
    enemy_defeated = False

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

                    if turn == 1:
                        time.sleep(1.2)    
                        pg.draw.rect(window.res, (0,0,0), clear_text)
                        if enemy.getHP() == 0:
                            ui.displayPopUp(window, font, TEXT_COL, enemy.name + " has been defeated! " + player.name
                            + " is Victorious!", window.width/2 - 250, window.height/2 - 50, 500, 100)
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

                        pg.display.update(clear_text)            
                        if player.getHP() == 0:
                            ui.displayPopUp(window, font, TEXT_COL,"GAME OVER!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                        turn = 0
    return enemy_defeated
    

# Initialize pg and set window size
pg.init()
window_size = (1200, 800)
window = pg.display.set_mode(window_size)

minimap_size = (200, 150)
minimap = pg.Surface(minimap_size)

# Set random colors
color_tuple_0 = (rd.randint(1, 254),rd.randint(1, 254),rd.randint(1, 254))
color_tuple_1 = (rd.randint(1, 254),rd.randint(1, 254),rd.randint(1, 254))
color_tuple_2 = (rd.randint(1, 254),rd.randint(1, 254),rd.randint(1, 254))

player = Player()
enemy = Enemy(player.pos)
goal = Rectangle([window_size[0] - 300, window_size[1] - 300])
player_rect = pg.Rect(player.pos[0], player.pos[1], player.size.get_width(), player.size.get_height())
enemy_rect = pg.Rect(player.pos[0], player.pos[1], player.size.get_width(), player.size.get_height())

# Set map size
map_size = setMapSize(4000, 4000)

# Set viewport size (size of the smaller window that follows the player)
viewport_size = setVPSize(800, 600)

# Set viewport starting position (centered on the player)
viewport_pos = setVPPos(player, viewport_size)

# Set wall size
wall_size = (100, 100)

# Create grid of wall positions
prob = 0.4
wall_grid = createGrid(map_size, wall_size, player, enemy, prob)

# Convert grid to list of walls
walls = createWalls(wall_grid, wall_size)

# Draw wall rectangles on minimap
color_tuple_2 = (rd.randint(1, 254),rd.randint(1, 254),rd.randint(1, 254))
draw_wall_rects(wall_grid, wall_size, minimap, color_tuple_2)


# Main game loop
running = True
combat_mode = False
goal_reached = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    goal_reached = checkPlayerCollideGoal(window, window_size, goal, player, enemy)
    # Update viewport position
    viewport_pos = updateViewportPos(viewport_pos, player, viewport_size)
    viewport_pos = keepViewportInMap(viewport_pos, map_size, viewport_size)

    # Handle player input
    keys = pg.key.get_pressed()
    new_pos = handlePlayerInput(player, keys)

    if not PlayerCollideWall(new_pos, walls, player.rect):
        player.pos = new_pos

    player = keepPlayerInMap(player, map_size)

    # Draw game elements
    drawBackground(window, color_tuple_0)
    drawWalls(window, walls, viewport_pos, color_tuple_1)

    # Update goal position
    goal = updateGoalPos(goal, window_size, viewport_pos)

    # Check if player collided with the goal
    zone_complete = checkPlayerCollideGoal(window, window_size, goal, player, enemy)

    player.rect.topleft = (player.pos[0] - viewport_pos[0], player.pos[1] - viewport_pos[1])
    enemy.rect.topleft = (enemy.pos[0] - viewport_pos[0], enemy.pos[1] - viewport_pos[1])

    # Draw minimap
    drawMinimap(minimap, map_size, minimap_size, player, enemy)

    # Update display and handle events
    enemy_defeated = False
    if not zone_complete:
        # check for collision between player and enemy
        if pg.sprite.collide_rect(player, enemy) and enemy_defeated == False:
            combat_mode = True

        if combat_mode == True and enemy_defeated == False:
            despawn_enemy = combat(enemy)
            if despawn_enemy:
                enemy_defeated = True
                combat_mode = False

        # Move the enemy towards the player and avoid walls
        enemy.move_towards(player, walls)
    else:
        enemy.speed = 0

    window.blit(minimap, (window_size[0]-minimap_size[0]-10, 10))
    window.blit(player.size, player.rect)

    if not enemy_defeated:
        window.blit(enemy.size, enemy.rect)

    # Move the enemy towards the player and avoid walls
    enemy.move_towards(player, walls)

    # Update the display
    pg.display.update()

pg.quit()

