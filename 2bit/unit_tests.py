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
        """
        player = gc.Player("Knight", 0, 0, 100, 100, 50, 50, [], None)
        damage = player.generateDamage()
        self.assertTrue(40 <= damage <= 60)

    # Acceptance test
    def testEnemyDmgRange(self):
        """
        Black-box acceptance test for enemy damage range.
        """
        enemy = gc.Enemy("Brigand", 0, 0, 100, 100, 50, 50, [])
        damage = enemy.generateDamage()
        self.assertTrue(25 <= damage <= 50)

    # White-box test
    def testPlayerTakeDmg(self):
        """
        White-box test for player taking damage.
        Coverage: Statement coverage, branch coverage
        Method being tested:
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
        Method being tested:
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
        Method being tested:
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
        Coverage: Statement coverage, branch coverage
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
        Method being tested:
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
        Method being tested:
        def drainMP(self, cost):
            self.mp -= cost
            if self.mp < 0:
                self.mp = 0
        """
        enemy = gc.Enemy("Orc", 0, 0, 100, 100, 50, 50, [])
        enemy.drainMP(30)
        self.assertEqual(enemy.getMP(), 70)

    def testEnemyAI(self):
        # Create an enemy with 0 MP
        enemy = gc.Enemy("Zombie", 0, 0, 300, 60, 25, 34, [gc.Spell("Fire", 20, 100, "Flame")])
        enemy.mp = 0

        # Run enemyAI() and check if the AI chooses to atack
        self.assertEqual(enemy.enemyAI(), "Attack")

    # White-box test
    def testDrawHealthBar(self):
        pg.init()
        window = ui.Window(800, 600, "Test")
        ui.drawHealthBar(50, 100, window.res, 0, 0, 100, 20)
        color = window.res.get_at((10, 10))
        self.assertEqual(color, (0, 255, 0))

    # White-box test
    def testDrawManaBar(self):
        pg.init()
        window = ui.Window(800, 600, "Test")
        ui.drawManaBar(50, 100, window.res, 0, 0, 100, 20)
        color = window.res.get_at((10, 10))
        self.assertEqual(color, (90, 50, 255))

    # White-box test
    def testDisplayPopUp(self):
        pg.init()
        window = ui.Window(800, 600, "Test")
        font = pg.font.Font(None, 30)
        message = "Test Pop Up"
        ui.displayPopUp(window, font, (255, 255, 255), message, 50, 50, 150, 30, 0.5)

class TestEffects(unittest.TestCase):
    def testPoisonEffect(self):
        # Initialize player and enemy
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

if __name__ == "__main__":
    unittest.main()
