import pygame
from .constants import *
from .config import *
from .util import *

class GameObject:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

class Bird(GameObject):

    a = 400
    jump_v = 300

    def __init__(self, y=height/2):
        super().__init__()
        self.x = 100
        self.y = y
        self.r = 20
        self.color = RED
        self.v = 0
        self.a = Bird.a

    def draw(self, surface, color=None):
        pygame.draw.circle(surface, color if color != None else self.color, [int(self.x), int(self.y)], int(self.r))

    def update(self, dt):
        self.v += self.a * dt
        self.y += self.v * dt

    def jump(self):
        self.v = -Bird.jump_v

    def collide(self, pipe):
        return collide([pipe.x, 0, pipe.width, pipe.uy], [self.x, self.y, self.r]) or collide([pipe.x, pipe.ly, pipe.width, height - pipe.ly], [self.x, self.y, self.r]) or self.y < self.r or self.y > height - self.r 

class Pipe(GameObject): 

    def __init__(self, uy, ly, x=width):
        super().__init__()
        self.x = x
        self.uy = uy
        self.ly = ly
        self.color = GREEN
        self.width = 100
        self.v = 100

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.x, 0, self.width, self.uy])
        pygame.draw.rect(surface, self.color, [self.x, self.ly, self.width, height - self.ly])

    def update(self, dt):
        self.x -= dt * self.v