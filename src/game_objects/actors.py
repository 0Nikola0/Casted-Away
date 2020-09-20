import pygame
import src.settings as s
from src.graphics import SpriteSheet


class ActorAdult(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheets):
        super(ActorAdult, self).__init__()

        sh = {key: SpriteSheet(value) for key, value in sprite_sheets.items()}

        self.images_idle = []
        for i in range(4):
            self.images_idle.append(sh["IDLE"].get_image(i))

        self.image = self.images_idle[0]
        pygame.transform.scale(self.image, s.ADULT_ACTOR_SIZE)

        self.rect = self.image.get_rect(topleft=pos)
        self.anim_type = 0
        self.state = "idle"
        self.vel = 5

    def move_left(self):
        self.rect.x -= self.vel

    def move_right(self):
        self.rect.x += self.vel

    def move_up(self):
        self.rect.y -= self.vel

    def move_down(self):
        self.rect.y += self.vel

    def update(self):
        self.image = self.images_idle[self.anim_type]
        pygame.time.delay(100)
        self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
