import pygame


class TestFloor(pygame.sprite.Sprite):
    def __init__(self, pos, size, color):
        super(TestFloor, self).__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
