# Anita Ply
# Grant Williams
# CS320
# 3/24/2023
# Unit testing for Metal and Magic

from model import game_states
import game
import unittest
from model import classes

class testGame(unittest.TestCase):

	# Acceptance test, confirm Game class properly initializes first set of variables
	def testGameInitialize(self):
		g = game.Game()
		self.assertTrue(isinstance(g.cur_state, game_states.Menu))
		self.assertEqual(g.run, True)
		self.assertEqual(g.difficulty, 0)
		self.assertEqual(g.numEncounters, 0)
		self.assertTrue(isinstance(g.player, classes.Player))


	# Acceptance test, confirm buttons on Menu state contain functions
	def testMenuButtons(self):
		g = game.Game()
		state = game_states.Menu(g)
		self.assertNotEqual(state.button_start.function, 'function')
		self.assertNotEqual(state.button_settings, 'function')
		self.assertNotEqual(state.button_quit, 'function')


	# Acceptance test, confirm buttons on Combat state contain functions
	def testCombatButtons(self):
		g = game.Game()
		state = game_states.Combat(g)
		self.assertNotEqual(state.button_attack, 'function')


	# Acceptance test, confirm buttons on Shop state contain functions
	def testShopButtons(self):
		g = game.Game()
		state = game_states.Shop(g)
		self.assertNotEqual(state.button_enter, 'function')
		self.assertNotEqual(state.button_leave, 'function')


	# Acceptance test, confirm buttons on Shop state contain functions
	def testShopMenuButtons(self):
		g = game.Game()
		state = game_states.ShopMenu(g)
		self.assertNotEqual(state.button_buy, 'function')
		self.assertNotEqual(state.button_sell, 'function')
		self.assertNotEqual(state.button_back, 'function')


	# Acceptance test, confirm buttons on Shop state contain functions
	def testDifficultyButtons(self):
		g = game.Game()
		state = game_states.Difficulty(g)
		self.assertNotEqual(state.button_easy, 'function')
		self.assertNotEqual(state.button_normal, 'function')
		self.assertNotEqual(state.button_hard, 'function')


	# Acceptance test, confirm buttons on Shop state contain functions
	def testRoomSelectionButtons(self):
		g = game.Game()
		state = game_states.RoomSelection(g)
		self.assertNotEqual(state.button_room_rd, 'function')
		self.assertNotEqual(state.button_room_shop, 'function')


	# Acceptance test, confirm buttons on Shop state contain functions
	def testVictoryButtons(self):
		g = game.Game()
		state = game_states.Victory(g)
		self.assertNotEqual(state.button_restart, 'function')


	#Acceptance test, confirm that an enemy class has been initialized during the combat state
	def testEnemyInitialize(self):
		g = game.Game()
		state = game_states.Combat(g)
		self.assertTrue(isinstance(state.enemy, classes.Enemy))


	# White Box test, test encounter increment method within the Game class
	def testEncounterIncrements(self):
		"""
		Method tested: increaseEncouter()
		This white box test tests that each increaseEncouter() call increments the
		numEncounters variable by 1 each time.
		"""
		g = game.Game()
		#initial encounters should be set to 0
		self.assertEqual(g.numEncounters, 0)
		g.increaseEncounters()
		self.assertEqual(g.numEncounters, 1)
		g.increaseEncounters()
		self.assertEqual(g.numEncounters, 2)
		g.increaseEncounters()
		self.assertEqual(g.numEncounters, 3)


	# White Box test, test set difficulty method within Game class
	def testSetDifficulty(self):
		"""
		Method tested: setDifficulty()
		This white box test tests if the setDifficulty() method will set
		the difficulty variable to the specified int.
		"""
		g = game.Game()
		#initial difficulty should be set to 0
		self.assertEqual(g.difficulty, 0)
		g.setDifficulty(5)
		self.assertEqual(g.difficulty, 5)
		g.setDifficulty(1000)
		self.assertEqual(g.difficulty, 1000)


	# White Box test, test reset encounters method within Game class
	def testResetEncounters(self):
		"""
		Method tested: resetEncounters()
		This white box test tests if the resetEncounters() method resets
		the numEncounter variable back to 0.
		"""
		g = game.Game()
		#initial encounters should be set to 0
		self.assertEqual(g.numEncounters, 0)
		g.increaseEncounters()
		self.assertEqual(g.numEncounters, 1)
		g.resetEncounters()
		self.assertEqual(g.numEncounters, 0)


	# Integration Testing, test difficulty values from difficulty class from game_states
	def testDifficultySettings(self):
		"""
		This integration test tests the game class and the difficulty class.
		The difficulty class changes the difficulty variable within the game
		class to set values. An incremental approach was used for this testing
		to test that each method from the difficulty class works with the game
		class. The first assert checks the difficulty setting within the
		difficulty class and the second assert checks the difficulty setting
		from the game class.
		"""

		g = game.Game()
		state = game_states.Difficulty(g)

		state.setEasyDifficulty()
		#checking from difficulty class object
		self.assertEqual(state.game.difficulty, 0)
		#checking from game class object
		self.assertEqual(g.difficulty, 0)

		state.setNormalDifficulty()
		self.assertEqual(state.game.difficulty, 1)
		self.assertEqual(g.difficulty, 1)

		state.setHardDifficulty()
		self.assertEqual(state.game.difficulty, 2)
		self.assertEqual(g.difficulty, 2)


	# Integration Testing, test encounter increment from combat class to game class
	def testCombatIncrement(self):
		"""
		This integration test tests the num encounter increment after successfully
		completing the combat module and defeating the enemy. Enemy hp is set to 0
		to pass enemy death conditional within the sliderQTE method. An incremental
		approach was used for this test.
		"""
		g = game.Game()
		state = game_states.Combat(g)
		#check num encounters from game class
		self.assertEqual(g.numEncounters, 0)
		#check num encounters from combat class
		self.assertEqual(state.game.numEncounters, 0)
		state.enemy.hp = 0
		state.sliderQTE()
		self.assertEqual(g.numEncounters, 1)
		self.assertEqual(state.game.numEncounters, 1)


if __name__ == '__main__':
	unittest.main()