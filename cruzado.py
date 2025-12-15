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
        self.right = True   # põe a direção inicial como sendo de frente

        self.sprites = sprites
        self.frame_index = 0

        self.current_sprite = self.sprites[self.state][self.frame_index]
        
        self.animacao_speed = 300
        self.last_update = pygame.time.get_ticks()

    def move(self, largura, altura):
        keys = pygame.key.get_pressed()

        estado_anterior = self.state

        VX = 0 # Reinicia a coordenada X
        VY = 0 # Reinicia a coordenada Y
        
        if keys[K_a]:
            VX -= 1                   # Declara a coordenada de X como negativa
            self.right = False
        if keys[K_d]:
            VX += 1                   # Declara a coordenada de X como positiva
            self.right = True
        if keys[K_w]:
            VY -= 1                   # Declara a coordenada de Y como negativa
        if keys[K_s]:
            VY += 1                   # Declara a coordenada de Y como positiva

        if VX != 0 or VY != 0:
            self.state = "Walk"  # Se o jogador se move, a animação é "walk"
        else:
            self.state = "Idle"  # Caso contrário, é "idle"

        if self.state != estado_anterior:
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

        self.update_animation()

        NORMA_DO_VETOR_MOV = sqrt(VX**2 + VY**2) # Define a norma do vetor (X, Y) para corrigir a velocidade diagonal
        if NORMA_DO_VETOR_MOV > 0:
            VX_NORM = VX / NORMA_DO_VETOR_MOV    # Define a nova coordenada X corrigida para com a velocidade diagonal
            VY_NORM = VY / NORMA_DO_VETOR_MOV    # Define a nova coordenada Y corrigida para com a velocidade diagonal

            self.x += VX_NORM * self.speed       # Move o jogador na direção X
            self.y += VY_NORM * self.speed       # Move o jogador na direção Y

        if self.x < 20:
            self.x = 20
        if self.x > largura - 95:
            self.x = largura - 95
        if self.y < 0:
            self.y = 0
        if self.y > altura - 100:
            self.y = altura - 100

    def update_animation(self):
        agora = pygame.time.get_ticks()

        current_frame = self.sprites[self.state][self.frame_index]

        if agora - self.last_update > self.animacao_speed:
            self.last_update = agora
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.state])
            current_frame = self.sprites[self.state][self.frame_index]

        if self.right:
            self.current_sprite = pygame.transform.flip(current_frame, True, False)
        else:
            self.current_sprite = current_frame

    def draw(self, tela):
        tela.blit(self.current_sprite, (self.x, self.y))  # Desenha o sprite na tela

        hitbox_rect = pygame.Rect(self.x + 15, self.y + 8, 40, 60)
        return hitbox_rect
    
class Sword(pygame.sprite.Sprite):
    def __init__(self, image_path, radius, hitbox_radius):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 2)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.radius = radius
        self.hitbox_radius = hitbox_radius
        self.behind_player = False
        self.angle_rad = 0
        self.hitbox_center = (0, 0)

    def update(self, player_x, player_y, mouse_x, mouse_y):
        player_center_x = player_x + 30
        player_center_y = player_y + 40

        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        
        self.angle_rad = atan2(dy, dx)
        angle_deg = degrees(self.angle_rad)

        self.behind_player = angle_deg > 0

        offset_x = self.radius * cos(self.angle_rad)
        offset_y = self.radius * sin(self.angle_rad)

        new_x = player_center_x + offset_x
        new_y = player_center_y + offset_y

        self.image = pygame.transform.rotate(self.original_image, -(angle_deg + 135))
        self.rect = self.image.get_rect(center=(new_x, new_y))

        hitbox_offset_x = self.hitbox_radius * cos(self.angle_rad)
        hitbox_offset_y = self.hitbox_radius * sin(self.angle_rad)
        
        hitbox_center_x = player_center_x + hitbox_offset_x
        hitbox_center_y = player_center_y + hitbox_offset_y
        self.hitbox_center = (hitbox_center_x, hitbox_center_y)

    def draw(self, tela):
        tela.blit(self.image, self.rect)

        hitbox_largura = 30
        hitbox_altura = 30
        
        hitbox_rect = pygame.Rect(0, 0, hitbox_largura, hitbox_altura)
        hitbox_rect.center = (int(self.hitbox_center[0]), int(self.hitbox_center[1]))

        pygame.draw.rect(tela, (255,0,0), hitbox_rect, 2)

        return hitbox_rect