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
        self.image = pygame.transform.scale(imagem_original, (88, 48))

        self.rect = self.image.get_rect()
        
        self.x = 10000
        self.y = 10000
        self.rect.topleft = (self.x, self.y)

    def reposition(self, largura_tela, altura_tela):
        limite_x = largura_tela - self.rect.width
        limite_y = altura_tela - self.rect.height

        Pos_x = randint(20, limite_x-95)
        Pos_y = randint(20, limite_y-100)
        # Gera Novamente caso tenha ficado embaixo da HUD
        while(Pos_x < 295 and Pos_y < 175):
            Pos_x = randint(20, limite_x-95)
            Pos_y = randint(20, limite_y-100)
        
        self.x = Pos_x
        self.y = Pos_y
        self.rect.topleft = (self.x, self.y)

    def draw(self, tela):
        self.rect.topleft = (self.x, self.y)
        tela.blit(self.image, self.rect)
        return self.rect

class Diamante(Coin):
    def __init__(self):
        super().__init__("diamante.png", 50)

class Moeda(Coin):
    def __init__(self):
        super().__init__("moeda.png", 10)

class Maça(Coin):
    def __init__(self):
        super().__init__("maca.png", 10)