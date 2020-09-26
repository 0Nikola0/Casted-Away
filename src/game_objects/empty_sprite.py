import pygame


class EmptySprite(pygame.sprite.Sprite):
    """Used to receive updates from main_loop, kind of hacky"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect((0, 0, 0, 0))

