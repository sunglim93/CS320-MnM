import pygame
import openai

openai.api_key = ""

def chatGPT(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop='stop',
        temperature=0.5,
    )

    npc_choice = completions.choices[0].text
    return npc_choice.strip()

# Initialize Pygame
pygame.init()

# Create the window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chatbot")

# Create the input box for the player
player_box = pygame.Rect(50, 400, 600, 50)

# Create the output box for the NPC
npc_box = pygame.Rect(50, 50, 600, 50)

# Create the font for the text
font = pygame.font.Font(None, 32)

# Initialize the player's input text
player_input = ""

# Initialize the NPC's response text
npc_response = ""

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalnum() or event.unicode in [' ', '.', ',', '!', '?']:
                player_input += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                player_input = player_input[:-1]
            elif event.key == pygame.K_RETURN:
                # with open("corpus.txt", "r") as corpus_file:
                #     corpus_text = corpus_file.read()
                final_input = player_input
                npc_response = chatGPT(final_input)
                player_input = ""
                print("NPC: " + npc_response)

    screen.fill((255, 255, 255))

    # Draw the input box for the player
    pygame.draw.rect(screen, (0, 0, 0), player_box, 2)
    player_text = font.render(player_input, True, (0, 0, 0))
    screen.blit(player_text, (60, 410))

    # Draw the output box for the NPC
    pygame.draw.rect(screen, (0, 0, 0), npc_box, 2)
    npc_text = font.render(npc_response, True, (0, 0, 0))
    screen.blit(npc_text, (60, 60))

    pygame.display.update()
