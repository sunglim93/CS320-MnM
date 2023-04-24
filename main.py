import pygame as pg
import UI as ui
import classes as gc
import random as rd

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

# Initialize exploration mode objects
player = gc.EM_Player()
enemy = gc.EM_Enemy(player.pos)
goal = gc.EM_Rectangle([window_size[0] - 300, window_size[1] - 300])

# Initiallize combat state
combat_state = gc.GameState("combat", gc.combat)  

player_rect = pg.Rect(player.pos[0], player.pos[1], player.size.get_width(), player.size.get_height())
enemy_rect = pg.Rect(player.pos[0], player.pos[1], player.size.get_width(), player.size.get_height())

extra_hp_item = gc.Item(name="Helm of Constitution", pos=(window_size[0] - 50, window_size[1] - 50), item_type="healing", effect=None, effect_strength=50, effect_duration=None, description="Grants the player 50 extra hit points.")

item_image = pg.image.load("assets/chest.png")
item_sprite = pg.transform.scale(item_image, (32, 32))
item_rect = pg.Rect(extra_hp_item.pos[0], extra_hp_item.pos[1], 32, 32)
item_list = []
item_list = extra_hp_item

# Set map size
map_size = gc.setMapSize(4000, 4000)

# Set viewport size (size of the smaller window that follows the player)
viewport_size = gc.setVPSize(800, 600)

# Set viewport starting position (centered on the player)
viewport_pos = gc.setVPPos(player, viewport_size)

# Set wall size
wall_size = (100, 100)

# Create grid of wall positions
prob = 0.4
wall_grid = gc.createGrid(map_size, wall_size, player, enemy, prob)

# Convert grid to list of walls
walls = gc.createWalls(wall_grid, wall_size)

# Draw wall rectangles on minimap
gc.draw_wall_rects(wall_grid, wall_size, minimap, color_tuple_2)

# Retain exploration mode aspect ratio
original_window_size = window_size
original_minimap_size = minimap_size

# Set booleans
running = True
combat_mode = False
goal_reached = False
enemy_defeated = False  
item_obtained = False

item_obtained_message = f"Item obtained: {extra_hp_item.name}!"
message_duration = 1200  # 1.2 seconds
message_timer = pg.USEREVENT + 1

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == message_timer:
            gc.display_message(window, pg.font.Font("assets/alagard.ttf", 40), (0, 0, 0), item_obtained_message, window_size[0]//2 - 150, window_size[1]//2 - 50, 300, 100)
            pg.time.set_timer(message_timer, 0)  # Stop the timer
            pg.time.delay(message_duration)  # Wait for the message to be displayed for the specified duration
            pg.display.update((window_size[0]//2 - 150, window_size[1]//2 - 50, 300, 100))  # Update the message area

    # Update viewport position
    viewport_pos = gc.updateViewportPos(viewport_pos, player, viewport_size)
    viewport_pos = gc.keepViewportInMap(viewport_pos, map_size, viewport_size)

    # Handle player input
    keys = pg.key.get_pressed()
    new_pos = gc.handlePlayerInput(player, keys)

    if not gc.PlayerCollideWall(new_pos, walls, player.rect):
        player.pos = new_pos

    player = gc.keepPlayerInMap(player, map_size)

    # Draw game elements
    gc.drawBackground(window, color_tuple_0)
    gc.drawWalls(window, walls, viewport_pos, color_tuple_1)

    # Update goal position
    goal = gc.updateGoalPos(goal, window_size, viewport_pos)

    # Check if player collided with the goal
    zone_complete = gc.checkPlayerCollideGoal(window, window_size, goal, player, enemy)

    # Keep objects synced with viewport
    item_rect.topleft = (extra_hp_item.pos[0] - viewport_pos[0], extra_hp_item.pos[1] - viewport_pos[1])
    player.rect.topleft = (player.pos[0] - viewport_pos[0], player.pos[1] - viewport_pos[1])
    enemy.rect.topleft = (enemy.pos[0] - viewport_pos[0], enemy.pos[1] - viewport_pos[1])

    # Draw minimap
    gc.drawMinimap(minimap, map_size, minimap_size, player, enemy, enemy_defeated, walls)

    # Check for item collision and handle item obtainment
    if player.rect.colliderect(item_rect) and not item_obtained:
        item_rect = pg.Rect(-100, -100, 32, 32)
        item_obtained = True
        pg.time.set_timer(message_timer, message_duration)

    # Display item to screen
    if not item_obtained:
        window.blit(item_sprite, (extra_hp_item.pos[0] - viewport_pos[0], extra_hp_item.pos[1] - viewport_pos[1]))

    # Check for collision between player and enemy
    if pg.sprite.collide_rect(player, enemy) and enemy_defeated == False:
        combat_mode = True

    if combat_mode == True and enemy_defeated == False:
        original_window_size = window_size  # Store the original window size before combat
        original_minimap_size = minimap_size  # Store the original minimap size before combat
        if item_obtained == True:
             enemy_defeated = gc.combat(enemy, item_list, True)
        else:
             enemy_defeated = gc.combat(enemy, False)

        combat_mode = False  # Set combat_mode to False and return to exploration mode
        window_size = original_window_size  # Restore the original window size
        minimap_size = original_minimap_size  
        window = pg.display.set_mode(window_size)

    if not enemy_defeated:
        enemy.move_towards(player, walls)
        window.blit(enemy.size, enemy.rect)

    window.blit(minimap, (window_size[0]-minimap_size[0]-10, 10))
    window.blit(player.size, player.rect)

    if player.rect.colliderect(item_rect) and not item_obtained:
        item_rect = pg.Rect(-100, -100, 32, 32)
        item_obtained = gc.handle_item_obtainment(player, extra_hp_item, item_obtained)

    pg.display.update()

pg.quit()
