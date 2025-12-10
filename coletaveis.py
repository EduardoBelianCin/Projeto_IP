import pygame
from pygame.locals import *
from random import randint

class Coin:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.radius = 10
        self.x = 10000
        self.y = 10000

    def reposition(self, largura, altura):
        self.x = randint(0, largura)
        self.y = randint(0, altura)

    def draw(self, tela):
        return pygame.draw.circle(tela, self.color, (self.x, self.y), self.radius)

class SilverCoin(Coin):
    def __init__(self):
        super().__init__((150, 150, 150), 1)

class GoldCoin(Coin):
    def __init__(self):
        super().__init__((200, 150, 0), 10)

class Ruby(Coin):
    def __init__(self):
        super().__init__((255, 0, 0), 50)