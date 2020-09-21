from random import randint

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
        self.state = {
            "ATTACK": 0,
            "DEATH": 1,
            "HURT": 2,
            "IDLE": 3,
            "WALK": 4
        }
        self.current_state = 4
        self.anim_type = 0
        self.anim_delay = 0.2
        self.time_in_frame = 0.0

        self.directionx, self.directiony = 0, 0
        self.vel = 5
        self.update_directions()

    def move_left(self):
        self.rect.x -= self.vel

    def move_right(self):
        self.rect.x += self.vel

    def move_up(self):
        self.rect.y -= self.vel

    def move_down(self):
        self.rect.y += self.vel

    def move(self):
        self.rect.x += self.vel * self.directionx
        self.rect.y += self.vel * self.directiony

    # This shouldn't be called every loop
    def update_directions(self):
        """
        -1: Left / Up
        0: No movement
        1: Right / Down
        """
        self.directionx = randint(-1, 1)
        self.directiony = randint(-1, 1)
        self.move()

    def update(self, time_delta, *args):
        self.time_in_frame += time_delta

        for state in self.state.values():
            if self.current_state == state:
                self.image = self.images[self.current_state][self.anim_type]
                if self.time_in_frame > self.anim_delay:
                    # Temporarly called from here
                    self.move()

                    self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
                    self.time_in_frame = 0


"""
    def update(self):
        self.image = self.images[self.state["WALK"]][self.anim_type]
        self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
"""
