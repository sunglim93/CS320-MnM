import pygame as pg
import random as rd

# Initialize pg and set screen size
pg.init()
screen_size = (1600, 900)
screen = pg.display.set_mode(screen_size)
attack_range = 20  # Attack range for the player

class Enemy:
    def __init__(self, player, walls):
        self.pos = [100, 100]  # initial position
        self.speed = 0.5  # movement speed
        self.image = pg.image.load("enemy.png")
        self.size = pg.transform.scale(self.image, (64, 64))
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size.get_width(), self.size.get_height())
        self.player = player
        self.walls = walls
        self.hit_count = 0  # Initialize hit count
        self.is_active = True  # Enemy is active by default

    def update(self):
        if self.hit_count >= 4:  # Despawn enemy if hit count >= 4
            return

        # Calculate distance between enemy and player
        dx = self.player.pos[0] - self.pos[0]
        dy = self.player.pos[1] - self.pos[1]
        dist = (dx**2 + dy**2)**0.5

        # Move enemy in direction of player
        if dist > 0:
            dx /= dist
            dy /= dist
            new_pos = [self.pos[0] + dx * self.speed, self.pos[1] + dy * self.speed]

            # Check for wall collisions
            if not collides_with_wall(new_pos, self.walls, self.rect):
                self.pos = new_pos
                self.rect.topleft = (self.pos[0], self.pos[1])
            else:
                # Handle wall collisions
                bump_dir = rd.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                self.pos[0] += bump_dir[0] * (10 * self.speed)
                self.pos[1] += bump_dir[1] * (10 * self.speed)
                self.rect.topleft = (self.pos[0], self.pos[1])

    def draw(self, screen, viewport_pos):
        if self.hit_count >= 4:  # Do not draw enemy if hit count >= 4
            return

        # Draw enemy on screen
        enemy_rect = pg.Rect(self.pos[0] - viewport_pos[0], self.pos[1] - viewport_pos[1], self.size.get_width(), self.size.get_height())
        screen.blit(self.size, enemy_rect)

    def is_hit(self, attack_rect):
        if self.rect.colliderect(attack_rect):
            self.hit_count += 1
            if self.hit_count >= 4:
                self.is_active = False
            else:
                self.is_active = True
        else:
            self.is_active = True  # Make sure the enemy remains active if not hit

class Player:
    def __init__(self):
        self.pos = [200, 300]
        self.speed = 1
        self.image = pg.image.load("player.png")
        self.size = pg.transform.scale(self.image, (64, 64))
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size.get_width(), self.size.get_height())
    
    def attack(self):
        attack_rect = pg.Rect(self.pos[0] - attack_range, self.pos[1], self.rect.width + attack_range, self.rect.height)
        return attack_rect

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

def collides_with_wall(new_pos, walls, player_rect):
    new_player_rect = player_rect.copy()
    new_player_rect.topleft = new_pos
    for wall in walls:
        if new_player_rect.colliderect(wall):
            return True
    return False

enemy = Enemy(player, walls)  # create enemy instance

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Handle player input
    keys = pg.key.get_pressed()
    new_pos = player.pos.copy()
    if keys[pg.K_LEFT]:
        new_pos[0] -= player.speed
        player.facing = 'left'
    if keys[pg.K_RIGHT]:
        new_pos[0] += player.speed
        player.facing = 'right'
    if keys[pg.K_UP]:
        new_pos[1] -= player.speed
        player.facing = 'up'
    if keys[pg.K_DOWN]:
        new_pos[1] += player.speed
        player.facing = 'down'

    # Check if player collides with walls
    if not collides_with_wall(new_pos, walls, player.rect):
        player.pos = new_pos

    # Keep player within map boundaries
    if player.pos[0] < 0:
        player.pos[0] = 0
    elif player.pos[0] > map_size[0] - player.rect.width:
        player.pos[0] = map_size[0] - player.rect.width
    if player.pos[1] < 0:
        player.pos[1] = 0
    elif player.pos[1] > map_size[1] - player.rect.height:
        player.pos[1] = map_size[1] - player.rect.height

    # Update player rect
    player.rect.topleft = (player.pos[0], player.pos[1])

    # Update enemy
    if enemy.is_active:
        enemy.update()

    # Update viewport position to be centered around the player
    viewport_pos[0] = player.pos[0] + player.rect.width / 2 - viewport_size[0] / 2
    viewport_pos[1] = player.pos[1] + player.rect.height / 2 - viewport_size[1] / 2

    # Keep viewport within map boundaries
    if viewport_pos[0] < 0:
        viewport_pos[0] = 0
    elif viewport_pos[0] > map_size[0] - viewport_size[0]:
        viewport_pos[0] = map_size[0] - viewport_size[0]
    if viewport_pos[1] < 0:
        viewport_pos[1] = 0
    elif viewport_pos[1] > map_size[1] - viewport_size[1]:
        viewport_pos[1] = map_size[1] - viewport_size[1]

    # if keys[pg.K_SPACE]:
    #     attack_rect = player.attack()
    #     enemy.is_hit(attack_rect)

    # Draw background
    screen.fill((255, 255, 255))

    # Draw walls
    for wall in walls:
        wall_rect = pg.Rect(wall.x - viewport_pos[0], wall.y - viewport_pos[1], wall.width, wall.height)
        screen.fill((0, 0, 0), wall_rect)

    if enemy.is_active:
        enemy.draw(screen, viewport_pos)

    player.rect.topleft = (player.pos[0] - viewport_pos[0], player.pos[1] - viewport_pos[1])
    screen.blit(player.size, player.rect)
    pg.display.update()

pg.quit()
