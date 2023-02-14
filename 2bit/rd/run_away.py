import pygame as pg
import random as rd

pg.init()
screen = pg.display.set_mode((1400, 900))
pg.display.set_caption("Run Away!")

class Player:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.speed = 1
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load('player.png')
        self.size = pg.transform.scale(self.image, (64, 64))

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.x += self.speed
        if keys[pg.K_UP]:
            self.y -= self.speed
        if keys[pg.K_DOWN]:
            self.y += self.speed
        self.rect = pg.Rect(self.x, self.y, 50, 50)

class Enemy:
    def __init__(self):
        self.x = rd.randint(50, 1000)
        self.y = rd.randint(50, 1000)
        self.speed = 0.4
        self.rect = pg.Rect(self.x, self.y, 150, 100)
        self.sprite = pg.Surface((32, 32))
        self.sprite.fill((255, 0, 0))
        self.image = pg.image.load('enemy.png')
        self.size = pg.transform.scale(self.image, (128, 128))

    def move_towards(self, player):
        if player.x > self.x:
            self.x += self.speed
        if player.x < self.x:
            self.x -= self.speed
        if player.y > self.y:
            self.y += self.speed
        if player.y < self.y:
            self.y -= self.speed
        self.rect = pg.Rect(self.x, self.y, 50, 50)

player = Player()
enemy = Enemy()
player_rect = pg.Rect(player.x, player.y, 64, 64)
enemy_rect = pg.Rect(enemy.x, enemy.y, 128, 128)
color_tuple_0 = (rd.randint(1, 254),rd.randint(1, 254),rd.randint(1, 254))
color_tuple_1 = (rd.randint(1, 254),rd.randint(1, 254),rd.randint(1, 254))
color_tuple_2 = (rd.randint(1, 254),rd.randint(1, 254),rd.randint(1, 254))


goal = pg.Rect(1300, 750, 128, 128)
walls = []
for i in range(20):
    wall = pg.Rect(rd.randint(0, 1300), rd.randint(0, 800), 100, 100)
    walls.append(wall)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            player.y -= 5
        if keys[pg.K_DOWN]:
            player.y += 5
        if keys[pg.K_LEFT]:
            player.x -= 5
        if keys[pg.K_RIGHT]:
            player.x += 5

    screen.fill(color_tuple_0)
    for wall in walls:
        pg.draw.rect(screen, (color_tuple_2), (wall[0], wall[1], 100, 100))
        if player.rect.colliderect(wall):
            # If collision, move the square back to its previous position
            if keys[pg.K_UP]:
                player.y += 5
            if keys[pg.K_DOWN]:
                player.y -= 5
            if keys[pg.K_LEFT]:
                player.x += 5
            if keys[pg.K_RIGHT]:
                player.x -= 5
        if enemy.rect.colliderect(wall):
            if player.x > enemy.x:
                enemy.x -= rd.randint(0, 40)
                enemy.y -= rd.randint(-20, 40)
            if player.x < enemy.x:
                enemy.x += rd.randint(0, 40)
                enemy.y -= rd.randint(-20, 40)
            if player.y > enemy.y:
                enemy.y -= rd.randint(0, 40)
                enemy.y -= rd.randint(-20, 40)
            if player.y < enemy.y:
                enemy.y += rd.randint(0, 40)
                enemy.y -= rd.randint(-20, 40)

    if player.rect.colliderect(enemy.rect):
        # If collision, despawn the player square
        player.x = -1
        player.y = -1
        enemy.x = 500
        enemy.y = 500

    pg.draw.rect(screen, (color_tuple_1), (goal[0], goal[1], 100, 100))
    if player.rect.colliderect(goal):
        font = pg.font.Font(None, 100)
        text = font.render("You Won!", True, (255, 255, 255))
        screen.blit(text, (600, 600))
        enemy.speed = 0
            
    player.move()
    enemy.move_towards(player)

    screen.blit(player.size, player.rect)
    screen.blit(enemy.size, enemy.rect)
    pg.display.update()
pg.display.flip()



