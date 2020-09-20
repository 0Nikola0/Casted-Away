import pygame
import src.settings as s
from src.graphics import SpriteSheet


class ActorAdult(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheets):
        super(ActorAdult, self).__init__()

        sh = {key: SpriteSheet(value) for key, value in sprite_sheets.items()}

        self.images = []
        for x in sh:
            self.images_temp = []
            for i in range(4):
                self.images_temp.append(sh[x].get_image(i))
            self.images.append(self.images_temp)

        # Just to reference what type self.image should be
        self.image = sh["IDLE"].get_image(0)
        pygame.transform.scale(self.image, s.ADULT_ACTOR_SIZE)

        self.rect = self.image.get_rect(topleft=pos)
        self.anim_type = 0
        self.state = {
            "ATTACK": 0,
            "DEATH": 1,
            "HURT": 2,
            "IDLE": 3,
            "WALK": 4
        }
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
        self.image = self.images[self.state["WALK"]][self.anim_type]
        self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
