import pygame
from src import settings as s


class Task(pygame.sprite.Sprite):
    def __init__(self, task_id: int,  increasement: float, pos, size):
        super(Task, self).__init__()
        """
        Harvesting = ID: 0
        Getting water = ID: 1
        Sleep / Eat / Drink = ID: 2
        """
        self.task_id = task_id
        self.increasement = increasement    # How much you gain from doing the task per loop
        self.rect = pygame.Rect(pos, size)

    def draw(self, surface):
        pygame.draw.rect(surface, s.BLACK, self.rect)

    def do_task(self):
        # Checks which ID the task is assigned and calls the corresponding function
        {0: self.harvest, 1: self.get_water, 2: self.increase_actor_stats}.get(self.task_id)()

    def harvest(self):
        s.FOOD_SUPPLY += self.increasement

    def get_water(self):
        s.WATER_SUPPLY += self.increasement

    # Same method can be used to increase each of the actor's stats eg Food status, Sleep status..
    def increase_actor_stats(self, current):
        current += self.increasement
        return current
