"""This is a simple combat module that allows
for testing of basic combat functionality"""

import game_classes as gc
import pygame as pg
import random as rd
import time

def drawHealthBar(health, max_health, x, y, width, height):
    # Calculate the percentage of health remaining
    health_percent = health / max_health
    # Draw the background of the health bar
    pg.draw.rect(screen, (255, 0, 0), (x, y, width, height))
    # Draw the current health as a filled portion of the bar
    pg.draw.rect(screen, (0, 255, 0), (x, y, width * health_percent, height))

def drawManaBar(mana, max_mana, x, y, width, height):
    # Calculate the percentage of health remaining
    mana_percent = mana / max_mana
    # Draw the background of the health bar
    pg.draw.rect(screen, (255, 0, 255), (x, y, width, height))
    # Draw the current health as a filled portion of the bar
    pg.draw.rect(screen, (90, 50, 255), (x, y, width * mana_percent, height))

pg.init()
pg.display.set_caption("Metal & Magic")
# Set up the display
width = 800
height = 600
size = (width, height)
screen = pg.display.set_mode(size)

fire = gc.Fire("Fire", 20, 100)
shock = gc.Shock("Shock", 30, 125)

player = gc.Player("Player", 500, 60, 60, 34, [fire, shock])
enemy = gc.Enemy("Enemy", 400, 34, 25, 34, [fire])

# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Draw the player and enemy
    pg.draw.rect(screen, (0, 0, 255), (width/2-25, height/2-25, 50, 50))
    pg.draw.circle(screen, (255, 0, 0), (width/2+100, height/2), 25)
    drawHealthBar(player.hp, player.max_hp, 10, 10, 100, 20)
    drawManaBar(player.mp, player.max_mp, 10, 40, 100, 20)
    drawHealthBar(enemy.hp, enemy.max_hp, 680, 10, 100, 20)
    drawManaBar(enemy.mp, enemy.max_mp, 680, 40, 100, 20)
    pg.display.update()

    # Get player input
    player_choice = input("Choose an action: ")
    if player_choice == "exit":
        running = False
    if player_choice == "1":
        enemy.takeDamage(player.generateDamage())
        print("You attacked the enemy and dealt", player.generateDamage(), "damage.")
    elif player_choice == "2":
        player.chooseMagic()
        magic_choice = input("Choose a spell: ")
        try:
            magic_choice = int(magic_choice) - 1
            if magic_choice < 0 or magic_choice >= len(player.magic):
                raise ValueError("Invalid spell choice.")
        except ValueError as e:
            print(e)

        magic_dmg = player.magic[magic_choice].generateDamage()
        magic_cost = player.magic[magic_choice].cost
       
        # Check if the player has enough MP to cast the spell
        if player.getMP() >= magic_cost:
            player.drainMP(magic_cost)
            enemy.takeDamage(magic_dmg)
            print("You cast", player.magic[magic_choice].name, "and dealt", magic_dmg, "damage.")
        else:
            print("Not enough MP.")
    elif player_choice != "exit":
        print("Invalid input.")

    # Check if the enemy is still alive
    if enemy.getHP() == 0:
        pg.display.update()
        print("You have defeated the enemy.")
        font = pg.font.Font(None, 30)
        text = font.render("VICTORY!", True, (255, 0, 0))
        screen.blit(text, (width/2 - 50, height/2 + 50)) 
        pg.display.update() 

    else:
        time.sleep(0.5)
        enemy_choice = enemy.enemyAI()
        if enemy_choice == "Attack":
            player.takeDamage(enemy.generateDamage())
            print("The enemy attacked you and dealt", enemy.generateDamage(), "damage.")
        elif enemy_choice == "Magic":
            magic_dmg = enemy.magic[0].generateDamage()
            player.takeDamage(magic_dmg)
            print("The enemy cast", enemy.magic[0].name, "and dealt", magic_dmg, "damage.")

# End the game
pg.quit()
