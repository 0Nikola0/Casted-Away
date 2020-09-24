import pygame
from src import settings as s

pygame.init()
screen = pygame.display.set_mode(s.SCREEN_SIZE)
FONT = pygame.font.SysFont("Mono", 32, bold=True)

IMGS_PATH = "../../assets/imgs/menu/"


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        # LOGO
        self.logo = pygame.image.load(IMGS_PATH + "logo.png")
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = round(s.SCREEN_WIDTH / 2), 80
        # Wallpaper
        self.image = pygame.image.load(IMGS_PATH + "background.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (0, 0)

    def draw(self):
        screen.blit(self.image, self.image_rect)
        screen.blit(self.logo, self.logo_rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos, size):
        super(Button, self).__init__()

        self.pos = pos

        self.name = name
        self.surface_text = FONT.render(self.name, True, s.WHITE)
        self.text_rect = self.surface_text.get_rect()
        self.text_rect.center = round(self.pos[0]), round(self.pos[1])

        self.image_inactive = pygame.image.load(IMGS_PATH + "green.png")
        self.image_inactive = pygame.transform.scale(self.image_inactive, size)
        self.image_active = pygame.image.load(IMGS_PATH + "green_clicked.png")
        self.image_active = pygame.transform.scale(self.image_active, size)
        self.image_clicked = pygame.transform.scale(self.image_active, (size[0] + 10, size[1] + 10))
        self.image = self.image_inactive
        self.rect = self.image.get_rect()
        self.rect.center = round(self.pos[0]), round(self.pos[1])

    def on_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.image = self.image_active
        else:
            self.image = self.image_inactive

    def on_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.image = self.image_clicked
            # Functionality here
            print(f"Clicked {self.name}")
        else:
            self.image = self.image_inactive

    def draw(self):
        self.rect = self.image.get_rect()
        self.rect.center = round(self.pos[0]), round(self.pos[1])
        screen.blit(self.image, self.rect)
        screen.blit(self.surface_text, self.text_rect)


def main():
    background = Background()
    posx, posy = 150, s.SCREEN_HEIGHT / 2
    buttons = [
        Button("Play", pos=(posx, posy + 240), size=(200, 80)),
        Button("Help", pos=(s.SCREEN_WIDTH / 2, posy + 240), size=(200, 80)),
        Button("About", pos=(s.SCREEN_WIDTH - posx, posy + 240), size=(200, 80)),
    ]
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for button in buttons:
            button.on_hover(mouse_pos)

        for button in buttons:
            if mouse_pressed[0]:    # If left click
                button.on_click(mouse_pos)

        background.draw()
        for button in buttons:
            button.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
