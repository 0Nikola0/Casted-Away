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
        self.vel = 5

        self.anim_delay = 0.2
        self.time_in_frame = 0.0

    def move_left(self):
        self.rect.x -= self.vel

    def move_right(self):
        self.rect.x += self.vel

    def move_up(self):
        self.rect.y -= self.vel

    def move_down(self):
        self.rect.y += self.vel

    def update(self, time_delta, *args):
        self.time_in_frame += time_delta

        for state in self.state.values():
            if self.current_state == state:
                self.image = self.images[self.current_state][self.anim_type]
                if self.time_in_frame > self.anim_delay:
                    self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
                    self.time_in_frame = 0


"""
    def update(self):
        self.image = self.images[self.state["WALK"]][self.anim_type]
        self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
"""


class TestActor(ActorAdult):
    """Test actor for physics tests"""
    def __init__(self, pos, sprite_sheets):
        super(TestActor, self).__init__(pos, sprite_sheets)
        self.target = None
        self.vel = 1

    def select_target(self, target_pos):
        self.target = target_pos

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        pass

    def handle_mouse_down(self, pos):
        self.select_target(pos)

    def handle_mouse_up(self, pos):
        pass

    def update(self, time_delta, *args):
        super(TestActor, self).update(time_delta, *args)

        if self.target is not None:
            tx, ty = self.target
            if self.rect.centerx < tx:
                self.move_right()
            elif self.rect.centerx > tx:
                self.move_left()

            if self.rect.centery < ty:
                self.move_down()
            elif self.rect.centery > ty:
                self.move_up()
