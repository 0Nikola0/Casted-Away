import pygame
import src.settings as s


class ActorAdult(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super(ActorAdult, self).__init__()

        self.image = pygame.image.load(image)
        pygame.transform.scale(self.image, s.ADULT_ACTOR_SIZE)
        self.rect = self.image.get_rect(topleft=pos)

        self.vel = 5

    def move_left(self):
        self.rect.x -= self.vel

    def move_right(self):
        self.rect.x += self.vel
