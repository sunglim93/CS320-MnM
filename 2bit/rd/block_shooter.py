import pygame
import random

class Player:
    def __init__(self, x, y, size, color, speed, health):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.health = health
        self.rect = pygame.Rect(x, y, size, size)
        self.projectiles = []
        self.shoot_cooldown = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.projectiles.append(Projectile(self.x + self.size // 2, self.y + self.size // 2, 5, (255, 0, 0), (0, -10)))
            self.shoot_cooldown = 20
        else:
            self.shoot_cooldown -= 1

class Enemy:
    def __init__(self, x, y, size,color, speed, health):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.health = health
        self.rect = pygame.Rect(x, y, size, size)
        self.projectiles = []
        self.shoot_cooldown = 0

    def move(self, player):
        if player.x > self.x:
            self.x += self.speed
        if player.x < self.x:
            self.x -= self.speed
        if player.y > self.y:
            self.y += self.speed
        if player.y < self.y:
            self.y -= self.speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.projectiles.append(Projectile(self.x + self.size // 2, self.y + self.size // 2, 5, (255, 0, 0), (0, -10)))
            self.shoot_cooldown = 20
        else:
            self.shoot_cooldown -= 1

class Projectile:
    def __init__(self, x, y, size, color, velocity):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.velocity = velocity
        self.rect = pygame.Rect(x, y, size, size)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("BlockShooter")
player = Player(350, 250, 50, (255, 0, 0), 1, 100)
enemies = []
for i in range(5):
    enemies.append(Enemy(random.randint(0, 100), random.randint(0, 100), 25, (0, 255, 0), 0.03, 50))

arrow_keys = {
    'left': False,
    'right': False,
    'up': False,
    'down': False
}

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

    # Get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    # Move the player
    player.move(keys)



    # Check if the player wants to shoot
    if keys[pygame.K_SPACE]:
        player.shoot()

    # Move the enemies
    for enemy in enemies:
        enemy.move(player)
        enemy.shoot()

    # Move the projectiles
    for obj in [player, *enemies]:
        for projectile in obj.projectiles:
            projectile.move()

    # Check for collision between projectiles and player/enemies
    for obj in [player, *enemies]:
        for projectile in obj.projectiles:
            for other_obj in [player, *enemies]:
                if obj != other_obj and projectile.rect.colliderect(other_obj.rect):
                    if projectile in obj.projectiles:
                        obj.projectiles.remove(projectile)
                    other_obj.health -= 10

    # Remove dead enemies
    for enemy in enemies:
        if enemy.health <= 0:
            enemies.remove(enemy)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the player and enemies on the screen
    pygame.draw.rect(screen, player.color, player.rect)

    for enemy in enemies:
        pygame.draw.rect(screen, enemy.color, enemy.rect)

    # Draw the projectiles on the screen
    for obj in [player, *enemies]:
        for projectile in obj.projectiles:
            pygame.draw.rect(screen, projectile.color, projectile.rect)

    # Update the screen
    pygame.display.flip()
pygame.quit()