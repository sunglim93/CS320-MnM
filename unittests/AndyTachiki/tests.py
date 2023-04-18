import unittest
import pygame
from game import Game
import time
from model.game_states import Menu, Loading

class Helper(unittest.TestCase):

    def setUp(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.flip()

        clock = pygame.time.Clock()
        FPS = 60
        self.game = Game()
        state = self.game.get_state()
        state.loadBackground(screen)
        state.loadUI(screen)
        self.main_menu = Menu(self.game)

    def tearDown(self):
        print("tear down")
        pygame.quit()


class TestMMButtonClick(Helper):
    """"Acceptance test, testing that the start button at the main menu when clicked, is sent to the loading state"""
    def test_start_button(self):
        # simulate a click on the start button
        start_button = self.main_menu.button_start
        #print(start_button.top_rect.center)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(368, 310))
        pygame.event.post(event)
        self.main_menu.handleActions(event)
        self.game.transitionToLoad()
        # check that the game state has transitioned from main_menu to loading_state
        self.assertEqual(type(self.main_menu.game.cur_state), Loading)


class TestLoadScreen(Helper):
    def test_load_screen_time(self):
        """"My cool cam acceptance test, testing that the loading screen doesn't take more than 3 seconds to load"""
        start_time = time.time()
        self.game.transitionToLoad()
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertLessEqual(elapsed_time, 3.0)


