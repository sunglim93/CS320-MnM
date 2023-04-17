import pygame
import time

# Initialize pygame
pygame.init()

# Set the window size
size = (800, 600)
screen = pygame.display.set_mode(size)

# Load the default font
font = pygame.freetype.SysFont(None, 24)

# Create the text box
text_box = pygame.Surface((600, 200))
text_box_rect = text_box.get_rect()
text_box_rect.center = (400, 300)

# Set the initial text
text = '*' * 20 + '\n' + '*' * 20 + '\n' + '*' * 20 + '\n' + '*' * 20  # start with 4 rows of 20 asterisks

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.unicode.isprintable():
                text = text.replace('*', event.unicode, 1)  # replace the first asterisk with the typed character
                time.sleep(0.1)
                text_rect = font.get_rect(text) # get the rect of the text
                if text_rect.width > text_box_rect.width:  # check if the width exceeds the text box
                    text = text[:text.rfind('\n')+1] + '\n' + '*' * (text.count('\n')+1)  # wrap the text to the next line
                if text.count('\n') >= 4:
                    text = text[text.index('\n')+1:]
    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the text box
    pygame.draw.rect(screen, (0, 0, 0), text_box_rect, 2)

    text_box.fill((255, 255, 255))
    font.render_to(text_box, (10, 10), text, (0, 0, 0))
    screen.blit(text_box, text_box_rect)

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()

