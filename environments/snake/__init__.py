from .. import Environment

import pygame
import numpy as np
import time

from .objects import *
from .constants import *
from .config import *

pygame.init()
font = pygame.font.SysFont(None, 20)

class Snake(Environment):

    def __init__(self):
        super().__init__()
        self.score = 0

    def render(self):

        if self.surface == None:
            self.surface = pygame.display.set_mode((width, height))
            pygame.display.set_caption('Flappy Bird')

        self.surface.fill(WHITE)

        self.surface.blit(font.render("Score: " + str(self.score), True, BLACK), [10, 10])
        pygame.display.update()

    def step(self, action):
        pass

    def random_action(self):
        return np.random.choice([0, 1, 2, 3])

    def reset(self):
        return self.get_state()

    def get_state(self):
        return []

    def num_of_actions(self):
        return 4

    def len_of_state(self):
        return 7

    def close(self):
        pygame.display.quit()
        self.surface = None