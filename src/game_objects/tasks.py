import pygame
from src import settings as s


class Task(pygame.sprite.Sprite):
    def __init__(self, name, pos, size):
        super(Task, self).__init__()
        self.name = name
        self.rect = pygame.Rect(pos, size)

    def draw(self, surface):
        pygame.draw.rect(surface, s.BLACK, self.rect)
