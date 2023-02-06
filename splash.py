import pygame
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
import openai

openai.api_key = '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'


# openai.Model.list()


def ai_image():
    response = openai.Image.create(
        prompt="An armored roguelike character running away from enemies in a castle",
        n=1,
        size="512x512"
    )

    image_url = response["data"][0]["url"]
    im = Image.open(BytesIO(requests.get(image_url).content))
    return im


def pixelate_ai_image(im, size=16):
  #  im = im.resize((im.width // 4, im.height // 4), resample=Image.NEAREST)
    im = im.resize((im.width, im.height), resample=Image.NEAREST)
    return im


def display_screen(screen, image):
    font = ImageFont.truetype("pixelated.ttf", 36)
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize("Metal and Magic", font=font)

    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2
    draw.text((x, y), "Metal and Magic", fill=(255, 255, 255), font=font)

    pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

    screen.blit(pygame_image, (0, 0))
    pygame.display.update()


def main():
    pygame.init()

    image = ai_image()
    pixeled_image = pixelate_ai_image(image)
    #pixeled_image = pygame.image.load("C:\\Users\\Andy\\Desktop\\text image example.PNG")

    pygame.display.set_caption("Metal and Magic")

    screen = pygame.display.set_mode( (pixeled_image.width, pixeled_image.height))

    image = pygame.image.fromstring(pixeled_image.tobytes(), (pixeled_image.width, pixeled_image.height), "RGB")

    screen.blit(image, (0, 0))

    font = pygame.font.Font(None, 36)
    text = font.render("LOADING", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (image.get_width() // 2, image.get_height() // 2)
    pygame.draw.rect(screen, (0, 0, 0),(text_rect.left - 20, text_rect.top - 20,
                                         text_rect.width + 40, text_rect.height + 40), 0)
    screen.blit(text, text_rect)

    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()


if __name__ == "__main__":
    main()
