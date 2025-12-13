import pygame
from pygame.locals import *
from math import sqrt

class Player:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.size = 60
        self.color = (150, 0, 200)
        self.speed = 10
        self.state = "Idle"        # Põe a animação inicila como "Parado"
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

        VX = 0 # Reinicia a coordenada X
        VY = 0 # Reinicia a coordenada Y
        
        if keys[K_a]:
            VX -= 1                   # Declara a coordenada de X como negativa
            self.direction = "Left"   # Define para qual direção ele deve ta olhando
        if keys[K_d]:
            VX += 1                   # Declara a coordenada de X como positiva
            self.direction = "Right"
        if keys[K_w]:
            VY -= 1                   # Declara a coordenada de Y como negativa
            self.direction = "Back"
        if keys[K_s]:
            VY += 1                   # Declara a coordenada de Y como positiva
            self.direction = "Front"

        if VX != 0 or VY != 0:
            self.state = "Walk"  # Se o jogador se move, a animação é "run"
        else:
            self.state = "Idle"  # Caso contrário, é "idle"

        if self.state != estado_anterior or self.direction != direção_anterior:
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

        self.update_animation()

        NORMA_DO_VETOR_MOV = sqrt(VX**2 + VY**2) # Define a norma do vetor (X, Y) para corrigir a velocidade diagonal
        if NORMA_DO_VETOR_MOV > 0:
            VX_NORM = VX / NORMA_DO_VETOR_MOV    # Define a nova coordenada X corrigida para com a velocidade diagonal
            VY_NORM = VY / NORMA_DO_VETOR_MOV    # Define a nova coordenada Y corrigida para com a velocidade diagonal

            self.x += VX_NORM * self.speed       # Move o jogador na direção X
            self.y += VY_NORM * self.speed       # Move o jogador na direção Y

        if self.x < 5:
            self.x = 5
        if self.x > largura - 80:
            self.x = largura - 80
        if self.y < 0:
            self.y = 0
        if self.y > altura - 100:
            self.y = altura - 100

    def update_animation(self):
        agora = pygame.time.get_ticks()

        if agora - self.last_update > self.animacao_speed:
            self.last_update = agora
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.state][self.direction])
        self.current_sprite = self.sprites[self.state][self.direction][self.frame_index]

    def draw(self, tela):
        tela.blit(self.current_sprite, (self.x, self.y))  # Desenha o sprite na tela

        return pygame.Rect(self.x, self.y, self.size, self.size)