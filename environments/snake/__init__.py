from .. import Environment

import pygame
import numpy as np
import time

from .objects import *
from .constants import *
from .config import *

pygame.init()
font = pygame.font.SysFont(None, 20)

class SnakeGame(Environment):

    sight_range = 3

    def __init__(self):
        super().__init__()
        self.score = 0
        self.snake = Snake()
        self.apple = Apple.random(self.snake)
        self.surface = None

    def render(self):

        if self.surface == None:
            self.surface = pygame.display.set_mode((width, height))
            pygame.display.set_caption('Snake Game')

        self.surface.fill(WHITE)

        self.apple.draw(self.surface)
        self.snake.draw(self.surface)

        self.surface.blit(font.render("Score: " + str(self.score), True, BLACK), [10, 10])
        pygame.display.update()

    def step(self, action):
        self.snake.direction = action
        self.snake.update()
        reward = -1
        done = False
        if self.snake.head.collide(self.apple):
            self.snake.eat_apple()
            self.apple = Apple.random(self.snake)
            self.score += 1
            reward = 100
        if self.snake.head.x < 0 or self.snake.head.y < 0 or self.snake.head.x >= width / Block.w or self.snake.head.y >= height / Block.h:
            done = True
            reward = -1000
        else:
            for block in self.snake.blocks:
                if block.collide(self.snake.head) and self.snake.head != block:
                    done = True
                    reward = -1000
                    continue

        return self.get_state(), reward, done, None

    def random_action(self):
        return np.random.choice([0, 1, 2, 3])

    def reset(self):
        self.score = 0
        self.snake = Snake()
        self.apple = Apple.random(self.snake)
        return self.get_state()

    def get_state(self):
        state = [self.apple.x, self.apple.y, self.snake.head.x, self.snake.head.y]
        block_positions = set()
        for block in self.snake.blocks:
            block_positions.add((block.x, block.y))
        sight_range = SnakeGame.sight_range
        for x in range(-sight_range, sight_range + 1):
            for y in range(-sight_range, sight_range + 1):
                s = -int((self.snake.head.x + x, self.snake.head.y + y) in block_positions)
                if s == 0 and self.snake.head.x + x == self.apple.x and self.snake.head.y + y == self.apple.y:
                    s = 1
                state.append(s)
        return state

    def num_of_actions(self):
        return 4

    def len_of_state(self):
        return (SnakeGame.sight_range * 2 + 1) ** 2 + 4

    def close(self):
        pygame.display.quit()
        self.surface = None