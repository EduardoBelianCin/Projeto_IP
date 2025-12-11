import pygame
import os
from pygame.locals import *
from sys import exit
from random import randint
from cruzado import Player
from coletaveis import *

pygame.init()

def load_sprites_from_folder(folder):
        directions = ['Back', 'Front', 'Left', 'Right']
        sprites = {}

        for state in ['Idle', 'Walk']:
            sprites[state] = {}


            for direction in directions:
                direction_folder = os.path.join(folder, state, direction)
                sprites[state][direction] = []

                if os.path.exists(direction_folder):
                    for filename in os.listdir(direction_folder):
                        if filename.endswith(".png"):
                            img = pygame.image.load(os.path.join(direction_folder, filename))
                            sprites[state][direction].append(img)
        return sprites

class Game:

    def __init__(self):
        self.largura = 1000
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('O Cruzado Aventureiro')

        self.relogio = pygame.time.Clock()
        self.font = pygame.font.SysFont("TimesNewRoman", 20, True, False)

        # Carregar os sprites das animações
        self.sprites = load_sprites_from_folder("sprites")

        # Criar o jogador, passando os sprites
        self.player = Player(self.largura // 2, self.altura // 2, self.sprites)

        self.item_diamante = Diamante()
        self.item_moeda = Moeda()
        self.item_maçã = Maça()

        self.BACKGROUND = pygame.image.load("Background_Game.png")                                 # Importa a imagem de background
        self.BACKEST = pygame.transform.scale(self.BACKGROUND, (self.largura, self.altura)) # Estica a imagem para o tamanho da janela

        self.pontos = 0
        self.diamantes = 0
        self.moedas = 0
        self.maçãs = 0
        self.vida = 100

        self.spawn_random_coin()

    def draw_hud(self):

        linha1 = self.font.render(f"Pontos: {self.pontos}", True, (255,255,255))
        linha2 = self.font.render(f"diamantes: {self.diamantes}", True, (255,255,255))
        linha3 = self.font.render(f"Moedas: {self.moedas}", True, (255,255,255))
        linha4 = self.font.render(f"maçãs: {self.maçãs}", True, (255,255,255))

        self.tela.blit(linha1, (20, 20))
        self.tela.blit(linha2, (20, 45))
        self.tela.blit(linha3, (20, 70))
        self.tela.blit(linha4, (20, 95))

    def spawn_random_coin(self):
        sorteio = randint(0, 20)

        self.item_diamante.x = self.item_diamante.y = 10000
        self.item_moeda.x = self.item_moeda.y = 10000
        self.item_maçã.x = self.item_maçã.y = 10000

        if sorteio in range(14, 21):
            self.item_maçã.reposition(self.largura, self.altura)
        elif sorteio in range(7, 21):
            self.item_moeda.reposition(self.largura, self.altura)
        else:
            self.item_diamante.reposition(self.largura, self.altura)

    def check_collisions(self, templário):
        if templário.colliderect(pygame.Rect(self.item_diamante.x+20, self.item_diamante.y, 10, 10)):
            self.diamantes += 1
            self.pontos += self.item_diamante.value
            self.spawn_random_coin()

        if templário.colliderect(pygame.Rect(self.item_moeda.x+20, self.item_moeda.y, 10, 10)):
            self.moedas += 1
            self.pontos += self.item_moeda.value
            self.spawn_random_coin()

        if templário.colliderect(pygame.Rect(self.item_maçã.x+20, self.item_maçã.y, 10, 10)):
            self.maçãs += 1
            self.pontos += self.item_maçã.value
            self.spawn_random_coin()

    def run(self):
        while True:
            self.relogio.tick(30)

            self.tela.fill((0, 0, 0))

            self.tela.blit(self.BACKEST, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            self.player.move(self.largura, self.altura)
            templário = self.player.draw(self.tela)

            s = self.item_diamante.draw(self.tela)
            g = self.item_moeda.draw(self.tela)
            r = self.item_maçã.draw(self.tela)

            self.check_collisions(templário)

            self.draw_hud()

            pygame.display.update()

Game().run()