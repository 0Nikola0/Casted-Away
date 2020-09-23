import pygame
from src import settings as s

pygame.init()
screen = pygame.display.set_mode(s.SCREEN_SIZE)

IMGS_PATH = "../../assets/imgs/menu/"


class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, size):
        super(Button, self).__init__()

        self.image_inactive = pygame.image.load(IMGS_PATH + "ButtonDefaultRounded.png")
        self.image_inactive = pygame.transform.scale(self.image_inactive, size)
        self.image_active = pygame.image.load(IMGS_PATH + "ButtonActiveRounded.png")
        self.image_active = pygame.transform.scale(self.image_active, size)
        self.image_clicked = pygame.transform.scale(self.image_active, (size[0] + 10, size[1] + 10))
        self.image = self.image_inactive
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def on_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.image = self.image_active
        else:
            self.image = self.image_inactive

    def on_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.image = self.image_clicked
        else:
            self.image = self.image_active

    def draw(self):
        screen.blit(self.image, self.rect)


def main():
    play_button = Button("Play", (200, 200), (200, 80))
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        play_button.on_hover(mouse_pos)

        if mouse_pressed[0]:    # If left click
            play_button.on_click(mouse_pos)

        screen.fill(s.GRAY)
        play_button.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
