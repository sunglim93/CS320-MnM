import pygame
import os
import time
import random
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Metal and Magic")

FPS = 60

clock = pygame.time.Clock()
FONT = pygame.font.Font(os.path.join('assets', 'alagard.ttf'), 80)

def renderLetters(text, letterList):
    for letter in text:
        char = FONT.render(letter, True, 'black')
        letterList.append(char)

def drawLetters(letterList):
    x = 100
    y = 100
    for i in letterList:
        WIN.blit(i, (x, y))
        x += 100

def drawCursor(curr):
    x = 100
    y = 50
    WIN.blit((FONT.render('V', True, 'red')), (x+(100 * curr),y))

#helper func to check if the cursor is within the sliderZone or not
def checkSlider(buttonRect, sliderZone, keyPresses, rectColors, i, palette): 
    if (buttonRect.center[0] <= sliderZone.right 
        and buttonRect.center[0] >= sliderZone.left
        and not keyPresses[i]):
        #on success, change color to green and consume keypress
        rectColors[i] = palette['baseThree']
        keyPresses[i] = True
        return 1
    else:
        keyPresses[i] = True
        rectColors[i] = palette['baseOne']
        return 0 
    #this helper func is for the handleTimeSliderQTE()

#QTE for mashing the mouse button
def handleMashQTE():
    quick = True
    sliderLength = 500
    sliderHeight = 36
    # number of button presses needed to pass QTE
    mashNum = 16
    mashLength = sliderLength // mashNum
    # time given to player to finish QTE
    timeDuration = 3000
    timer = timeDuration
    # progress bar to track player's progress with mashing
    progressBarLength = 1
    progressBarColor = 'blue'
    # create rects
    sliderRect = pygame.Rect(WIDTH // 2 - sliderLength // 2, HEIGHT // 2 - sliderHeight // 2, sliderLength, sliderHeight)
    progressBarRect = pygame.Rect(WIDTH // 2 - sliderLength // 2, HEIGHT // 2 - sliderHeight // 2, progressBarLength, sliderHeight)
    bgRect = pygame.Rect(sliderRect.left, sliderRect.top - sliderHeight // 2, sliderLength, sliderHeight * 2)
    while quick:
        #decrement timer for each tick
        timer -= clock.tick(FPS)
        #decrement progress bar so that the player has to fight progress bar decay
        if progressBarLength > 1:
            progressBarLength -= 1
        # draw rects
        pygame.draw.rect(WIN, 'orange', bgRect)
        pygame.draw.rect(WIN, 'black', sliderRect)
        pygame.draw.rect(WIN, progressBarColor, progressBarRect)
        pygame.display.update()
        #timer failure
        if timer <= 0:
            #turn bar red and return False
            print("Failed, time out")
            progressBarColor = 'red'
            pygame.draw.rect(WIN, progressBarColor, progressBarRect)
            pygame.display.update()
            quick = False
            return False

        #mash the left mouse button to make progress
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quick = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #add to progress bar whenever the lmb is pressed
                progressBarLength += mashLength
                #when getting to the end of the slider, make the bar green to indicate success and return True
                if progressBarLength >= sliderLength:
                    print("success")
                    progressBarRect.width = sliderLength
                    progressBarColor = 'green'
                    pygame.draw.rect(WIN, progressBarColor, progressBarRect)
                    pygame.display.update()
                    quick = False
                    return True

        # update progress bar rectangle based on current progress
        progressBarRect.width = progressBarLength
        progressBarRect.left = sliderRect.left

#QTE for mashing alternating mouse buttons
def handleMashAlternateQTE():
    quick = True
    flag = 3
    sliderLength = 500
    sliderHeight = 36
    # number of button presses needed to pass QTE
    mashNum = 25
    mashLength = sliderLength // mashNum
    # time given to player to finish QTE
    timeDuration = 3000
    timer = timeDuration
    # progress bar to track player's progress with mashing
    progressBarLength = 1
    progressBarColor = 'blue'
    # create rects
    sliderRect = pygame.Rect(WIDTH // 2 - sliderLength // 2, HEIGHT // 2 - sliderHeight // 2, sliderLength, sliderHeight)
    progressBarRect = pygame.Rect(WIDTH // 2 - sliderLength // 2, HEIGHT // 2 - sliderHeight // 2, progressBarLength, sliderHeight)
    bgRect = pygame.Rect(sliderRect.left, sliderRect.top - sliderHeight // 2, sliderLength, sliderHeight * 2)
    while quick:
        #decrement timer for each tick
        timer -= clock.tick(FPS)
        #decrement progress bar so that the player has to fight progress bar decay
        if progressBarLength > 1:
            progressBarLength -= 2
        # draw rects
        pygame.draw.rect(WIN, 'orange', bgRect)
        pygame.draw.rect(WIN, 'black', sliderRect)
        pygame.draw.rect(WIN, progressBarColor, progressBarRect)
        pygame.display.update()
        #timer failure
        if timer <= 0:
            #turn bar red and return False
            print("Failed, time out")
            progressBarColor = 'red'
            pygame.draw.rect(WIN, progressBarColor, progressBarRect)
            pygame.display.update()
            quick = False
            return False

        #mash the left mouse button to make progress
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quick = False
            #make it so that player can start mashing with either mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and flag == 3:
                progressBarLength += mashLength
                flag = 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and flag == 3:
                progressBarLength += mashLength
                flag = 0

            #when left mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and flag == 0:
                #add to progress bar whenever the lmb is pressed
                progressBarLength += mashLength
                flag = 1
                #when getting to the end of the slider, make the bar green to indicate success and return True
                if progressBarLength >= sliderLength:
                    print("success")
                    progressBarRect.width = sliderLength
                    progressBarColor = 'green'
                    pygame.draw.rect(WIN, progressBarColor, progressBarRect)
                    pygame.display.update()
                    quick = False
                    return True
                
            #when right mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and flag == 1:
                #add to progress bar whenever the lmb is pressed
                progressBarLength += mashLength
                flag = 0
                #when getting to the end of the slider, make the bar green to indicate success and return True
                if progressBarLength >= sliderLength:
                    print("success")
                    progressBarRect.width = sliderLength
                    progressBarColor = 'green'
                    pygame.draw.rect(WIN, progressBarColor, progressBarRect)
                    pygame.display.update()
                    quick = False
                    return True

        # update progress bar rectangle based on current progress
        progressBarRect.width = progressBarLength
        progressBarRect.left = sliderRect.left

#for multi-hit attacks; every success will translate to a hit
def handleTimeSliderQTE(numHits, palette): 
    quick = True
    sliderLength = 500
    sliderHeight = 36
    #list to hold the values to spawn slider zones at
    randomList = [] 
    zoneWidth = 50
    zoneHeight = 50
    #value to give the player time to react to the start of the QTE
    playerLeeWay = 100 
    
    #var to hold all the successes in the QTE
    success = 0 
    #keep track of key presses for each slider region
    keyPresses = [False, False, False] 
    rectColors = [palette['midOne'], palette['midOne'], palette['midOne']]
    #list to hold all the slider zones to be created
    sliderZones = []
    #speed of the slider, can change for higher difficulties
    speed = 4 
    randomRanges = []

    #create slider
    sliderRect = pygame.Rect(WIDTH//2 - sliderLength//2, HEIGHT//2 - sliderHeight//2, sliderLength, sliderHeight) 
    offset = (zoneHeight - sliderRect.height)//2
    #create slider button
    buttonRect = pygame.Rect(sliderRect.left, sliderRect.top - offset, 10, zoneHeight) 
    bgRect = pygame.Rect(sliderRect.left, sliderRect.top - sliderHeight//2, sliderLength, sliderHeight*2)

    #starting position for first region
    x = sliderRect.left+playerLeeWay 
    #determine the width of each region
    regionWidth = (sliderRect.width - playerLeeWay)//numHits 
    
    for i in range(numHits):
        xPrime = x+regionWidth
        randomRanges.append((x, xPrime))
        x = xPrime

    #generate a list of random numbers to spawn slider zones
    for r in randomRanges: 
        randomNum = random.randint(r[0], r[1] - zoneWidth)
        randomList.append(randomNum)

    #create rects at the random spots in each region of the slider
    for i in range(numHits): 
        sliderZones.append(pygame.Rect(randomList[i], sliderRect.top - offset, zoneWidth, zoneHeight))
    
    while quick:
        clock.tick(FPS)
        pygame.draw.rect(WIN, palette['lightTwo'], bgRect)
        #move slider back and forth
        buttonRect.x += speed 
        #end loop once button reaches the end of the slider
        if buttonRect.right >= sliderRect.right: 
            quick = False
            #returns the num of successes for the attack
            return success 
        pygame.draw.rect(WIN, palette['baseOne'], sliderRect) #draw slider
        #draw slider zones
        for i in range(numHits): 
            pygame.draw.rect(WIN, rectColors[i], sliderZones[i])
        #draw slider button
        pygame.draw.rect(WIN, palette['midTwo'], buttonRect) 
        pygame.display.update()
        '''When the left mouse button press is detected, check the position of the 
        slider button. Check if the button is in range of the slider zone
        in its respective range. If it is within the slider zone, increment
        success and change its respective key press to True. Otherwise,
        just turn the key press to True to "consume" the key press for that
        region. Repeat until all 3 regions have been checked.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quick = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (buttonRect.center[0] >= sliderRect.left 
                    and buttonRect.center[0] <= sliderZones[0].right):
                    success += checkSlider(buttonRect, sliderZones[0], keyPresses, rectColors, 0, palette)
                if (buttonRect.center[0] >= sliderZones[0].right 
                    and buttonRect.center[0] <= sliderZones[1].right):
                    success += checkSlider(buttonRect, sliderZones[1], keyPresses, rectColors, 1, palette)
                if (buttonRect.center[0] >= sliderZones[1].right 
                    and buttonRect.center[0] <= sliderRect.right):
                    success += checkSlider(buttonRect, sliderZones[2], keyPresses, rectColors, 2, palette)		

#press mouse button within the correct zone to succeed QTE
def handleSliderQTE():
    quick = True
    sliderWidth = 200
    sliderHeight = 36
    #create rects
    sliderRect = pygame.Rect(WIDTH//2 - sliderWidth//2, HEIGHT//2 - sliderHeight//2, sliderWidth, sliderHeight) 
    bgRect = pygame.Rect(sliderRect.left, sliderRect.top - sliderRect.height//2, sliderRect.width, sliderRect.height*3)
    buttonRect = pygame.Rect(sliderRect.left, sliderRect.top - 7, 10, 50)
    sliderZone = pygame.Rect(sliderRect.center[0] - 10, sliderRect.top, 20, 36)
    #speed of the slider, can change for higher difficulties
    speed = 3 
    #3 seconds to finish QTE, will change with difficulty
    timeDuration = 3000 
    timer = timeDuration
    while quick:	
        pygame.draw.rect(WIN, 'orange', bgRect)
        #tick timer
        timer -= clock.tick(FPS) 
        #update width of the timer bar per tick
        barWidth = (timer / timeDuration) * sliderWidth
        pygame.draw.rect(WIN, 'red', (bgRect.left,bgRect.bottom - 20,barWidth,20))
        #move slider back and forth
        buttonRect.x += speed 
        if buttonRect.left <= sliderRect.left or buttonRect.right >= sliderRect.right:
            speed = -speed
        #draw rects
        pygame.draw.rect(WIN, 'black', sliderRect)
        pygame.draw.rect(WIN, 'blue', sliderZone)
        pygame.draw.rect(WIN, 'red', buttonRect)
        pygame.display.update()
        #if player runs out of time
        if timer <= 0: 
            pygame.draw.rect(WIN, 'red', sliderZone)
            pygame.display.update()
            quick = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quick = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonRect.center[0] <= sliderZone.right and buttonRect.center[0] >= sliderZone.left:
                    pygame.draw.rect(WIN, 'green', sliderZone)
                    pygame.display.update()
                else:
                    pygame.draw.rect(WIN, 'red', sliderZone)
                    pygame.display.update()
                quick = False

def handleComboQTE():
    choices = ['L', 'R']
    # directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    #text list will hold the actual text
    text = [] 
    #combo list will hold the button values to compare with
    combo = []
    #randomize a list of 5 letters or buttons
    for i in range(5):
        #use random to randomize a list of L and R
        button = random.choice(choices)
        #append to list
        text.append(button)
        #if button is L, append button 1 and if it is R, append button 2
        if button == 'L':
            combo.append(1)
        if button == 'R':
            combo.append(3)
        #Z, X, C alternate with directional keys 
        # if (i % 2) != 0: 
            # letter = random.choice(choices)
            # text.append(letter)
            #generate combo list to check with
            # if letter == 'Z': 
            #     combo.append(pygame.K_z)
            # if letter == 'X':
            #     combo.append(pygame.K_x)
            # if letter == 'C':
            #     combo.append(pygame.K_c)
        # else:
        #     direction = random.choice(directions)
        #     if direction == "UP":
        #         text.append('^')
        #         combo.append(pygame.K_UP)
        #     if direction == "DOWN":
        #         text.append('V')
        #         combo.append(pygame.K_DOWN)
        #     if direction == "LEFT":
        #         text.append('<')
        #         combo.append(pygame.K_LEFT)
        #     if direction == "RIGHT":
        #         text.append('>')
        #         combo.append(pygame.K_RIGHT)

    #used to draw letters onto the screen
    letterList = [] 
    #generate letters to be drawn
    renderLetters(text, letterList) 
    curr = 0
    quick = True
    #3 seconds to finish combo, will change with difficulty
    timeDuration = 3000 
    timer = timeDuration
    bgRectWidth = 500
    bgRectHeight = 200
    bgRect = pygame.Rect((WIDTH - bgRectWidth) // 2 , (HEIGHT - bgRectHeight)// 2, bgRectWidth, bgRectHeight )
    #color list for blitting to the screen. Will update as player completes the combo
    colorList = ['black','black','black','black','black']

    while quick:
        #draw screen, timer, and letters here
        # drawLetters(letterList)
        # drawCursor(curr)
        #for timer visualization purposes
        timer -= clock.tick(FPS)
        barWidth = (timer / timeDuration) * bgRectWidth
        pygame.draw.rect(WIN, 'orange', bgRect)
        pygame.draw.rect(WIN, 'red', (bgRect.left,bgRect.bottom - 20,barWidth,20))
        i = 0
        x = bgRect.left + 25
        y = bgRect.center[1] - 40
        #iterate thru the list and blit each letter
        while i < len(text):
            textSurface = FONT.render(text[i], True, colorList[i])
            WIN.blit(textSurface, (x, y))
            x += 100
            i += 1
        pygame.display.update()
        if timer <= 0:
            #failure message
            print("Failed! Ran out of time!")
            #change all text to red to indicate time out
            j = 0
            while j < len(colorList):
                colorList[j] = 'red'
                j += 1
            blitText(WIN, FONT, text, colorList, bgRect)
            quick = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quick = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if the input is correct, change color of letter to green
                if event.button == combo[curr]:
                    colorList[curr] = 'green'
                    curr += 1
                    #if the end of the combo is reached, end the QTE
                    if curr == len(combo):
                        colorList[curr-1] = 'green'
                        blitText(WIN, FONT, text, colorList, bgRect)
                        print("Success!")
                        quick = False
                        return True
                else:
                    #if an incorrect input is received, change the current letter to red and end the QTE
                    colorList[curr] = 'red'
                    blitText(WIN, FONT, text, colorList, bgRect)
                    print("Failed! Wrong combo!")
                    quick = False
                    return False
            #kept this stuff in case we needed to add in kb combos
            # if event.type == pygame.KEYDOWN:
            #     if event.key == combo[curr]:
            #         curr += 1
            #         if curr == len(combo):
            #             #success message
            #             print("Success!") 
            #             WIN.fill((0,255,0))
            #             WIN.blit(FONT.render("SUCCESS!", True, 'black'), (100,100))
            #             pygame.display.update()

            #             quick = False
            #     else:
            #         #failure message
            #         print("Failed! Wrong Combo!") 
            #         WIN.fill((255,0,0))
            #         WIN.blit(FONT.render("Failure...", True, 'white'), (100,100))
            #         pygame.display.update()
            #         quick = False

#helper function for handleComboQTE() to blit the updated text colors onto the screen
def blitText(WIN, FONT, text, colorList, bgRect):
    i = 0
    x = bgRect.left + 25
    y = bgRect.center[1] - 40
    #iterate thru the list and blit each letter
    while i < len(text):
        textSurface = FONT.render(text[i], True, colorList[i])
        WIN.blit(textSurface, (x, y))
        x += 100
        i += 1
    pygame.display.update()

def main():
    WIN.fill((255,255,255))
    # WIN.blit(FONT.render("Press R ctrl to start combo QTE", True, 'black'), (0,0))
    # WIN.blit(FONT.render("Press L ctrl to start slider QTE", True, 'black'), (0,100))
    # WIN.blit(FONT.render("Press '=' to start multi hit QTE", True, 'black'), (0,200))
    pygame.display.update()
    run = True
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    handleComboQTE()
                if event.key == pygame.K_RCTRL:
                    handleSliderQTE()
                if event.key == pygame.K_EQUALS:
                    handleTimeSliderQTE(3)
                if event.key == pygame.K_TAB:
                    handleMashAlternateQTE()
                if event.key == pygame.K_SPACE:
                    handleMashQTE()
    pygame.quit()

if __name__ == "__main__":
    main()