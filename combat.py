from view import combat_interface as ui
import classes as gc
import pygame as pg
import random as rd
import time

def combat():
    screen_width = 600
    screen_height = 800
    window = ui.Window(screen_height, screen_width, "Metal & Magic")
    TEXT_COL = ("#bce7fc")
    font = pg.font.Font("assets/alagard.ttf",20)

    fire = gc.Fire("Fire", 20, 100)
    shock = gc.Shock("Shock", 30, 125)
    karate_kick = gc.KarateKick("Karate Kick", 50, 200)
    psionic_storm = gc.PsionicStorm("Psionic Storm", 100, 600)

    player = gc.Player("Armored Soul", (screen_width * 0.3), (screen_height * 0.51), 400, 120, 60, 34, \
    [fire, shock, karate_kick, psionic_storm], 'longsword')
    enemy = gc.Enemy("Wretch", (screen_width * 0.8), (screen_height * 0.45), 300, 60, 25, 34, [fire])

    button_width, button_height = 75, 50
    exit_button_x, exit_button_y = int(screen_width * 0.8), int(screen_height * 0.68)
    attack_button_x, attack_button_y = int(screen_width * 0.01), int(screen_height * 0.68)
    magic_button_0_x, magic_button_0_y = int(screen_width * 0.16), int(screen_height * 0.68)
    magic_button_1_x, magic_button_1_y = int(screen_width * 0.31), int(screen_height * 0.68)
    magic_button_2_x, magic_button_2_y = int(screen_width * 0.46), int(screen_height * 0.68)
    magic_button_3_x, magic_button_3_y = int(screen_width * 0.61), int(screen_height * 0.68)

    exit_button = pg.Rect(exit_button_x, exit_button_y, button_width, button_height)
    attack_button = pg.Rect(attack_button_x, attack_button_y, button_width, button_height)
    magic_button_0 = pg.Rect(magic_button_0_x, magic_button_0_y, button_width, button_height)
    magic_button_1 = pg.Rect(magic_button_1_x, magic_button_1_y, button_width, button_height)
    magic_button_2 = pg.Rect(magic_button_2_x, magic_button_2_y, button_width, button_height)
    magic_button_3 = pg.Rect(magic_button_3_x, magic_button_3_y, button_width, button_height)

    exit_color = (255, 0, 0)
    attack_color = (0, 255, 0)
    magic_color = (0, 0, 255)

    clear_text = pg.Rect(0, 100, 800, 200)

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

        player.drawPlayer(window.res)
        window.res.blit(enemy.size, enemy.rect)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if turn == 0:
                if event.type == pg.MOUSEBUTTONUP:
                    mouse_pos = event.pos
                    c = -1
                    if exit_button.collidepoint(mouse_pos):
                        running = False
                    elif attack_button.collidepoint(mouse_pos):
                        pg.draw.rect(window.res, (0,0,0), clear_text)
                        dmg = player.generateDamage()
                        enemy.takeDamage(dmg)
                        text = font.render("You attacked the " + enemy.name + " with your " + player.weapon + \
                        " and deal " + str(dmg) + " damage!", True, TEXT_COL)
                        window.res.blit(text, (window.width/2 - 350, window.height/2 + -50))
                        pg.display.update()
                        turn = 1
                    elif magic_button_0.collidepoint(mouse_pos):
                        c = 0
                    elif magic_button_1.collidepoint(mouse_pos):
                        c = 1
                    elif magic_button_2.collidepoint(mouse_pos):
                        c = 2
                    elif magic_button_3.collidepoint(mouse_pos):
                        c = 3
                    if c >= 0 and c <= 3:
                        magic_choice = player.magic[c]
                        magic_dmg = player.magic[c].generateDamage()
                        magic_cost = player.magic[c].cost
                        if player.getMP() >= magic_cost:
                            player.drainMP(magic_cost)
                            enemy.takeDamage(magic_dmg)
                            pg.draw.rect(window.res, (0,0,0), clear_text)
                            text = font.render("You cast " + player.magic[c].name + " and deal " \
                            + str(magic_dmg) + " damage!", True, TEXT_COL)
                            window.res.blit(text, (window.width/2 - 250, window.height/2 - 50))
                            pg.display.update()
                            turn = 1
                        else:
                            pg.draw.rect(window.res, (0,0,0), clear_text)
                            text = font.render("Not enough MP!", True, TEXT_COL)
                            window.res.blit(text, (window.width/2 - 250, window.height/2 - 50))
                            pg.display.update()
                            continue

            if turn == 1:
                time.sleep(1.2)
                pg.draw.rect(window.res, (0,0,0), clear_text)
                if enemy.getHP() == 0:
                    text = font.render(enemy.name + " has been defeated! " + player.name
                    + " is Victorious!", True, TEXT_COL)
                    window.res.blit(text, (window.width/2 - 250, window.height/2 - 50))
                else:
                    enemy_choice = enemy.enemyAI()
                    if enemy_choice == "Attack":
                        enemy_dmg = enemy.generateDamage()
                        player.takeDamage(enemy_dmg)
                        text = font.render("The " + enemy.name + " attacks you and deals " + str(enemy_dmg) \
                        + " damage!", True, TEXT_COL)
                        window.res.blit(text, (window.width/2 - 250, window.height/2 - 50))
                    elif enemy_choice == "Magic":
                        enemy_magic_cost = fire.cost
                        if enemy.getMP() >= enemy_magic_cost:
                            enemy.drainMP(enemy_magic_cost)
                            enemy_magic_dmg = enemy.magic[0].generateDamage()
                            player.takeDamage(enemy_magic_dmg)
                            text = font.render(enemy.name + " casts "+ enemy.magic[0].name + \
                            " and deals " + str(enemy_magic_dmg)  + " damage!", True, TEXT_COL)
                            window.res.blit(text, (window.width/2 - 250, window.height/2 - 50))
                        else:
                            enemy_dmg = enemy.generateDamage()
                            player.takeDamage(enemy_dmg)
                            text = font.render(enemy.name + " attacks you and deals "+ str(enemy_dmg) \
                            + " damage!", True, TEXT_COL)
                            window.res.blit(text, (window.width/2 - 250, window.height/2 - 50))
                pg.display.update(clear_text)            
                if player.getHP() == 0:
                    text = font.render("GAME OVER!", True, TEXT_COL)
                    window.res.blit(text, (window.width/2 - 20, window.height/2 - 90))
                pg.display.update(clear_text)
                turn = 0

    pg.quit()
