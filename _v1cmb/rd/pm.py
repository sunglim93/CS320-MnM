import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen size
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("mini-pac")

# Initialize Pac-Man position
pacman_x = 100
pacman_y = 100

# Set wall coordinates
walls = [
    (100, 50, 10, 50),
    (100, 100, 300, 10),  # top horizontal wall
    (100, 200, 150, 10),
    (100, 200, 10, 200),  # left vertical wall
    (390, 200, 10, 200),  # right vertical wall
    (100, 400, 100, 10),  # bottom horizontal wall
]

# Initialize ghost positions
ghosts = [
    (200, 300),
    (250, 200),
    (300, 250),
    (200, 200)
]

# Set game loop flag
running = True

# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move Pac-Man based on key events
    keys = pygame.key.get_pressed()
    pacman_move_x = 0
    pacman_move_y = 0
    if keys[pygame.K_UP]:
        pacman_move_y -= 0.05
    if keys[pygame.K_DOWN]:
        pacman_move_y += 0.05
    if keys[pygame.K_LEFT]:
        pacman_move_x -= 0.05
    if keys[pygame.K_RIGHT]:
        pacman_move_x += 0.05

    # Check for wall collisions
    for wall in walls:
        if pacman_x + 20 > wall[0] and pacman_x < wall[0] + wall[2]:
            if pacman_y + 20 > wall[1] and pacman_y < wall[1] + wall[3]:
                pacman_move_x -= 0.1
                pacman_move_y -= 0.1

    # Update Pac-Man position
    pacman_x += pacman_move_x
    pacman_y += pacman_move_y

    # Keep Pac-Man from leaving the screen
    pacman_x = max(0, min(pacman_x, width - 40))
    pacman_y = max(0, min(pacman_y, height - 40))

    # Fill screen with background color
    screen.fill((0,0,0))

    for i in range(len(ghosts)):
        ghost_x, ghost_y = ghosts[i]
        if pacman_x > ghost_x:
            ghost_x += 0.01
        if pacman_x < ghost_x:
            ghost_x -= 0.01
        if pacman_y > ghost_y:
            ghost_y += 0.01
        if pacman_y < ghost_y:
            ghost_y -= 0.01
        distance_x = pacman_x - ghost_x
        distance_y = pacman_y - ghost_y
        if abs(distance_x) > abs(distance_y):
            ghost_move_x = 0.01 if distance_x > 0 else -0.01
            ghost_move_y = 0
        else:
            ghost_move_y = 0.01 if distance_y > 0 else -0.01
            ghost_move_x = 0
    # Check for wall collisions for each ghost
    for wall in walls:
        if ghost_x + 20 > wall[0] and ghost_x < wall[0] + wall[2]:
            if ghost_y + 20 > wall[1] and ghost_y < wall[1] + wall[3]:
                ghost_move_x = -ghost_move_x
                ghost_move_y = -ghost_move_y
                    
    # Update ghost position
    ghost_x += ghost_move_x
    ghost_y += ghost_move_y
        
    # Keep ghost from leaving the screen
    ghost_x = max(0, min(ghost_x, width - 40))
    ghost_y = max(0, min(ghost_y, height - 40))
        
    # Update ghost coordinates in the list
    ghosts[i] = (ghost_x, ghost_y)

    # Draw each ghost as a red square
    pygame.draw.rect(screen, (255, 0, 0), (ghost_x, ghost_y, 20, 20))

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, ("#1919a6"), wall)

    # Draw Pac-Man as a yellow circle
    pygame.draw.circle(screen, (255, 255, 0), (pacman_x, pacman_y), 20)

    # Update display

    pygame.display.update()

pygame.quit()


