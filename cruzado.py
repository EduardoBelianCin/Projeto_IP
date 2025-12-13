import pygame
from pygame.locals import *
from math import sqrt, sin, cos, radians, atan2, degrees

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
    
class Sword(pygame.sprite.Sprite):
    def __init__(self, image_path, rotation_speed, radius):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 2)  # Ajuste o tamanho
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.rotation_speed = rotation_speed # Velocidade em graus por frame
        self.radius = radius # Raio de rotação em torno do jogador
        self.angle = 0 # Ângulo inicial em graus

    def update(self, player_x, player_y, mouse_x, mouse_y):
        player_center_x = player_x + 30 
        player_center_y = player_y + 30
        
        dx_mouse = mouse_x - player_center_x
        dy_mouse = mouse_y - player_center_y

        target_angle_rad = atan2(dy_mouse, dx_mouse)
        target_angle_deg = degrees(target_angle_rad)
        
        offset_x = self.radius * cos(target_angle_rad)
        offset_y = self.radius * sin(target_angle_rad)

        new_center_x = player_center_x + offset_x
        new_center_y = player_center_y + offset_y

        final_rotation = target_angle_deg + 225
        
        final_rotation = target_angle_deg + 180 - 45 

        self.image = pygame.transform.rotate(self.original_image, -final_rotation)

        self.rect = self.image.get_rect(center=(new_center_x, new_center_y))

    def draw(self, tela):
        tela.blit(self.image, self.rect)