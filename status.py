import pygame
from pygame.locals import *
from cruzado import *
from coletaveis import *
from Main import *

class Hud:
    def draw_hud(self):
            self.pontos = 0
            self.diamantes = 0
            self.moedas = 0
            self.maçãs = 0

            linha1 = self.font.render(f"Pontos: {self.pontos}", True, (255,255,255))
            linha2 = self.font.render(f"diamantes: {self.diamantes}", True, (255,255,255))
            linha3 = self.font.render(f"Moedas: {self.moedas}", True, (255,255,255))
            linha4 = self.font.render(f"maçãs: {self.maçãs}", True, (255,255,255))

            self.tela.blit(linha1, (20, 20))
            self.tela.blit(linha2, (20, 45))
            self.tela.blit(linha3, (20, 70))
            self.tela.blit(linha4, (20, 95))
