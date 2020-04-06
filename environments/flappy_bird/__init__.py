from .. import Environment

import pygame
import numpy as np
import time

from .objects import Bird, Pipe
from .constants import *
from .config import *

pygame.init()
font = pygame.font.SysFont(None, 20)

class FlappyBird(Environment):
    
    def __init__(self, dbp=300, opening_dist=200, a=None, jump_v=None):
        self.pipes = []
        self.bird = Bird()
        self.current_time = time.time()
        self.score = 0
        self.dbp = dbp
        self.opening_dist = opening_dist
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Flappy Bird')
        if a != None:
            Bird.a = a
        if jump_v != None:
            Bird.jump_v = jump_v
        for i in range(int(width / dbp) + 1):
            uy = np.random.random() * (height - opening_dist)
            ly = np.random.random() * 50 - 25 + opening_dist + uy
            self.pipes.append(Pipe(uy, ly, width + dbp * i))

    def render(self):

        self.surface.fill(WHITE)

        self.bird.draw(self.surface)
        for pipe in self.pipes:
            pipe.draw(self.surface)

    def step(self, action):
        reward = 0
        done = False
        if action == 1:
            self.bird.jump()

        dt = time.time() - self.current_time

        self.bird.update(dt)

        for pipe in self.pipes:
            pipe.update(dt)
            if self.bird.collide(pipe):
                done = True

        if self.pipes[0].x < -self.pipes[0].width:
            self.score += 1
            reward = 1
            self.pipes.pop(0)
            uy = np.random.random() * (height - opening_dist)
            ly = np.random.random() * 50 - 25 + opening_dist + uy
            self.pipes.append(Pipe(uy, ly, self.pipes[len(pipes) - 1].x + self.dbp))

        self.surface.blit(font.render("Score: " + str(self.score), True, BLACK), [10, 10])
        pygame.display.update()

        self.current_time += dt

        return self.get_state(), reward, done, None

    def random_action(self):
        return 1 if np.random.random() < 0.05 else 0

    def reset(self):
        self.pipes = []
        self.bird = Bird()
        self.current_time = time.time()
        self.score = 0
        for i in range(int(width / self.dbp) + 1):
            uy = np.random.random() * (height - self.opening_dist)
            ly = np.random.random() * 50 - 25 + self.opening_dist + uy
            self.pipes.append(Pipe(uy, ly, width + self.dbp * i))
        return self.get_state()

    def get_state(self):
        for i in range(len(self.pipes) - 1):
            if self.pipes[i].x + self.pipes[i].width > self.bird.x:
                return ((self.pipes[i].x - self.bird.x) / width, (self.pipes[i].uy - self.bird.y) / width, (self.pipes[i].ly - self.bird.y) / width, (self.pipes[i + 1].x - self.bird.x) / width, (self.pipes[i + 1].uy - self.bird.y) / width, (self.pipes[i + 1].ly - self.bird.y) / width, 2 * self.bird.v / height)

    def num_of_actions(self):
        return 2

    def len_of_state(self):
        return 7

    def close(self):
        pygame.quit()