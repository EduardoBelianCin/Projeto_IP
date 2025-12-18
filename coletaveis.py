import pygame
import os
from random import randint

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_ITENS = os.path.join(PASTA_ATUAL, "sprites", "itens")

class Coin:
    def __init__(self, x, y, nome_da_imagem, pontos):
        self.value = pontos
        
        caminho = os.path.join(PASTA_ITENS, nome_da_imagem)
        
        imagem_original = pygame.image.load(caminho).convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (88, 48))

        self.sprite = pygame.image.load(f"sprites/itens/{nome_da_imagem}").convert_alpha()
        self.rect = self.sprite.get_rect()
        
        self.x = 10000
        self.y = 10000
        self.rect.topleft = (self.x, self.y)

    def reposition(self, largura_tela, altura_tela):
        limite_x = largura_tela - 30
        limite_y = altura_tela - 30

        Pos_x = randint(30, limite_x-30)
        Pos_y = randint(30, limite_y-30)
        # Gera Novamente caso tenha ficado embaixo da HUD
        while(Pos_x < 295 and Pos_y < 175):
            Pos_x = randint(30, limite_x-30)
            Pos_y = randint(30, limite_y-30)
        
        self.x = Pos_x
        self.y = Pos_y
        self.rect.topleft = (self.x, self.y)

    def draw(self, tela):
        self.rect.topleft = (self.x, self.y)
        tela.blit(self.image, self.rect)
        return self.rect
    
    def get_hitbox(self):
        hitbox_largura = 25
        hitbox_altura = 25
        hitbox_dx = 33
        hitbox_dy = 12

        return pygame.Rect(self.x + hitbox_dx, self.y + hitbox_dy, hitbox_largura, hitbox_altura)

class Diamante(Coin):
    def __init__(self, x, y):
        super().__init__(x, y, "diamante.png", 500)

class Moeda(Coin):
    def __init__(self, x, y):
        super().__init__(x, y, "moeda.png", 100)

class Maça(Coin):
    def __init__(self, x, y):
        super().__init__(x, y, "maca.png", 10)