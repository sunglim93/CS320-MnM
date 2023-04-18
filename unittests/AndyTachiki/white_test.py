import unittest
from unittest.mock import MagicMock, patch

from game import Game
from model.classes import Player, Enemy
from model import item, classes, game_states

# coverage run -m unittest test_white
from model.game_states import Reward


class TestPlayer(unittest.TestCase):

    def testDamage(self):
        """Unit testing the damage method for the player - White-box"""
        p = Player("AAA")
        self.assertEqual(p.hp, 100)
        p.takeDamage(10)
        self.assertEqual(p.hp, 90)
        p.takeDamage(10)
        self.assertEqual(p.hp, 80)
        p.takeDamage(100)
        self.assertEqual(p.hp, 0)

    def testHeal(self):
        """Unit testing the heal method for the player - White-box"""
        p = Player("AAA")
        self.assertEqual(p.hp, 100)
        p.heal(50)
        self.assertEqual(p.hp, 100)
        p.hp = 50
        self.assertEqual(p.hp, 50)
        p.heal(50)
        self.assertEqual(p.hp, 100)


"""  model\classes.py: 44% coverage

    def __init__(self, name, hp=100, atk=20, weapon="rusty dagger"):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.actions = ["Attack"]
        self.items = []
        self.weapon = weapon
        if self.hp < 0:
            self.hp = 0

    def generateDamage(self):
        return rd.randrange(self.atk_low, self.atk_high)

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, heal_amt):
        self.hp += heal_amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp    

"""


class TestEnemy(unittest.TestCase):

    def testDamage(self):
        """Unit testing the damage method for the enemy - White-box"""
        p = Enemy("AAA", 1)
        self.assertEqual(p.hp, 150)
        p.takeDamage(10)
        self.assertEqual(p.hp, 140)
        p.takeDamage(10)
        self.assertEqual(p.hp, 130)
        p.takeDamage(150)
        self.assertEqual(p.hp, 0)

    def testHeal(self):
        """Unit testing the heal method for the enemy - White-box"""
        p = Enemy("AAA", 1)
        self.assertEqual(p.hp, 150)
        p.heal(50)
        self.assertEqual(p.hp, 150)
        p.hp = 50
        self.assertEqual(p.hp, 50)
        p.heal(50)
        self.assertEqual(p.hp, 100)
        p.heal(50)
        self.assertEqual(p.hp, 150)
        p.heal(50)
        self.assertEqual(p.hp, 150)


""" model\classes.py: 41% coverage

class Enemy:
    def __init__(self, name, difficultyMod, hp=150, atk=10, weapon="claws"):
        self.name = name
        self.max_hp = int(hp*difficultyMod) #modify hp and atk according to difficulty
        self.hp = self.max_hp
        self.atk = int(atk*difficultyMod)
        self.atk_low = atk - 5
        self.atk_high = atk + 5
        self.actions = ["Attack"]
        self.weapon = weapon

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, heal_amt):
        self.hp += heal_amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp
"""


class TestHeal(unittest.TestCase):
    """"Integration test, testing the player's heal mechanic following damage taken. One relies on the other through
        a bottom-up procedure."""

    def testPlayerHealAfterAttack(self):
        p = Player("AAA")
        self.assertEqual(p.hp, 100)
        p.takeDamage(50)
        self.assertEqual(p.hp, 50)
        p.heal(50)
        self.assertEqual(p.hp, 100)
        p.heal(50)
        self.assertEqual(p.hp, 100)

    def testEnemyHealAfterAttack(self):
        """"Integration test, testing the enemies heal mechanic following damage taken. One relies on the other like it
            did for the Player. This is also done through a bottom-up procedure like the enemy"""

        p = Enemy("AAA", 1)
        self.assertEqual(p.hp, 150)
        p.takeDamage(50)
        self.assertEqual(p.hp, 100)
        p.heal(50)
        self.assertEqual(p.hp, 150)
        p.heal(50)
        self.assertEqual(p.hp, 150)


class TestReward(unittest.TestCase):
    """"White-box test, testing the player is rewarded an item. Testing the state the game is in following the reward
        state """

    @patch('model.game_states.Menu')
    def testGetItem1(self, mock_menu):
        g = Game()
        reward = Reward(g)
        self.assertEqual(g.player.items, [])
        self.assertEqual(str(type(g.cur_state)), str(MagicMock))
        reward.getItem1()
        self.assertTrue(len(g.player.items), 1)
        self.assertEqual(str(type(g.cur_state)), "<class 'model.game_states.RoomSelection'>")


""" model\game_state.py: 34% coverage

    class Reward(GameState):

    def __init__(self, g):
        self.name = "ENEMY DIED. Select an item."
        self.background = "#BC88DF"
        self.game = g
        # initialize items
        activeItem = item.Item()
        activeItem.randomAbility("Active")
        activeItem.randomValueWideRange(10, 25, self.game.difficulty)
        passiveItem = item.Item()
        passiveItem.randomAbility("Passive")
        passiveItem.randomValueWideRange(10, 25, self.game.difficulty)
        self.item1 = activeItem.getItem()
        self.item2 = passiveItem.getItem()
        self.button_item1 = ui.Button("get "+self.item1[1], 220, 60, (60,300), function=self.getItem1)
        self.button_item2 = ui.Button("get "+self.item2[1], 220, 60, (540,300), function=self.getItem2)

    def getItem1(self):
        # put item 1 into player class inventory
        self.game.player.items.append(self.item1)
        self.game.transitionToRoomSelection()
"""

"""      
    game.py: coverage 65%

    class Game():
        #audio = Audio()
        def __init__(self):

            # By default the game is initialized to the Main state
            self.cur_state = game_states.Menu(self)
            self.run = True
            self.difficulty = 0
            self.numEncounters = 0
            self.player = classes.Player("Armored Soul")
            self.difficultyMods = { #dictionary containing modifiers
            0: 0.5, #easy
            1: 1.0, #medium
            2: 1.5 #hard

        def transitionToRoomSelection(self):
            self.cur_state = game_states.RoomSelection(self)
"""


class TestGame(unittest.TestCase):
    """"White-box tests, testing each method within the Game class itself"""

    def test_init(self):
        game = Game()
        self.assertEqual(game.getDifficulty(), 0)
        self.assertEqual(game.getEncounters(), 0)
        self.assertIsInstance(game.player, classes.Player)
        self.assertEqual(game.running(), True)

    def test_setDifficulty(self):
        game = Game()
        game.setDifficulty(0)
        self.assertEqual(game.getDifficulty(), 0)
        game.setDifficulty(1)
        self.assertEqual(game.getDifficulty(), 1)

    def test_set_state(self):
        game = Game()
        game.set_state(game_states.Combat)
        self.assertEqual(game.get_state(), game_states.Combat)

    def test_transitionToCombat(self):
        game = Game()
        game.transitionToCombat()
        self.assertEqual(game.get_state().__class__.__name__, 'Combat')


"""
    game.py: coverage 76%

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def getDifficulty(self):
        return self.difficulty

    # keep track of battles that the player has encountered
    def getEncounters(self):
        return self.numEncounters

    def set_state(self, new_state=0):
        self.cur_state = new_state

    # returns the current state
    def get_state(self):
        return self.cur_state

    def transitionToCombat(self):
        self.cur_state = game_states.Combat(self)

"""

if __name__ == '__main__':
    unittest.main()
