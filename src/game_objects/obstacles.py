import pygame
import src.settings as s
from src.game_objects.pymunk_bodies import ObstacleBody


class Obstacle(pygame.sprite.Sprite, ObstacleBody):
    __OBSTACLE_IDS = {}

    def __init__(self, pos, size, space):
        self.id = s.get_id(self, Obstacle.__OBSTACLE_IDS)
        ObstacleBody.__init__(self, pos, size, self.id, space)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

    def draw(self, surface):
        pygame.draw.rect(surface, s.BLACK, self.rect, 1)
