import combat_interface as ui
import classes as gc
import pygame as pg
import random as rd
import time

def combat():

    screen_width = 600
    screen_height = 800
    
    window = ui.Window(screen_height, screen_width, "Metal & Magic")
    TEXT_COL = ("#bce7fc")
    font = pg.font.Font("alagard.ttf",20)

    fire = gc.Spell("Fire", 20, 100, "Flame")
    shock = gc.Spell("Shock", 30, 125, "Electricity")
    poison_dart = gc.Spell("Poison Dart", 15, 20, "Poison", effect="Poison", effect_strength=2, effect_duration=5)
    healing_light = gc.Spell("Healing Light", 40, 60, "Healing", effect="Heal", is_healing=True)

    player = gc.Player("Armored Soul", (screen_width * 0.3), (screen_height * 0.51), 400, 120, 60, 34, \
    [fire, shock, poison_dart, healing_light], 'longsword')

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
        player_damage_popup = player.processEffects()
        enemy_damage_popup = enemy.processEffects()
        poison_damage_popup = enemy.getEffectsPopUp()

        if poison_damage_popup:
            ui.displayPopUp(window, font, TEXT_COL, poison_damage_popup, window.width/2 - 250, window.height/2 - 50, 500, 100)

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
                        ui.displayPopUp(window, font, TEXT_COL, "You attacked the " + enemy.name + " with your " + player.weapon + \
                        " and deal " + str(dmg) + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)
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
                        heal_bool = player.magic[c].isHealing()
                        if player.magic[c].effect != None:
                            effect_type = player.magic[c].effect
                            effect_strength = player.magic[c].effect_strength
                            effect_duration = player.magic[c].effect_duration
                            if effect_type:
                                enemy.applyEffect(effect_type, effect_strength, effect_duration)
                        if player.getMP() >= magic_cost:
                            player.drainMP(magic_cost)
                            if heal_bool == False:
                                enemy.takeDamage(magic_dmg)
                                ui.displayPopUp(window, font, TEXT_COL, "You cast " + player.magic[c].name + " and deal " \
                                + str(magic_dmg) + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)

                            else:
                                player.heal(magic_dmg)
                                ui.displayPopUp(window, font, TEXT_COL, "You cast " + player.magic[c].name + " and heal for " \
                                + str(magic_dmg) + " health!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            turn = 1
                        else:
                            ui.displayPopUp(window, font, TEXT_COL, "Not enough MP!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                            continue

            if turn == 1:
                time.sleep(0.8)    
                pg.draw.rect(window.res, (0,0,0), clear_text)
                if enemy.getHP() == 0:
                    ui.displayPopUp(window, font, TEXT_COL, enemy.name + " has been defeated! " + player.name
                    + " is Victorious!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                else:
                    enemy_choice = enemy.enemyAI()
                    if enemy_choice == "Attack":
                        enemy_dmg = enemy.generateDamage()
                        player.takeDamage(enemy_dmg)
                        ui.displayPopUp(window, font, TEXT_COL, "The " + enemy.name + " attacks you and deals " \
                        + str(enemy_dmg) + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                    elif enemy_choice == "Magic":
                        enemy_magic_cost = fire.cost
                        if enemy.getMP() >= enemy_magic_cost:
                            enemy.drainMP(enemy_magic_cost)
                            enemy_magic_dmg = enemy.magic[0].generateDamage()
                            player.takeDamage(enemy_magic_dmg)
                            ui.displayPopUp(window, font, TEXT_COL, enemy.name + " casts "+ enemy.magic[0].name + \
                            " and deals " + str(enemy_magic_dmg)  + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)

                        else:
                            enemy_dmg = enemy.generateDamage()
                            player.takeDamage(enemy_dmg)
                            ui.displayPopUp(window, font, TEXT_COL, enemy.name + " attacks you and deals "+ str(enemy_dmg) \
                            + " damage!", window.width/2 - 250, window.height/2 - 50, 500, 100)

                pg.display.update(clear_text)            
                if player.getHP() == 0:
                    ui.displayPopUp(window, font, TEXT_COL,"GAME OVER!", window.width/2 - 250, window.height/2 - 50, 500, 100)
                turn = 0

    pg.quit()

combat()