import pygame
import random
WIDTH, HEIGHT = 900, 500

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Room Demo")

easy_button_image = pygame.image.load('easy_button.png').convert_alpha()
normal_button_image = pygame.image.load('normal_button.png').convert_alpha()
hard_button_image = pygame.image.load('hard_button.png').convert_alpha()

#button class
class Button():
    def __init__(self, x, y, image, name):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.button_name = name
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False

    def draw(self):

        #get mouse position
        position = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(position): #mouse is above button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print("clicked ", self.button_name)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        gameDisplay.blit(self.image, (self.rect.x, self.rect.y))



#button instances
easy_button = Button(WIDTH/2-150, HEIGHT/2, easy_button_image, "easy")
normal_button = Button(WIDTH/2, HEIGHT/2, normal_button_image, "normal")
hard_button = Button(WIDTH/2+150, HEIGHT/2, hard_button_image, "hard")

def main():
    run = True
    while run:

        easy_button.draw()
        normal_button.draw()
        hard_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #print(event)

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     print(event)
            #     color = (random.randrange(255), random.randrange(255), random.randrange(255))
            #     gameDisplay.fill(color)
            #     print("RGB Value: ", color)


        pygame.display.update()
    
    print("Quitting..")
    pygame.quit()

if __name__ == "__main__":
    main()

    