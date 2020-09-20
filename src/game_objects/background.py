import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, screen_size, color):
        super(Background, self).__init__()
        self.image = pygame.Surface(screen_size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
