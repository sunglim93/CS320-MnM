import pygame
import os
import time
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Metal and Magic")

FPS = 60

clock = pygame.time.Clock()

FONT = pygame.font.Font(os.path.join('Assets', 'alagard.ttf'), 52)
QTE = pygame.USEREVENT + 1

def drawBlankWindow(tp):
	WIN.fill(tp)
	pygame.display.update()

def renderLetters(text, letterList):
	for letter in text:
		char = FONT.render(letter, True, 'black')
		letterList.append(char)

def drawLetters(letterList):
	x = 100
	y = 100
	for i in letterList:
		letter = i
		WIN.blit(letter, (x, y))
		x += 100
	pygame.display.update()

def handleQTE(): 
#To do:
	#timer visualization
	#randomized button combos
	drawBlankWindow((255,255,255))  
	letterList = []
	text = "ZXC"
	renderLetters(text, letterList)
	drawLetters(letterList)

	curr = 0
	combo = [pygame.K_z, pygame.K_x, pygame.K_c]
	quick = True
	print("Starting QTE!")
	time = 3000
	while quick:
		time -= clock.tick(FPS)
		if time <= 0:
			print("Failed! Ran out of time!")
			drawBlankWindow((255,0,0))
			WIN.blit(FONT.render("Failure...", True, 'white'), (100,100))
			pygame.display.update()
			quick = False
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == combo[curr]:
					curr += 1
					if curr == len(combo):
						print("Success!")
						drawBlankWindow((0,255,0))
						WIN.blit(FONT.render("SUCCESS!", True, 'black'), (100,100))
						pygame.display.update()

						quick = False
				else:
					print("Failed! Wrong Combo!")
					drawBlankWindow((255,0,0))
					WIN.blit(FONT.render("Failure...", True, 'white'), (100,100))
					pygame.display.update()
					quick = False

def main():
	drawBlankWindow((255,255,255))

	run = True
	while run:
		clock.tick(FPS)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				run = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL:
					handleQTE()
	pygame.quit()

if __name__ == "__main__":
	main()