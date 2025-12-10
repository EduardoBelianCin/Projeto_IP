import pygame
from pygame.locals import *
from math import sqrt

class Player:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.size = 30
        self.color = (150, 0, 200)
        self.speed = 5
        self.state = "Idle" # Põe a animação inicila como "Parado"
        self.direction = "Front"   # põe a direção inicial como sendo de frente

        self.sprites = sprites
        self.frame_index = 0
        self.current_sprite = self.sprites[self.state][self.direction][self.frame_index]
        self.animacao_speed = 300
        self.last_update = pygame.time.get_ticks()

    def move(self, largura, altura):
        keys = pygame.key.get_pressed()

        estado_anterior = self.state
        direção_anterior = self.direction

        VX = 0
        VY = 0
        
        if keys[K_a]:
            VX -= 1  # Move o boneco
            self.direction = "Left"   # Define para qual direção ele deve ta olhando
        if keys[K_d]:
            VX += 1
            self.direction = "Right"
        if keys[K_w]:
            VY -= 1
            self.direction = "Back"
        if keys[K_s]:
            VY += 1
            self.direction = "Front"

        if VX != 0 or VY != 0:
            self.state = "Walk"  # Se o jogador se move, a animação é "run"
        else:
            self.state = "Idle"  # Caso contrário, é "idle"

        if self.state != estado_anterior or self.direction != direção_anterior:
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

        self.update_animation()

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

    def update_animation(self):
        agora = pygame.time.get_ticks()

        if agora - self.last_update > self.animacao_speed:
            self.last_update = agora
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.state][self.direction])
        self.current_sprite = self.sprites[self.state][self.direction][self.frame_index]

    def draw(self, tela):
        tela.blit(self.current_sprite, (self.x, self.y))  # Desenha o sprite na tela

        return pygame.Rect(self.x, self.y, self.size, self.size)