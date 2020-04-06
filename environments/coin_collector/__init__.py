from .. import Environment

import pygame
import numpy as np

from .objects import *
from .config import *
from .constants import *

pygame.init()

class CoinCollector(Environment):

    def __init__(self):
        self.enemy = Enemy(np.random.choice(range(4)))
        self.agent = Player()
        self.coin = Coin()
        self.surface = None

    def render(self):
        if self.surface == None:
            self.surface = pygame.display.set_mode((width, height))
            pygame.display.set_caption('Coin Collecter')
        self.surface.fill(WHITE)
        self.enemy.draw(self.surface)
        self.agent.draw(self.surface)
        self.coin.draw(self.surface)
        pygame.display.update()

    def step(self, action):

        reward = 1
        done = False

        self.agent.update(action)
        self.enemy.update(self.agent)

        if self.agent.collides(self.coin):
            self.coin = Coin()
            reward = 100
        
        if self.agent.collides(self.enemy):
            done = True
            reward = -50

        return self.get_state(), reward, done, None

    def random_action(self):
        return np.random.choice(range(4))

    def reset(self):
        self.enemy = Enemy(np.random.choice(range(4)))
        self.agent = Player()
        self.coin = Coin()
        return self.get_state()

    def get_state(self):
        return np.array([self.agent.x, self.agent.y, self.enemy.x, self.enemy.y, self.coin.x, self.coin.y])

    def num_of_actions(self):
        return 4

    def len_of_state(self):
        return 6

    def close(self):
        pygame.display.quit()
        self.surface = None