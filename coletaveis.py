import pygame
import os
from random import randint

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_ITENS = os.path.join(PASTA_ATUAL, "sprites", "itens")

class Coin:
    def __init__(self, nome_da_imagem, pontos):
        self.value = pontos
        
        caminho = os.path.join(PASTA_ITENS, nome_da_imagem)
        
        imagem_original = pygame.image.load(caminho).convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (32, 32))
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        
        self.x = 10000
        self.y = 10000
        self.rect.topleft = (self.x, self.y)

    def reposition(self, largura_tela, altura_tela):
        limite_x = largura_tela - self.rect.width
        limite_y = altura_tela - self.rect.height
        
        self.x = randint(0, limite_x)
        self.y = randint(0, limite_y)
        self.rect.topleft = (self.x, self.y)

    def draw(self, tela):
        self.rect.topleft = (self.x, self.y)
        tela.blit(self.image, self.rect)
        return self.rect

class SilverCoin(Coin):
    def __init__(self):
        super().__init__("diamante.png", 1)

class GoldCoin(Coin):
    def __init__(self):
        super().__init__("moeda.png", 10)

class Ruby(Coin):
    def __init__(self):
        super().__init__("maca.png", 50)