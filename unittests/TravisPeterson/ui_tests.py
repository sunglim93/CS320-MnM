

import unittest

import pygame

import game

from view import UIElements

from model import game_states

from model import classes




class TravisTestingSuite(unittest.TestCase):



    """

    These test, thoroughly test the Game class features.

    This includes tests for state transitions, quitting/running,

    ensuring game_states are inherited correctly, etc.

    """

    # Test One - Black Box Acceptance Test

    def test_running(self): 

        g = game.Game()

        self.assertFalse(g.running())



    # Test Two - Black Box Acceptance Test

    def test_quitting(self):

        g = game.Game()

        g.quit()

        self.assertFalse(g.running())



    # Test Three - Black Box Acceptance Test

    def test_game_initialization(self): #blackbox

        g = game.Game()

        self.assertEqual(type(g.get_state()), game_states.Menu)



    # Test Four - Black Box Acceptance Test

    def test_transition_to_Load(self): #blackbox

        g = game.Game()

        g.transitionToLoad()

        self.assertEqual(type(g.get_state()), game_states.Loading)



    # Test Five - Black Box Acceptance Test

    def test_transition_to_Combat(self): #blackbox

        g = game.Game()

        g.transitionToCombat()

        self.assertEqual(type(g.get_state()), game_states.Combat)



    # Test Six - Black Box Acceptance Test

    def test_boss_instance_of_combat(self): #blackbox

        g = game.Game()

        g.transitionToBoss()

        self.assertIsInstance(g.get_state(), game_states.Combat)

    

    """

    The following test exmaine the functionality of the healthbar object.

    These tests verify the healthbar does not draw outside of its established 

    bounds, verifies that it adequately adjusts for when positioned outside 

    of the window size, and verifies that it integrates nicely with the 

    developed player object.



    Note: The constructor of HealthBar contains this code snippet:



        if cur > max:

            self.cur = max

        else:

            self.cur = cur



        if self.cur < 0:

            self.cur = 0



    Tests Seven and Eight combined provide full coverage as they test all

    possible circumstances for cur.



    Test Seven: test the case where cur > max and self.cur > 0

    Test Eight: test the case where cur <= max and self.cur < 0

    """



    # Test Seven - White Box Test

    def test_healthbar_max(self):

        hb = UIElements.HealthBar(100, 50, (100,100))

        self.assertEqual(hb.cur, 50)



    # Test Eight - White Box Test

    def test_healthbar_min(self):

        hb = UIElements.HealthBar(-100, 100, (100,100))

        self.assertEqual(hb.cur, 0)



    # Test Nine - Black Box Acceptance Test

    def test_healthbar_posx_high(self):

        pygame.init()

        pygame.display.flip()

        screen = pygame.display.set_mode((800,600))

        hb = UIElements.HealthBar(100, 100, (900,100))

        hb.draw(screen)

        self.assertEqual(hb.pos, (800,100))



    # Test Ten - Black Box Acceptance Test

    def test_healthbar_posx_low(self):

        pygame.init()

        pygame.display.flip()

        screen = pygame.display.set_mode((800,600))

        hb = UIElements.HealthBar(100, 100, (-100,100))

        hb.draw(screen)

        self.assertEqual(hb.pos, (30,100))



    """

    The below are two integration tests (eleven and twelve) tests the 

    integration between the player object and the healthbar object. 

    It uses the player health and damage functions to set the healthbar's 

    values to verify the two can work together.



    This would be an example of Bottom-Up integration testing since

    we have written the two units (player and healthbar) that work should

    work together. Now, we are writing the unittests for them.

    """



    # Test Eleven - Integration Test

    def test_player_loss_health(self):

        p = classes.Player("Williams")

        hb = UIElements.HealthBar(p.getHP(), p.getMaxHP(), (100,100))

        p.takeDamage(20)

        hb.update(p.getHP(), p.getMaxHP())

        self.assertEqual(p.getHP(), hb.cur)



    # Test Tweleve - Integration Test

    def test_player_lose_too_much(self):

        p = classes.Player("Grant")

        hb = UIElements.HealthBar(p.getHP(), p.getMaxHP(), (100, 100))

        p.takeDamage(p.getMaxHP() + 30)

        hb.update(p.getHP(), p.getMaxHP())

        self.assertEqual(hb.cur,p.getHP())

        self.assertEqual(hb.cur, 0)



if __name__ == '__main__':

    unittest.main()

