import pygame


class SelectionBox(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        super().__init__()
        self.image = pygame.Surface(rect.size)
        self.image.set_colorkey((0, 0, 0))
        w, h = self.image.get_width(), self.image.get_height()
        d = 1  # line width
        pts = [(0, 0 + d), (w - d, 0 + d), (w - d, h - d), (0, h - d)]
        pygame.draw.lines(self.image, color, True, pts, d)
        self.rect = self.image.get_rect(center=rect.center)
