import pygame
import qtest as q
import unittest
import time
from model import game_states
import game as g

class testSliderQTE(unittest.TestCase):
    '''
    White box test that tests for the coverage of the slider color. 
    Default is blue, green upon a success and red upon a failure
    '''
    def testColors(self):
        pygame.init()
        clock = pygame.time.Clock()
        slider = q.sliderQTE(timing=clock.tick)
        '''
        Test default value (blue)
        Code snippet that is being tested:
        class sliderQTE:
            def __init__(self, timing):
                self.sliderColor = 'blue'
        '''
        self.assertEqual(slider.sliderColor, 'blue')
        '''
        Test if the slider turns green after a success.
        Code snippet that is being tested:
        if self.buttonRect.center[0] <= self.sliderZone.right and self.buttonRect.center[0] >= self.sliderZone.left:
            self.sliderColor = 'green'
            return (True, 1)
        '''
        slider.buttonRect.x = slider.sliderZone.left
        slider.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        self.assertEqual(slider.sliderColor, 'green')
        '''
        Test if the slider turns red after a failure.
        Code snippet being tested:
        if self.buttonRect.center[0] <= self.sliderZone.right and self.buttonRect.center[0] >= self.sliderZone.left:
            self.sliderColor = 'green'
            return (True, 1)
        else:
            self.sliderColor = 'red'
            return (True, 0)
        '''
        slider.buttonRect.x = slider.sliderZone.right + 100
        slider.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        self.assertEqual(slider.sliderColor, 'red')

    def testTimeOutFail(self):#acceptance test for timing out
        pygame.init()
        clock = pygame.time.Clock()
        slider = q.sliderQTE(timing=clock.tick)
        slider.timeGiven = 1
        result, score = slider.update()
        while True:
            result, score = slider.update()
            if result:
                break
        self.assertEqual(result, True)
        self.assertEqual(score, 0)
    
    def testClickFail(self): #acceptance test for failing with a click immediately
        pygame.init()
        clock = pygame.time.Clock()
        slider = q.sliderQTE(timing=clock.tick)
        result, score = slider.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        self.assertEqual(result, True)
        self.assertEqual(score, 0)
    
    def testSuccess(self): #acceptance test for success click
        pygame.init()
        clock = pygame.time.Clock()
        slider = q.sliderQTE(timing=clock.tick)
        slider.buttonRect.x = slider.sliderZone.left
        result, score = slider.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        self.assertEqual(result, True)
        self.assertEqual(score, 1)

class testMultiHitSliderQTE(unittest.TestCase):
    def testNoSuccess(self): #acceptance test for no successes
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 0)
    
    def testFirst(self): #acceptance test for only one success on the first area
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.left = multiHit.sliderZones[0].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 1)
    
    def testSecond(self): #acceptance test for only one success on the second area
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.left = multiHit.sliderZones[1].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 1)
    
    def testThird(self): #acceptance test for only one success on the third area
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.left = multiHit.sliderZones[2].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 1)
    
    def testFirstSecond(self): #acceptance test for 2 successes on first and second area and make sure they're being added up correctly
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.left = multiHit.sliderZones[0].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.left = multiHit.sliderZones[1].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 2)
    
    def testFirstLastSuccess(self):#acceptance test for 2 successes on first and third area and make sure they're being added up correctly
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.left = multiHit.sliderZones[0].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.left = multiHit.sliderZones[2].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 2)
    
    def testSecondLastSuccess(self): #acceptance test for 2 successes on second and third area and make sure they're being added up correctly
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.left = multiHit.sliderZones[1].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.left = multiHit.sliderZones[2].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 2)
    
    def testThreeSuccess(self): #acceptance test for when all 3 are successes
        pygame.init()
        multiHit = q.multiHitSliderQTE(3)
        multiHit.buttonRect.left = multiHit.sliderZones[0].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.left = multiHit.sliderZones[1].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.left = multiHit.sliderZones[2].left
        multiHit.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        multiHit.buttonRect.right = multiHit.sliderRect.right
        result, score = multiHit.update()
        self.assertEqual(result, True)
        self.assertEqual(score, 3)
    
    def testIntegration(self): #Top down integration test by creating a mock battle scenario and then calling sliderQTE()
        game = g.Game()
        game.transitionToCombat()
        state = game.get_state()
        slider = state.sliderQTE()
        slider.buttonRect.right = slider.sliderRect.right
        result, score = slider.update()
        self.assertEqual(result, True) 
        self.assertEqual(score, 0) #test should return 0 successes

if __name__ == "__main__":
	unittest.main()