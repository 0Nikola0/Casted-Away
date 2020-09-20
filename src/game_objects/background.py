import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, screen_size, color):
        super(Background, self).__init__()
        self.surface = pygame.Surface(screen_size)
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
