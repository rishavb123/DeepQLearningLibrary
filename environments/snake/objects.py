import pygame
import random

from .config import *
from .constants import *

class GameObject:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        pass

    def draw(self, surface):
        pass

class Block:

    w, h = 10, 10

    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.x * Block.w, self.y * Block.h, Block.w, Block.h])

    def copy(self):
        return Block(self.x, self.y, self.color)
    
    def collide(self, block):
        return block.x == self.x and block.y == self.y

class Snake:

    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self):
        super().__init__()
        self.head = Block(width / (2 * Block.w), height / (2 * Block.h), GREEN)
        self.blocks = [self.head]
        self.direction = 0
        self.tail = None

    def update(self):
        self.tail = self.blocks.pop()
        new_head = self.tail.copy()
        dx, dy = Snake.get_movements(self.direction)
        new_head.x = self.head.x + dx
        new_head.y = self.head.y + dy
        self.head = new_head
        self.blocks.insert(0, self.head)

    def eat_apple(self):
        self.blocks.append(self.tail)

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

    @staticmethod
    def get_movements(direction):
        if direction == Snake.LEFT:
            return -1, 0
        elif direction == Snake.UP:
            return 0, -1
        elif direction == Snake.RIGHT:
            return 1, 0
        elif direction == Snake.DOWN:
            return 0, 1

class Apple(Block):

    def __init__(self, x, y):
        super().__init__(x, y, RED)

    @staticmethod
    def random(snake):
        a = Apple(random.randrange(0, width / Block.w), random.randrange(0, height / Block.h))
        for block in snake.blocks:
            if a.collide(block):
                return Apple.random()
        return a