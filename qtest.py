import pygame
import os
import time
import random

import unittest
from unittest.mock import MagicMock, patch

from game import Game
from model.classes import Player, Enemy
from model import item, classes, game_states

# coverage run -m unittest qtest

from model.game_states import Reward

pygame.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Metal and Magic")

FPS = 60

clock = pygame.time.Clock()
FONT = pygame.font.Font(os.path.join('assets', 'alagard.ttf'), 52)

class sliderQTE:
    def __init__(self, timing):
        self.sliderColor = 'blue'
        self.sliderWidth = 200
        self.sliderHeight = 36
        self.sliderRect = pygame.Rect(WIDTH//2 - self.sliderWidth//2, HEIGHT//2 - self.sliderHeight//2, self.sliderWidth, self.sliderHeight) #create rects
        self.bgRect = pygame.Rect(self.sliderRect.left, self.sliderRect.top - self.sliderRect.height//2, self.sliderRect.width, self.sliderRect.height*3)
        self.buttonRect = pygame.Rect(self.sliderRect.left, self.sliderRect.top - 7, 10, 50)
        self.sliderZone = pygame.Rect(self.sliderRect.center[0] - 10, self.sliderRect.top, 20, 36)
        self.speed = 2
        self.timeGiven = 3000
        self.timeLeft = self.timeGiven
        self.timing = timing
        self.timeSinceLastUpdate = 0
    
    def update(self, deltaTime=10, event=None):
        self.buttonRect.x += self.speed
        self.timeLeft -= deltaTime
        if self.timeLeft <= 0: #if player runs out of time
            self.sliderColor = 'red'
            return (True, 0)
        if self.buttonRect.left <= self.sliderRect.left or self.buttonRect.right >= self.sliderRect.right:
            self.speed = -self.speed
        if event != None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttonRect.center[0] <= self.sliderZone.right and self.buttonRect.center[0] >= self.sliderZone.left:
                    self.sliderColor = 'green'
                    return (True, 1)
                else:
                    self.sliderColor = 'red'
                    return (True, 0)
            # self.timeSinceLastUpdate = timeElapsed - self.timing
        return (False, 0)
    
    def render(self):
        pygame.draw.rect(WIN, 'orange', self.bgRect)
        barWidth = (self.timeLeft / self.timeGiven) * self.sliderWidth #update width of the timer bar per tick
        pygame.draw.rect(WIN, 'red', (self.bgRect.left,self.bgRect.bottom - 20,barWidth,20))
        self.buttonRect = self.buttonRect #move slider back and forth
        pygame.draw.rect(WIN, 'black', self.sliderRect) #draw rects
        pygame.draw.rect(WIN, self.sliderColor, self.sliderZone)
        pygame.draw.rect(WIN, 'red', self.buttonRect)
        pygame.display.update()

class multiHitSliderQTE():
    def __init__(self, num):
        self.numHits = num
        self.sliderLength = 500
        self.sliderHeight = 36
        self.randomList = [] #list to hold the values to spawn slider zones at
        self.zoneWidth = 50
        self.zoneHeight = 50
        self.playerLeeWay = 100 #value to give the player time to react to the start of the QTE
        self.success = 0 #var to hold all the successes in the QTE
        self.keyPresses = [False, False, False] #keep track of key presses for each slider region
        self.rectColors = ['blue', 'blue', 'blue']
        self.sliderZones = [] #list to hold all the slider zones to be created
        self.speed = 3 #speed of the slider, can change for higher difficulties
        self.randomRanges = []
        self.sliderRect = pygame.Rect(WIDTH//2 - self.sliderLength//2, HEIGHT//2 - self.sliderHeight//2, self.sliderLength, self.sliderHeight) #create slider
        offset = (self.zoneHeight - self.sliderRect.height)//2
        self.buttonRect = pygame.Rect(self.sliderRect.left, self.sliderRect.top - offset, 10, self.zoneHeight) #create slider button
        self.bgRect = pygame.Rect(self.sliderRect.left, self.sliderRect.top - self.sliderHeight//2, self.sliderLength, self.sliderHeight*2)
        x = self.sliderRect.left+self.playerLeeWay #starting position for first region
        regionWidth = (self.sliderRect.width - self.playerLeeWay)//self.numHits #determine the width of each region
        for i in range(self.numHits):
            xPrime = x+regionWidth
            self.randomRanges.append((x, xPrime))
            x = xPrime
        for r in self.randomRanges: #generate a list of random numbers to spawn slider zones
            randomNum = random.randint(r[0], r[1] - self.zoneWidth)
            self.randomList.append(randomNum)
        for i in range(self.numHits): #create rects at the random spots in each region of the slider
            self.sliderZones.append(pygame.Rect(self.randomList[i], self.sliderRect.top - offset, self.zoneWidth, self.zoneHeight))

    def checkSlider(self, buttonRect, sliderZone, keyPresses, rectColors, i): #helper func to check if the cursor is within the sliderZone or not
        if (buttonRect.center[0] <= sliderZone.right 
            and buttonRect.center[0] >= sliderZone.left
            and not keyPresses[i]):
            rectColors[i] = 'green' #on success, change color to green and consume keypress
            keyPresses[i] = True
            return 1
        else:
            keyPresses[i] = True
            rectColors[i] = 'red'
            return 0 #this helper func is for the handleTimeSliderQTE()

    def update(self, event=None):
        self.buttonRect.x += self.speed
        if self.buttonRect.right >= self.sliderRect.right:
            return (True, self.success)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.buttonRect.center[0] >= self.sliderRect.left #There's probably a better way to implement this
                and self.buttonRect.center[0] <= self.sliderZones[0].right 
                and not self.keyPresses[0]):
                self.success += self.checkSlider(self.buttonRect, self.sliderZones[0], self.keyPresses, self.rectColors, 0)
            if (self.buttonRect.center[0] >= self.sliderZones[0].right 
                and self.buttonRect.center[0] <= self.sliderZones[1].right
                and not self.keyPresses[1]):
                self.success += self.checkSlider(self.buttonRect, self.sliderZones[1], self.keyPresses, self.rectColors, 1)
            if (self.buttonRect.center[0] >= self.sliderZones[1].right 
                and self.buttonRect.center[0] <= self.sliderRect.right
                and not self.keyPresses[2]):
                self.success += self.checkSlider(self.buttonRect, self.sliderZones[2], self.keyPresses, self.rectColors, 2)
        return (False, 0)
    
    def render(self):
        pygame.draw.rect(WIN, 'orange', self.bgRect)
        pygame.draw.rect(WIN, 'black', self.sliderRect) #draw slider
        for i in range(self.numHits): #draw slider zones
            pygame.draw.rect(WIN, self.rectColors[i], self.sliderZones[i])
        pygame.draw.rect(WIN, 'pink', self.buttonRect) #draw slider button
        pygame.display.update()
    
def main():
    WIN.fill((255,255,255))
    WIN.blit(FONT.render("Press R ctrl to start slider QTE", True, 'black'), (0,100))
    pygame.display.update()
    run = True
    state = []
    while run:
        clock.tick(FPS)
        timeElapsed = (pygame.time.get_ticks()) / 1000
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    print("starting qte")
                    state.append(sliderQTE(timeElapsed))
                if event.key == pygame.K_LCTRL:
                    print("starting multi hit qte")
                    state.append(multiHitSliderQTE(3))

        if len(state) != 0:
            result = state[-1].update(event=event)
            state[-1].render()
            if result[0] == True:
                print(result[1])
                state.pop()

    pygame.quit()




if __name__ == "__main__":
    main()