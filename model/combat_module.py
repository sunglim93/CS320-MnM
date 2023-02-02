import user_interface as ui
import classes as gc
import pygame as pg
import random as rd
import time
import sys
import os

def main():
    window = gc.Window(800,600)
    font = pg.font.Font(None, 30)
    pg.display.set_caption("Metal & Magic")

    fire = gc.Fire("Fire", 20, 100)
    shock = gc.Shock("Shock", 30, 125)
    karate_kick = gc.KarateKick("Karate Kick!!!", 50, 200)
    psionic_storm = gc.PsionicStorm("Psionic Storm", 100, 600)

    player = gc.Player("Armored Soul", 200, 450, 500, 120, 60, 34, [fire, shock, karate_kick, psionic_storm], 'longsword')
    enemy = gc.Enemy("Wretch", 400, 400, 300, 34, 25, 34, [fire])

    exit_button = pg.Rect(700, 550, 75, 50)
    attack_button = pg.Rect(50, 550, 75, 50)
    magic_button_0 = pg.Rect(150, 550, 75, 50)
    magic_button_1 = pg.Rect(250, 550, 75, 50)
    magic_button_2 = pg.Rect(350, 550, 75, 50)
    magic_button_3 = pg.Rect(450, 550, 75, 50)

    exit_color = (255, 0, 0)
    attack_color = (0, 255, 0)
    magic_color = (0, 0, 255)

    clear_text = pg.Rect(0, 100, 800, 300)

    turn = 0
    running = True
    while running:

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

        window.res.blit(player.size, player.rect)
        window.res.blit(enemy.size, enemy.rect)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if turn == 0:
                if event.type == pg.MOUSEBUTTONUP:
                    mouse_pos = event.pos
                    if exit_button.collidepoint(mouse_pos):
                        running = False
                    elif attack_button.collidepoint(mouse_pos):
                        pg.draw.rect(window.res, (0,0,0), clear_text)
                        dmg = player.generateDamage()
                        enemy.takeDamage(dmg)
                        text = font.render("You attacked the enemy with your " + player.weapon + \
                        " and dealt " + str(dmg) + " damage.", True, (255, 0, 0))
                        window.res.blit(text, (window.width/2 - 350, window.height/2 + 50))
                        pg.display.update()
                        turn = 1
                    else:
                        if magic_button_0.collidepoint(mouse_pos):
                            c = 0
                        if magic_button_1.collidepoint(mouse_pos):
                            c = 1
                        if magic_button_2.collidepoint(mouse_pos):
                            c = 2
                        if magic_button_3.collidepoint(mouse_pos):
                            c = 3
                        if c >= 0 and c <= 3:
                            magic_choice = player.magic[c]
                            magic_dmg = player.magic[c].generateDamage()
                            magic_cost = player.magic[c].cost
                            if player.getMP() >= magic_cost:
                                player.drainMP(magic_cost)
                                enemy.takeDamage(magic_dmg)
                                pg.draw.rect(window.res, (0,0,0), clear_text)
                                text = font.render("You cast " + player.magic[c].name + " and dealt " \
                                + str(magic_dmg) + " damage.", True, (255, 0, 0))
                                window.res.blit(text, (window.width/2 - 250, window.height/2 + 50))
                                pg.display.update()
                                turn = 1
                            else:
                                pg.draw.rect(window.res, (0,0,0), clear_text)
                                text = font.render("Not enough MP.", True, (255, 0, 0))
                                window.res.blit(text, (window.width/2 - 250, window.height/2 + 50))
                                pg.display.update()
                                continue

            if turn == 1:
                time.sleep(1.2)
                if enemy.getHP() == 0:
                    pg.draw.rect(window.res, (0,0,0), clear_text)
                    text = font.render(enemy.name + " has been defeated! " + player.name
                    + " is Victorious!", True, (255, 0, 0))
                    window.res.blit(text, (window.width/2 - 250, window.height/2 + 50))
                    pg.display.update()
                    turn = 0
                else:
                    enemy_choice = enemy.enemyAI()
                    if enemy_choice == "Attack":
                        pg.draw.rect(window.res, (0,0,0), clear_text)
                        enemy_dmg = enemy.generateDamage()
                        player.takeDamage(enemy_dmg)
                        text = font.render("The enemy attacked you and dealt " + str(enemy_dmg) \
                        + " damage.", True, (255, 0, 0))
                        window.res.blit(text, (window.width/2 - 250, window.height/2 + 50))
                        pg.display.update()
                        turn = 0
                    elif enemy_choice == "Magic":
                        pg.draw.rect(window.res, (0,0,0), clear_text)
                        enemy_magic_cost = fire.cost
                        if enemy.getMP() >= enemy_magic_cost:
                            pg.draw.rect(window.res, (0,0,0), clear_text)
                            enemy.drainMP(enemy_magic_cost)
                            enemy_magic_dmg = enemy.magic[0].generateDamage()
                            player.takeDamage(enemy_magic_dmg)
                            text = font.render(enemy.name + " casts "+ enemy.magic[0].name + " and deals " + str(enemy_magic_dmg) \
                            + " damage.", True, (255, 0, 0))
                            window.res.blit(text, (window.width/2 - 250, window.height/2 + 50))
                            pg.display.update()
                            turn = 0
                        else:
                            pg.draw.rect(window.res, (0,0,0), clear_text)
                            enemy_dmg = enemy.generateDamage()
                            player.takeDamage(enemy_dmg)
                            text = font.render(enemy.name + " attacked you and dealt "+ str(enemy_dmg) \
                            + " damage.", True, (255, 0, 0))
                            window.res.blit(text, (window.width/2 - 250, window.height/2 + 50))
                            pg.display.update()
                            turn = 0

    pg.quit()

if __name__ == '__main__':
    main()