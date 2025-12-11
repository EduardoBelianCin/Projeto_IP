import pygame
import os
from pygame.locals import *
from sys import exit
from random import randint
from cruzado import Player
from coletaveis import *
from hud import Hud

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
                            img = pygame.transform.scale_by(img, 2)
                            sprites[state][direction].append(img)
        return sprites

class Game:

    def __init__(self):
        self.largura = 1920
        self.altura = 1080
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('O Cruzado Aventureiro')

        self.relogio = pygame.time.Clock()
        self.font = pygame.font.SysFont("dejavusans", 30, False, False)

        # Carregar os sprites das animações
        self.sprites = load_sprites_from_folder("sprites")

        # Criar o jogador, passando os sprites
        self.player = Player(self.largura // 2, self.altura // 2, self.sprites)

        self.cursor_customizado()

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
        self.hud_sprites = self.load_hud_sprites("sprites/hud/barra de vida")

        self.spawn_random_coin()

    def load_hud_sprites(self, arquivos):
        hud_sprites = {}
        for filename in os.listdir(arquivos):
            if filename.endswith(".png"):
                key = os.path.splitext(filename)[0]
                img = pygame.image.load(os.path.join(arquivos, filename)).convert_alpha()
                img = pygame.transform.scale(img, (270, 30))
                hud_sprites[key] = img
        return hud_sprites
    
    def cursor_customizado(self):
        self.cursor = pygame.image.load("sprites/cursor.png").convert_alpha()
        pygame.mouse.set_visible(False)

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
            self.vida = min(100, self.vida + self.item_maçã.value)
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

            Hud().draw_hud(
                self.tela,
                self.font,
                self.pontos,
                self.diamantes,
                self.moedas,
                self.maçãs,
                self.vida,
                self.hud_sprites
            )

            mouse_pos = pygame.mouse.get_pos()
            self.tela.blit(self.cursor, mouse_pos)

            pygame.display.update()

Game().run()