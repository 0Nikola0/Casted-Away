import pygame
import src.settings as s


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super(Obstacle, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

    def draw(self, surface):
        pygame.draw.rect(surface, s.BLACK, self.rect, 1)
