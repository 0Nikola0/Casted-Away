import pygame
import src.settings as s


class Actor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Actor, self).__init__()

        self.posx, self.posy = pos
        self.sizex, self.sizey = s.ACTOR_SIZE
        self.image = pygame.Surface(s.ACTOR_SIZE)
        self.rect = self.image.get_rect(topleft=pos)

        self.vel = 5

    def move_left(self):
        self.posx -= self.vel

    def move_right(self):
        self.posx += self.vel
