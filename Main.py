import pygame
from pygame.locals import *
from sys import exit
from random import randint
from cruzado import Player
from coletaveis import *

pygame.init()

class Game:
    def __init__(self):

        self.largura = 1000
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('O Cruzado Aventureiro')

        self.relogio = pygame.time.Clock()
        self.font = pygame.font.SysFont("TimesNewRoman", 20, False, False)

        self.player = Player(self.largura // 2, self.altura // 2)

        self.silver = SilverCoin()
        self.gold = GoldCoin()
        self.ruby = Ruby()

        self.pontos = 0
        self.moedas_prata = 0
        self.moedas_ouro = 0
        self.rubis = 0

        self.BACKGROUND = pygame.image.load("sample1.png")
        self.BACKGROUNDESTICADO = pygame.transform.scale(self.BACKGROUND, (self.largura, self.altura))

        self.spawn_random_coin()

    def spawn_random_coin(self):
        sorteio = randint(0, 20)

        self.silver.x = self.silver.y = 10000
        self.gold.x = self.gold.y = 10000
        self.ruby.x = self.ruby.y = 10000

        if sorteio in range(15, 21):
            self.ruby.reposition(self.largura, self.altura)
        elif sorteio in range(10, 21):
            self.gold.reposition(self.largura, self.altura)
        else:
            self.silver.reposition(self.largura, self.altura)

    def check_collisions(self, prot):
        if prot.colliderect(pygame.Rect(self.silver.x-10, self.silver.y-10, 20, 20)):
            self.moedas_prata += 1
            self.pontos += self.silver.value
            self.spawn_random_coin()

        if prot.colliderect(pygame.Rect(self.gold.x-10, self.gold.y-10, 20, 20)):
            self.moedas_ouro += 1
            self.pontos += self.gold.value
            self.spawn_random_coin()

        if prot.colliderect(pygame.Rect(self.ruby.x-10, self.ruby.y-10, 20, 20)):
            self.rubis += 1
            self.pontos += self.ruby.value
            self.spawn_random_coin()

    def draw_hud(self):
        linha1 = self.font.render(f"Pontos: {self.pontos}", True, (255,255,255))
        linha2 = self.font.render(f"Moedas de prata: {self.moedas_prata}", True, (255,255,255))
        linha3 = self.font.render(f"Moedas de ouro: {self.moedas_ouro}", True, (255,255,255))
        linha4 = self.font.render(f"Rubis: {self.rubis}", True, (255,255,255))

        self.tela.blit(linha1, (20, 20))
        self.tela.blit(linha2, (20, 45))
        self.tela.blit(linha3, (20, 70))
        self.tela.blit(linha4, (20, 95))

    def run(self):
        while True:
            self.relogio.tick(30)

            self.tela.fill((0, 0, 0))

            self.tela.blit(self.BACKGROUNDESTICADO, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            self.player.move(self.largura, self.altura)
            prot = self.player.draw(self.tela)

            s = self.silver.draw(self.tela)
            g = self.gold.draw(self.tela)
            r = self.ruby.draw(self.tela)

            self.check_collisions(prot)

            self.draw_hud()

            pygame.display.update()

Game().run()