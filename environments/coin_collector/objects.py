import pygame
import numpy as np

from .config import *
from .constants import *

class Box:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def collides(self, box):
        if (self.x < box.x and self.x + self.w > box.x) or (self.x < box.x + box.w and self.x + self.w > box.x + box.w):
            if (self.y < box.y and self.y + self.h > box.y) or (self.y < box.y + box.h and self.y + self.h > box.y + box.h):
                return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [int(self.x), int(self.y), int(self.w), int(self.h)])

    def update(self):
        if self.x + self.w > width:
            self.x = 0
        elif self.x < 0:
            self.x = width - self.w
        if self.y + self.h > height:
            self.y = 0
        elif self.y < 0:
            self.y = height - self.h


class Enemy(Box):

    def __init__(self, corner):
        super().__init__(0 if corner < 2 else width * 0.9, 0 if corner in [0, 2] else height - 0.1 * width, 0.1 * width, 0.1 * width,  RED)
        self.v = 2

    def update(self, player):

        dx = 0
        dy = 0

        if np.random.random() < 0.3:
            dx = -1 if np.random.random() < 0.5 else 1
            dy = -1 if np.random.random() < 0.5 else 1
        else:
            dx = (player.x - self.x) / abs(self.x - player.x)
            dy = (player.y - self.y) / abs(self.y - player.y)

        dx *= self.v
        dy *= self.v

        self.x += dx
        self.y += dy

        super().update()

class Player(Box):

    def __init__(self):
        super().__init__(width / 2 - 0.025 * width, height / 2 - 0.025 * width, 0.05 * width, 0.05 * width,  BLUE)
        self.v = 5

    def update(self, action):

        if action == 0:
            dx = 1
            dy = 0
        elif action == 1:
            dx = -1
            dy = 0
        elif action == 2:
            dx = 0
            dy = 1
        elif action == 3:
            dx = 0
            dy = -1

        dx *= self.v
        dy *= self.v

        self.x += dx
        self.y += dy

        super().update()

class Coin(Box):

    def __init__(self):
        super().__init__(np.random.random() * 0.95 * width, np.random.random() * (height - 0.05 * width), 0.05 * width, 0.05 * width, YELLOW)
