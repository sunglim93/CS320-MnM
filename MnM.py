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
FONT = pygame.font.Font(os.path.join('Assets', 'alagard.ttf'), 52)

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

def handleSliderQTE(): #press z within the correct zone to succeed QTE
	quick = True
	sliderRect = pygame.Rect(100, 150, 200, 36) #create rects
	buttonRect = pygame.Rect(sliderRect.left, sliderRect.top - 7, 10, 50)
	sliderZone = pygame.Rect(sliderRect.center[0] - 10, sliderRect.top, 20, 36)
	speed = 3 #speed of the slider, can change for higher difficulties
	timeDuration = 3000 #3 seconds to finish QTE, will change with difficulty
	timer = timeDuration
	while quick:	
		WIN.fill((255,255,255)) #bg
		timer -= clock.tick(FPS) #tick timer
		barWidth = (timer / timeDuration) * 400 #update width of the timer bar per tick
		pygame.draw.rect(WIN, 'red', (500,0,barWidth,50))
		WIN.blit(FONT.render("Press Z", True, 'black'), (0,0))
		buttonRect.x += speed #move slider back and forth
		if buttonRect.left <= sliderRect.left or buttonRect.right >= sliderRect.right:
			speed = -speed
		pygame.draw.rect(WIN, 'black', sliderRect) #draw rects
		pygame.draw.rect(WIN, 'green', sliderZone)
		pygame.draw.rect(WIN, 'red', buttonRect)
		pygame.display.update()
		if timer <= 0: #if player runs out of time
			print("Failed! Ran out of time!")
			WIN.fill((255,0,0)) #failure message
			WIN.blit(FONT.render("Failure...", True, 'white'), (100,100))
			pygame.display.update()
			quick = False
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z: #if z button press is detected
					if buttonRect.center[0] <= sliderZone.right and buttonRect.center[0] >= sliderZone.left:
						print("You got it!")
						WIN.fill('green')
						WIN.blit(FONT.render("SUCCESS!", True, 'black'), (100,100))
						pygame.display.update()
					else:
						print("Failed...")
						WIN.fill('red')
						WIN.blit(FONT.render("Failure...", True, 'white'), (100,100))
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

def main():
	WIN.fill((255,255,255))
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
	pygame.quit()

if __name__ == "__main__":
	main()