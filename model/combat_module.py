import user_interface as ui
import classes as gc
import pygame as pg
import random as rd
import time
import sys
import os

def main():
    window = gc.Window(800,600)

    fire = gc.Fire("Fire", 20, 100)
    shock = gc.Shock("Shock", 30, 125)
    karate_kick = gc.KarateKick("Karate Kick!!!", 50, 200)

    player = gc.Player("Armored Soul", 200, 450, 500, 60, 60, 34, [fire, shock, karate_kick], 'longsword')
    enemy = gc.Enemy("Wretch", 400, 400, 300, 34, 25, 34, [fire])

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        ui.drawHealthBar(player.hp, player.max_hp, window.res, 10, 10, 100, 20)
        ui.drawManaBar(player.mp, player.max_mp, window.res, 10, 40, 100, 20)
        ui.drawHealthBar(enemy.hp, enemy.max_hp, window.res, 680, 10, 100, 20)
        ui.drawManaBar(enemy.mp, enemy.max_mp, window.res, 680, 40, 100, 20)
        window.res.blit(player.size, player.rect)
        window.res.blit(enemy.size, enemy.rect)
        pg.display.update()

        player_choice = input("Choose an action: ")
        if player_choice == "exit":
            running = False
        if player_choice == "1":
            enemy.takeDamage(player.generateDamage())
            print("You attacked the enemy with your " + player.weapon + " and dealt", player.generateDamage(), "damage.")
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

            if player.getMP() >= magic_cost:
                player.drainMP(magic_cost)
                enemy.takeDamage(magic_dmg)
                print("You cast", player.magic[magic_choice].name, "and dealt", magic_dmg, "damage.")
            else:
                print("Not enough MP.")
                continue
        elif player_choice != "exit":
            print("Invalid input.")

        if enemy.getHP() == 0:
            pg.display.update()
            print("You have defeated the enemy.")
            font = pg.font.Font(None, 30)
            text = font.render(enemy.name + " has been defeated! " + player.name + " is Victorious!", True, (255, 0, 0))
            window.res.blit(text, (window.width/2 - 250, window.height/2 + 50))
            pg.display.update()

        else:
            time.sleep(0.5)
            enemy_choice = enemy.enemyAI()
            if enemy_choice == "Attack":
                player.takeDamage(enemy.generateDamage())
                print("The enemy attacked you and dealt", enemy.generateDamage(), "damage.")
            elif enemy_choice == "Magic":
                enemy_magic_cost = fire.cost
                if enemy.getMP() >= enemy_magic_cost:
                    enemy.drainMP(enemy_magic_cost)
                    enemy_magic_dmg = enemy.magic[0].generateDamage()
                    player.takeDamage(enemy_magic_dmg)
                    print("The enemy cast", enemy.magic[0].name, "and dealt", enemy_magic_dmg, "damage.")
                else:
                    player.takeDamage(enemy.generateDamage())
                    print("The enemy attacked you and dealt", enemy.generateDamage(), "damage.")
    pg.quit()

if __name__ == '__main__':
    main()