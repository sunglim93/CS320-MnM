import pygame

class enemy():
  def __init__(self, name, size, color, speed=0.08, x=50, y=50, level=0):
      self.name = name
      self.size = size
      self.color = color
      self.speed = speed
      self.x = x
      self.y = y
      self.level = level

# Initialize pygame
pygame.init()

# Set the screen size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("BlockRunner")

# Set the square's starting position
player_x = 350
player_y = 250

# Set the square's size
player_size = 50

# Set the square's color
player_color = (255, 0, 0)

#Create enemies
bob = enemy('Bob', 25, (0, 255, 0))
moe = enemy('Moe', 25, (255, 255, 0), 0.08, 100, 100)

# Create a dictionary to store the arrow key status
arrow_keys = {
    'left': False,
    'right': False,
    'up': False,
    'down': False
}

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                arrow_keys['left'] = True
            elif event.key == pygame.K_RIGHT:
                arrow_keys['right'] = True
            elif event.key == pygame.K_UP:
                arrow_keys['up'] = True
            elif event.key == pygame.K_DOWN:
                arrow_keys['down'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                arrow_keys['left'] = False
            elif event.key == pygame.K_RIGHT:
                arrow_keys['right'] = False
            elif event.key == pygame.K_UP:
                arrow_keys['up'] = False
            elif event.key == pygame.K_DOWN:
                arrow_keys['down'] = False

    # Create a list of walls
    walls = [
    pygame.Rect(200, 200, 50, 50),
    pygame.Rect(450, 300, 100, 100),
    pygame.Rect(100, 400, 250, 50)
    ]

    # Move the square based on the arrow key status
    if arrow_keys['left']:
        player_x -= 0.5
    if arrow_keys['right']:
        player_x += 0.5
    if arrow_keys['up']:
        player_y -= 0.5
    if arrow_keys['down']:
        player_y += 0.5

    # Check if the square collides with a wall
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for wall in walls:
        if player_rect.colliderect(wall):
            # If collision, move the square back to its previous position
            if arrow_keys['left']:
                player_x += 0.5
            if arrow_keys['right']:
                player_x -= 0.5
            if arrow_keys['up']:
                player_y += 0.5
            if arrow_keys['down']:
                player_y -= 0.5

    # Move the enemy square towards the player square
    if player_x > bob.x:
        bob.x += bob.speed
    if player_x < bob.x:
        bob.x -= bob.speed
    if player_y > bob.y:
        bob.y += bob.speed
    if player_y < bob.y:
        bob.y -= bob.speed

    if player_x > moe.x:
        moe.x += moe.speed
    if player_x < moe.x:
        moe.x -= moe.speed
    if player_y > moe.y:
        moe.y += moe.speed
    if player_y < moe.y:
        moe.y -= moe.speed

    # Check if the enemy square touches the player square
    # Check if the enemy square collides with a wall
    enemy_rect1 = pygame.Rect(bob.x, bob.y, bob.size, bob.size)
    enemy_rect2 = pygame.Rect(moe.x, moe.y, moe.size, moe.size)

    for wall in walls:
        if enemy_rect1.colliderect(wall):
            # If collision, move the enemy square back to its previous position
            if player_x > bob.x:
                bob.x -= 10
                bob.y -= 10
            if player_x < bob.x:
                bob.x += 10
                bob.y -= 10
            if player_y > bob.y:
                bob.y -= 10
                bob.y -= 10
            if player_y < bob.y:
                bob.y += 10
                bob.y -= 10
        if enemy_rect2.colliderect(wall):
            if player_x > moe.x:
                moe.x -= 10
                moe.y -= 10
            if player_x < moe.x:
                moe.x += 10
                moe.y -= 10
            if player_y > moe.y:
                moe.y -= 10
                moe.y -= 10
            if player_y < moe.y:
                moe.y += 10
                moe.y -= 10

    if enemy_rect1.colliderect(player_rect) or enemy_rect2.colliderect(player_rect):
        # If collision, despawn the player square
        player_x = -1
        player_y = -1
        bob.x = 700
        bob.y = 500
        moe.x = 600
        moe.y = 600

    if enemy_rect1.colliderect(enemy_rect2):
        bob.x -= 25
        bob.y -= 25
        moe.x += 25
        moe.y += 25

    # Fill the screen with a background color
    screen.fill((0, 0, 0))

    # Draw the walls on the screen
    for wall in walls:
        pygame.draw.rect(screen, (255,255,255), wall)

    # Draw the player square on the screen
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Draw the enemy square on the screen
    pygame.draw.rect(screen, bob.color, (bob.x, bob.y, bob.size, bob.size))
    pygame.draw.rect(screen, moe.color, (moe.x, moe.y, moe.size, moe.size))
    pygame.display.flip()

# Exit pygame
pygame.quit()

