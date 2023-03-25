# Satchel Hamilton
# CS 320
# 3/11/2023
# Testing Suite - Combat Functionality
# Tests game files labeled cmbv1, classes, combat_interface.

import unittest
import classes as gc
import combat_interface as ui
import pygame as pg

class TestCombat(unittest.TestCase):
    # Acceptance test
    def testPlayerDmgRange(self):
        """
        Black-box acceptance test for player damage range.
        Coverage: Statement coverage, branch coverage,
        path coverage for generateDamage() method in Player class
        Method tested:
        def generateDamage(self):
            return rd.randrange(self.atk_low, self.atk_high)
        """
        player = gc.Player("Knight", 0, 0, 100, 100, 50, 50, [], None)
        damage = player.generateDamage()
        self.assertTrue(40 <= damage <= 60)

    # Acceptance test
    def testEnemyDmgRange(self):
        """
        Black-box acceptance test for enemy damage range.
        Coverage: Statement coverage, branch coverage,
        path coverage for generateDamage() method in Enemy class
        Method tested:
        def generateDamage(self):
            return rd.randrange(self.atk_low, self.atk_high)
        """
        enemy = gc.Enemy("Brigand", 0, 0, 100, 100, 50, 50, [])
        damage = enemy.generateDamage()
        self.assertTrue(25 <= damage <= 50)

    # White-box test
    def testPlayerTakeDmg(self):
        """
        White-box test for player taking damage.
        Coverage: Statement coverage, branch coverage,  path coverage
        Method tested:
        def takeDamage(self, damage):
            self.hp -= damage
            if self.hp < 0:
                self.hp = 0
        """
        player = gc.Player("Jester", 0, 0, 100, 100, 50, 50, [], None)
        player.takeDamage(20)
        self.assertEqual(player.getHP(), 80)

    # White-box test
    def testEnemyTakeDmg(self):
        """
        White-box test for enemy taking damage.
        Coverage: Statement coverage, branch coverage
        Method tested:
        def takeDamage(self, damage):
            self.hp -= damage
            if self.hp < 0:
                self.hp = 0
        """
        enemy = gc.Enemy("Skeleton", 0, 0, 100, 100, 50, 50, [])
        enemy.takeDamage(30)
        self.assertEqual(enemy.getHP(), 70)

    # White-box test
    def testSpellDmgRange(self):
        """
        White-box test for spell damage range.
        Coverage: Statement coverage, branch coverage
        Method tested:
        def generateDamage(self):
            return random.randrange(self.damage_low, self.damage_high)
        """
        spell = gc.Spell("Fire", 20, 30, "Flame")
        damage = spell.generateDamage()
        self.assertTrue(15 <= damage <= 45)

    # White-box test
    def testPlayerHeal(self):
        """
        White-box test for player healing.
        Coverage: Statement coverage, branch coverage,
        path coverage for the heal() method of the Player class
        Method being tested:
        def heal(self, heal_amount):
            self.hp += heal_amount
            if self.hp > self.maxhp:
                self.hp = self.maxhp
        """
        player = gc.Player("Ranger", 0, 0, 100, 100, 50, 50, [], None)
        player.takeDamage(40)
        player.heal(30)
        self.assertEqual(player.getHP(), 90)

    # White-box test
    def testPlayerDrainMP(self):
        """
        White-box test for player draining MP.
        Coverage: Statement coverage, branch  coverage
        Method tested:
        def drainMP(self, cost):
            self.mp -= cost
            if self.mp < 0:
                self.mp = 0
        """
        player = gc.Player("Knight", 0, 0, 100, 100, 50, 50, [], None)
        player.drainMP(20)
        self.assertEqual(player.getMP(), 80)

    # White-box test
    def testEnemyDrainMP(self):
        """
        White-box test for enemy draining MP.
        Coverage: Statement coverage, branch coverage
        Method tested:
        def drainMP(self, cost):
            self.mp -= cost
            if self.mp < 0:
                self.mp = 0
        """
        enemy = gc.Enemy("Orc", 0, 0, 100, 100, 50, 50, [])
        enemy.drainMP(30)
        self.assertEqual(enemy.getMP(), 70)


     # Acceptance test
    def testEnemyAI(self):
        """
        Black-box test on enemy AI.
        Coverage: Statement coverage, branch coverage
        Method tested:
        def enemyAI(self):
            if self.mp == 0:
                return "Attack"
            if self.hp < self.maxhp * 0.3:
                return "Heal"
            else:
                return "Spell"
        """
        enemy = gc.Enemy("Zombie", 0, 0, 300, 60, 25, 34, [gc.Spell("Fire", 20, 100, "Flame")])
        enemy.mp = 0

        # Run enemyAI() and check if the AI chooses to atack
        self.assertEqual(enemy.enemyAI(), "Attack")

    # White-box test
    def testDrawHealthBar(self):
        """
        White-box test on drawing health bar.
        path coverage for the drawHealthBar() function
        Coverage: Statement coverage, branch coverage,

        Method tested:
        def drawHealthBar(x, y, surface, left, top, width, height):
            health_ratio = left / width
            health_width = health_ratio * width
            health_rect = pg.Rect(left, top, health_width, height)
            pg.draw.rect(surface, (0, 255, 0), health_rect)
        """
        pg.init()
        window = ui.Window(800, 600, "Test")
        ui.drawHealthBar(50, 100, window.res, 0, 0, 100, 20)
        color = window.res.get_at((10, 10))
        self.assertEqual(color, (0, 255, 0))

    # White-box test
    def testDrawManaBar(self):
        """
        White-box test on drawing  bar.
        Coverage: Statement coverage, branch coverage,
        path coverage for the drawManaBar() function
        Method tested:
        def drawManaBar(x, y, surface, left, top, width, height):
            mana_ratio = left / width
            mana_width = mana_ratio * width
            mana_rect = pg.Rect(left, top, mana_width, height)
            pg.draw.rect(surface, (90, 50, 255), mana_rect)
        """
        pg.init()
        window = ui.Window(800, 600, "Test")
        ui.drawManaBar(50, 100, window.res, 0, 0, 100, 20)
        color = window.res.get_at((10, 10))
        self.assertEqual(color, (90, 50, 255))

    # White-box test
    def testDisplayPopUp(self):
        """
        White-box test on displaying a pop-up.
        Coverage: Statement coverage, branch coverage
        Method tested:
        def displayPopUp(window, font, color, message, x, y, width, height, duration):
            surf = pg.Surface((width, height))
            surf.set_alpha(200)
            surf.fill((255, 255, 255))
            rect = surf.get_rect()
            rect.x, rect.y = x, y
            window.draw(surf, rect)
            txt = font.render(message, True, color)
            txt_rect = txt.get_rect(center=surf.get_rect().center)
            surf.blit(txt, txt_rect)
            pg.display.flip()
            pg.time.wait(int(duration * 1000))
        """
        pg.init()
        window = ui.Window(800, 600, "Test")
        font = pg.font.Font(None, 30)
        message = "Test Pop Up"
        ui.displayPopUp(window, font, (255, 255, 255), message, 50, 50, 150, 30, 0.5)

