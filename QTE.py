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
FONT = pygame.font.Font(os.path.join('assets', 'alagard.ttf'), 52)

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

def checkSlider(buttonRect, sliderZone, keyPresses, rectColors, i): #helper func to check if the cursor is within the sliderZone or not
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

def handleTimeSliderQTE(numHits): #for multi-hit attacks; every success will translate to a hit
	quick = True
	sliderLength = 500
	sliderHeight = 36
	randomList = [] #list to hold the values to spawn slider zones at
	zoneWidth = 50
	zoneHeight = 50
	playerLeeWay = 100 #value to give the player time to react to the start of the QTE
	
	success = 0 #var to hold all the successes in the QTE
	keyPresses = [False, False, False] #keep track of key presses for each slider region
	rectColors = ['blue', 'blue', 'blue']
	sliderZones = [] #list to hold all the slider zones to be created
	speed = 4 #speed of the slider, can change for higher difficulties
	randomRanges = []

	sliderRect = pygame.Rect(WIDTH//2 - sliderLength//2, HEIGHT//2 - sliderHeight//2, sliderLength, sliderHeight) #create slider
	offset = (zoneHeight - sliderRect.height)//2
	buttonRect = pygame.Rect(sliderRect.left, sliderRect.top - offset, 10, zoneHeight) #create slider button
	bgRect = pygame.Rect(sliderRect.left, sliderRect.top - sliderHeight//2, sliderLength, sliderHeight*2)

	x = sliderRect.left+playerLeeWay #starting position for first region
	regionWidth = (sliderRect.width - playerLeeWay)//numHits #determine the width of each region
	
	for i in range(numHits):
		xPrime = x+regionWidth
		randomRanges.append((x, xPrime))
		x = xPrime

	for r in randomRanges: #generate a list of random numbers to spawn slider zones
		randomNum = random.randint(r[0], r[1] - zoneWidth)
		randomList.append(randomNum)

	for i in range(numHits): #create rects at the random spots in each region of the slider
		sliderZones.append(pygame.Rect(randomList[i], sliderRect.top - offset, zoneWidth, zoneHeight))
	
	while quick:
		clock.tick(FPS)
		pygame.draw.rect(WIN, 'orange', bgRect)
		# WIN.blit(FONT.render("Press Z", True, 'black'), (0,0))
		# WIN.blit(FONT.render("Successes: {}".format(success), True, 'black'), (300, 0)) #show number of successes on screen
		buttonRect.x += speed #move slider
		if buttonRect.right >= sliderRect.right: #end loop once button reaches the end of the slider
			quick = False
			return success #returns the num of successes for the attack
		pygame.draw.rect(WIN, 'black', sliderRect) #draw slider
		for i in range(numHits): #draw slider zones
			pygame.draw.rect(WIN, rectColors[i], sliderZones[i])
		pygame.draw.rect(WIN, 'red', buttonRect) #draw slider button
		pygame.display.update()
		'''When z button press is detected, check the position of the 
		slider button. Check if the button is in range of the slider zone
		in its respective range. If it is within the slider zone, increment
		success and change its respective key press to True. Otherwise,
		just turn the key press to True to "consume" the key press for that
		region. Repeat until all 3 regions have been checked.'''
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if (buttonRect.center[0] >= sliderRect.left #There's probably a better way to implement this
					and buttonRect.center[0] <= sliderZones[0].right):
					success += checkSlider(buttonRect, sliderZones[0], keyPresses, rectColors, 0)
				if (buttonRect.center[0] >= sliderZones[0].right 
					and buttonRect.center[0] <= sliderZones[1].right):
					success += checkSlider(buttonRect, sliderZones[1], keyPresses, rectColors, 1)
				if (buttonRect.center[0] >= sliderZones[1].right 
					and buttonRect.center[0] <= sliderRect.right):
					success += checkSlider(buttonRect, sliderZones[2], keyPresses, rectColors, 2)		

def handleSliderQTE(): #press z within the correct zone to succeed QTE
	quick = True
	sliderWidth = 200
	sliderHeight = 36
	sliderRect = pygame.Rect(WIDTH//2 - sliderWidth//2, HEIGHT//2 - sliderHeight//2, sliderWidth, sliderHeight) #create rects
	bgRect = pygame.Rect(sliderRect.left, sliderRect.top - sliderRect.height//2, sliderRect.width, sliderRect.height*3)
	buttonRect = pygame.Rect(sliderRect.left, sliderRect.top - 7, 10, 50)
	sliderZone = pygame.Rect(sliderRect.center[0] - 10, sliderRect.top, 20, 36)
	speed = 3 #speed of the slider, can change for higher difficulties
	timeDuration = 3000 #3 seconds to finish QTE, will change with difficulty
	timer = timeDuration
	while quick:	
		pygame.draw.rect(WIN, 'orange', bgRect)
		timer -= clock.tick(FPS) #tick timer
		barWidth = (timer / timeDuration) * sliderWidth #update width of the timer bar per tick
		pygame.draw.rect(WIN, 'red', (bgRect.left,bgRect.bottom - 20,barWidth,20))
		buttonRect.x += speed #move slider back and forth
		if buttonRect.left <= sliderRect.left or buttonRect.right >= sliderRect.right:
			speed = -speed
		pygame.draw.rect(WIN, 'black', sliderRect) #draw rects
		pygame.draw.rect(WIN, 'blue', sliderZone)
		pygame.draw.rect(WIN, 'red', buttonRect)
		pygame.display.update()
		if timer <= 0: #if player runs out of time
			pygame.draw.rect(WIN, 'red', sliderZone)
			pygame.display.update()
			quick = False
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if buttonRect.center[0] <= sliderZone.right and buttonRect.center[0] >= sliderZone.left:
					pygame.draw.rect(WIN, 'green', sliderZone)
					pygame.display.update()
				else:
					pygame.draw.rect(WIN, 'red', sliderZone)
					pygame.display.update()
				quick = False

def handleComboQTE():
	choices = ['Z', 'X', 'C']
	directions = ["UP", "DOWN", "LEFT", "RIGHT"]
	text = [] 
	combo = []
	for i in range(5): #randomize a list of 5 letters
		if (i % 2) != 0: #Z, X, C alternate with directional keys
			letter = random.choice(choices)
			text.append(letter)
			if letter == 'Z': #generate combo list to check with
				combo.append(pygame.K_z)
			if letter == 'X':
				combo.append(pygame.K_x)
			if letter == 'C':
				combo.append(pygame.K_c)
		else:
			direction = random.choice(directions)
			if direction == "UP":
				text.append('^')
				combo.append(pygame.K_UP)
			if direction == "DOWN":
				text.append('V')
				combo.append(pygame.K_DOWN)
			if direction == "LEFT":
				text.append('<')
				combo.append(pygame.K_LEFT)
			if direction == "RIGHT":
				text.append('>')
				combo.append(pygame.K_RIGHT)
	letterList = [] #used to draw letters onto the screen
	renderLetters(text, letterList) #generate letters to be drawn
	curr = 0
	quick = True
	timeDuration = 3000 #3 seconds to finish combo, will change with difficulty
	timer = timeDuration
	while quick:
		#draw screen, timer, and letters here
		WIN.fill((255,255,255))
		drawLetters(letterList)
		drawCursor(curr)
		timer -= clock.tick(FPS)
		barWidth = (timer / timeDuration) * 400
		pygame.draw.rect(WIN, 'red', (0,0,barWidth,50))
		pygame.display.update()
		pygame.time.delay(FPS)
		if timer <= 0:
			print("Failed! Ran out of time!")
			WIN.fill((255,0,0)) #failure message
			WIN.blit(FONT.render("Failure...", True, 'white'), (100,100))
			pygame.display.update()
			quick = False
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == combo[curr]:
					curr += 1
					if curr == len(combo):
						print("Success!") #success message
						WIN.fill((0,255,0))
						WIN.blit(FONT.render("SUCCESS!", True, 'black'), (100,100))
						pygame.display.update()

						quick = False
				else:
					print("Failed! Wrong Combo!") #failure message
					WIN.fill((255,0,0))
					WIN.blit(FONT.render("Failure...", True, 'white'), (100,100))
					pygame.display.update()
					quick = False

# def main():
# 	WIN.fill((255,0,0))
# 	# WIN.blit(FONT.render("Press R ctrl to start combo QTE", True, 'black'), (0,0))
# 	# WIN.blit(FONT.render("Press L ctrl to start slider QTE", True, 'black'), (0,100))
# 	# WIN.blit(FONT.render("Press '=' to start multi hit QTE", True, 'black'), (0,200))
# 	pygame.display.update()
# 	run = True
# 	while run:
# 		clock.tick(FPS)
# 		events = pygame.event.get()
# 		for event in events:
# 			if event.type == pygame.QUIT:
# 				run = False

# 			elif event.type == pygame.KEYDOWN:
# 				if event.key == pygame.K_LCTRL:
# 					handleComboQTE()
# 				if event.key == pygame.K_RCTRL:
# 					handleSliderQTE()
# 				if event.key == pygame.K_EQUALS:
# 					handleTimeSliderQTE(3)
# 	pygame.quit()

# if __name__ == "__main__":
# 	main()