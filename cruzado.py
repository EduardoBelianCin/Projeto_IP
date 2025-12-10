import pygame
from pygame.locals import *
from math import sqrt

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.color = (150, 0, 200)
        self.speed = 10

    def move(self, largura, altura):
        keys = pygame.key.get_pressed()

        VX = 0
        VY = 0
        
        if keys[K_a]:
            VX -= 1
        if keys[K_d]:
            VX += 1
        if keys[K_w]:
            VY -= 1
        if keys[K_s]:
            VY += 1

        NORMA_DO_VETOR_MOV = sqrt(VX**2 + VY**2)

        if NORMA_DO_VETOR_MOV > 0:
            VX_NORM = VX / NORMA_DO_VETOR_MOV
            VY_NORM = VY / NORMA_DO_VETOR_MOV

            self.x += VX_NORM * self.speed
            self.y += VY_NORM * self.speed


        if self.x < 0:
            self.x = 0
        if self.x > largura - self.size:
            self.x = largura - self.size
        if self.y < 0:
            self.y = 0
        if self.y > altura - self.size:
            self.y = altura - self.size

    def draw(self, tela):
        return pygame.draw.rect(tela, self.color, (self.x, self.y, self.size, self.size))