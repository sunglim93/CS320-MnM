import pygame as pg
import random as rd

# Initialize pg and set screen size
pg.init()
screen_size = (800, 600)
screen = pg.display.set_mode(screen_size)

class Player:
    def __init__(self):
        self.pos = [200, 300]
        self.speed = 1
        self.rect = pg.Rect(self.pos[0], self.pos[1], 25, 25)
        self.image = pg.image.load('player.png')
        self.size = pg.transform.scale(self.image, (64, 64))
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size.get_width(), self.size.get_height())

player = Player()

# Set map size
map_size = (4000, 4000)

# Set viewport size (size of the smaller window that follows the player)
viewport_size = (800, 600)

# Set viewport starting position (centered on the player)
viewport_pos = [player.pos[0] - viewport_size[0]/2, player.pos[1] - viewport_size[1]/2]

# Set wall size
wall_size = (100, 100)
# Create grid of wall positions
wall_grid = [[0 for _ in range(map_size[0]//wall_size[0])] for _ in range(map_size[1]//wall_size[1])]

# Fill grid with walls
prob = 0.5
for i in range(map_size[1]//wall_size[1]):
    for j in range(map_size[0]//wall_size[0]):
        if i % 2 == 0 and j % 2 == 0 and rd.random()<prob:
            wall_grid[i][j] = 1
            if rd.randint(1,2) == 1:
                wall_grid[i-1][j] = 1
            else:
                wall_grid[i][j+1] = 1

# Convert grid to list of wall rectangles
walls = []
for i in range(len(wall_grid)):
    for j in range(len(wall_grid[i])):
        if wall_grid[i][j] == 1:
            wall = pg.Rect(j*wall_size[0], i*wall_size[1], wall_size[0], wall_size[1])
            walls.append(wall)

player_rect = pg.Rect(player.pos[0], player.pos[1], player.size.get_width(), player.size.get_height())

# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player.pos[0] -= 10
    if keys[pg.K_RIGHT]:
        player.pos[0] += 10
    if keys[pg.K_UP]:
        player.pos[1] -= 10
    if keys[pg.K_DOWN]:
        player.pos[1] += 10

    # Keep player within map boundaries
    if player.pos[0] < 0:
        player.pos[0] = 0
    elif player.pos[0] > map_size[0] - player.rect.width:
        player.pos[0] = map_size[0] - player.rect.width
    if player.pos[1] < 0:
        player.pos[1] = 0
    elif player.pos[1] > map_size[1] - player.rect.height:
        player.pos[1] = map_size[1] - player.rect.height

    # Keep viewport centered on player
    viewport_pos = [player.pos[0] + player.rect.width/2 - viewport_size[0]/2, player.pos[1] + player.rect.height/2 - viewport_size[1]/2]

    # Keep viewport within map boundaries
    if viewport_pos[0] < 0:
        viewport_pos[0] = 0
    elif viewport_pos[0] > map_size[0] - viewport_size[0]:
        viewport_pos[0] = map_size[0] - viewport_size[0]
    if viewport_pos[1] < 0:
        viewport_pos[1] = 0
    elif viewport_pos[1] > map_size[1] - viewport_size[1]:
        viewport_pos[1] = map_size[1] - viewport_size[1]

    # Draw background
    screen.fill((255, 255, 255))

    # Draw walls
    for wall in walls:
        wall_rect = pg.Rect(wall.x - viewport_pos[0], wall.y - viewport_pos[1], wall.width, wall.height)
        screen.fill((0, 0, 0), wall_rect)

    # Draw player
    player.rect.topleft = player.pos
    screen.blit(player.size, player.rect)

    # Update viewport
    pg.display.update()

pg.quit()
