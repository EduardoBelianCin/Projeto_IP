import pygame
from pygame.locals import *
from sys import exit
from random import randint
from math import sqrt

pygame.init()

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


class Coin:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.radius = 10
        self.x = 10000
        self.y = 10000

    def reposition(self, largura, altura):
        self.x = randint(0, largura)
        self.y = randint(0, altura)

    def draw(self, tela):
        return pygame.draw.circle(tela, self.color, (self.x, self.y), self.radius)

class SilverCoin(Coin):
    def __init__(self):
        super().__init__((150, 150, 150), 1)

class GoldCoin(Coin):
    def __init__(self):
        super().__init__((200, 150, 0), 10)

class Ruby(Coin):
    def __init__(self):
        super().__init__((255, 0, 0), 50)


class Game:
    def __init__(self):

        self.largura = 1000
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Vovô caçando butija')

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

            self.tela.blit(self.BACKGROUND, (0, 0))

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