import pygame


class SelectionBox(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((0,0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.target = None

    def bind_to(self, target: pygame.sprite.Sprite):
        self.target = target
        self.image = pygame.Surface(target.rect.size)
        self.image.set_colorkey((0, 0, 0))
        w, h = self.image.get_width(), self.image.get_height()
        d = 1  # line width
        pts = [(0, 0 + d), (w - d, 0 + d), (w - d, h - d), (0, h - d)]
        pygame.draw.lines(self.image, self.color, True, pts, d)
        self.rect = self.image.get_rect(center=target.rect.center)

    def reset(self):
        self.image = pygame.Surface((0,0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.target = None

    def update(self, *args):
        if self.target:
            self.rect.center = self.target.rect.center