class TestEffects(unittest.TestCase):
    # White-box test
    def testPoisonEffect(self):
        """
        White-box test for poison effect.
        Coverage: Statement coverage, branch coverage
        Method being tested:
        def applyEffect(self, effect, strength, duration):
        self.effects[effect] = (strength, duration)
        """
        player = gc.Player("Bard", 0, 0, 100, 100, 50, 50, [], None)
        enemy = gc.Enemy("Dwarf", 0, 0, 100, 100, 50, 50, [])
        
        # Get Poison Dart spell
        poison_dart = gc.Spell("Poison Dart", 15, 20, "Poison", effect="Poison", effect_strength=2, effect_duration=5)
        
        # Apply poison effect to the enemy
        enemy.applyEffect(poison_dart.effect, poison_dart.effect_strength, poison_dart.effect_duration)
        
        # Simulate turns and ensures enemy is poisoned for  5 turns
        initial_hp = enemy.getHP()
        for turn in range(5):
            enemy.processEffects()  # Assuming process_effects() method in the Enemy class handles effects
            self.assertTrue(enemy.isPoisoned())  # Assuming is_poisoned() method in the Enemy class
            self.assertLess(enemy.getHP(), initial_hp)
            initial_hp = enemy.getHP()
        
        # After 5 turns poison effect should dissipate 
        enemy.processEffects()
        self.assertFalse(enemy.isPoisoned())
        self.assertEqual(enemy.getHP(), initial_hp)

class TestIntegration(unittest.TestCase):
    # Intergration Test
    def setUp(self):
        """
        Set up test objects for integration tests: player, enemy, and spells.
        This method tests the Player, Enemy, and Spell classes.
        The testing approach is big-bang since we are testing multiple units together.
        """
        self.fire = gc.Spell("Fire", 20, 100, "Flame")
        self.shock = gc.Spell("Shock", 30, 125, "Electricity")
        self.poison_dart = gc.Spell("Poison Dart", 15, 20, "Poison", effect="Poison", effect_strength=2, effect_duration=5)
        self.healing_light = gc.Spell("Healing Light", 40, 60, "Healing", effect="Heal", is_healing=True)
        self.player = gc.Player("Armored Soul", 100, 100, 400, 120, 60, 34, \
                                [self.fire, self.shock, self.poison_dart, self.healing_light], 'longsword')
        self.enemy = gc.Enemy("Wretch", 200, 100, 300, 60, 25, 34, [self.fire])

    # Intergration Test
    def test_player_attack_enemy(self):
        """
        Test if player's attack successfully reduces the enemy's HP.
        This method tests the integration of Player and Enemy classes through the attack process using a big-bang approach.
        """
        initial_enemy_hp = self.enemy.getHP()
        dmg = self.player.generateDamage()
        self.enemy.takeDamage(dmg)
        final_enemy_hp = self.enemy.getHP()
        self.assertEqual(initial_enemy_hp - dmg, final_enemy_hp)

    # Intergration Test
    def test_enemy_attack_player(self):
        """
        Test if enemy's attack successfully reduces the player's HP.
        This method tests the integration of Player and Enemy classes through the attack process using a big-bang approach.
        """
        initial_player_hp = self.player.getHP()
        enemy_dmg = self.enemy.generateDamage()
        self.player.takeDamage(enemy_dmg)
        final_player_hp = self.player.getHP()
        self.assertEqual(initial_player_hp - enemy_dmg, final_player_hp)

    # Intergration Test
    def test_player_cast_spell_on_enemy(self):
        """
        Test if player's spell casting successfully reduces the enemy's HP and drains the player's MP.
        This method tests the integration of Player, Enemy, and Spell classes through the spell casting process using a big-bang approach.
        """
        spell = self.fire
        initial_enemy_hp = self.enemy.getHP()
        initial_player_mp = self.player.getMP()
        magic_dmg = spell.generateDamage()
        magic_cost = spell.cost
        self.player.drainMP(magic_cost)
        self.enemy.takeDamage(magic_dmg)
        final_enemy_hp = self.enemy.getHP()
        final_player_mp = self.player.getMP()
        self.assertEqual(initial_enemy_hp - magic_dmg, final_enemy_hp)
        self.assertEqual(initial_player_mp - magic_cost, final_player_mp)

if __name__ == "__main__":
    unittest.main()
