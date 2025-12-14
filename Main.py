import pygame
import os
from pygame.locals import *
from sys import exit
from random import randint
from cruzado import *
from coletaveis import *
from hud import Hud

pygame.init()

def load_sprites_from_folder(folder):    # Animação do templário
        directions = ['Back', 'Front', 'Left', 'Right']
        sprites = {}

        templario_folder = os.path.join(folder, "templario")

        for state in ['Idle', 'Walk']:
            sprites[state] = {}

            for direction in directions:
                direction_folder = os.path.join(templario_folder, state, direction)
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

        info = pygame.display.Info()
        largura_desktop = info.current_w
        altura_desktop = info.current_h
        self.tela = pygame.display.set_mode((largura_desktop, altura_desktop), pygame.NOFRAME)
        self.largura, self.altura = self.tela.get_size()

        pygame.display.set_caption('O Cruzado Aventureiro')
        pygame.display.set_icon(pygame.image.load('icone_teste.png'))

        self.relogio = pygame.time.Clock()
        self.font = pygame.font.SysFont("dejavusans", 30, False, False)

        # Carregar os sprites das animações
        self.sprites = load_sprites_from_folder("sprites")
        # Criar o jogador, passando os sprites
        self.player = Player(self.largura // 2, self.altura // 2, self.sprites)

        Hud().cursor_customizado()

        self.item_diamante = Diamante()
        self.item_moeda = Moeda()
        self.item_maçã = Maça()

        self.BACKGROUND = pygame.image.load("Background_Game.png")   # Importa a imagem de background
        self.BACKEST = pygame.transform.scale(self.BACKGROUND, (self.largura, self.altura)) # Estica a imagem para o tamanho da janela

        self.pontos = 0
        self.diamantes = 0
        self.moedas = 0
        self.maçãs = 0

        self.vida = 100
        self.hud_sprites = Hud().load_hud_sprites("sprites/hud/barra de vida")

        self.FULLSCREEN = False

        self.spawn_random_coin()

        self.hud_sprites = Hud().load_hud_sprites("sprites/hud/barra de vida")

        self.FULLSCREEN = False

        self.spawn_random_coin()
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
        self.sword = Sword('sprites/templario/espada.png', 10, 80)
        self.sword.update(self.player.x, self.player.y, mouse_x, mouse_y)
        sword_rect = self.sword.rect
        self.sword.draw(self.tela)

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

    def check_collisions(self, templário):    # Ação de coleta dos itens
        if templário.colliderect(pygame.Rect(self.item_diamante.x+40, self.item_diamante.y, 10, 20)):
            self.diamantes += 1
            self.pontos += self.item_diamante.value
            self.spawn_random_coin()

        if templário.colliderect(pygame.Rect(self.item_moeda.x+40, self.item_moeda.y, 10, 20)):
            self.moedas += 1
            self.pontos += self.item_moeda.value
            self.spawn_random_coin()

        if templário.colliderect(pygame.Rect(self.item_maçã.x+40, self.item_maçã.y, 10, 20)):
            self.maçãs += 1
            self.vida = min(100, self.vida + self.item_maçã.value)
            self.spawn_random_coin()

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos

            keysrun = pygame.key.get_pressed()

            if keysrun[K_F11]:
                if self.FULLSCREEN==False:
                    self.BACKEST = pygame.transform.scale(self.BACKGROUND, (self.largura, self.altura)) 
                    self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.FULLSCREEN)
                    self.FULLSCREEN=True

                    while(bool(self.tela.get_flags() & pygame.FULLSCREEN)==False):
                        self.FULLSCREEN=True
                elif self.FULLSCREEN==True:
                    self.BACKEST = pygame.transform.scale(self.BACKGROUND, (self.largura, self.altura)) 
                    self.tela = pygame.display.set_mode((self.largura, self.altura))
                    self.FULLSCREEN=False
                    
                    while(bool(self.tela.get_flags() & pygame.FULLSCREEN)==True):
                        self.FULLSCREEN=False

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

            self.sword.update(self.player.x, self.player.y, mouse_x, mouse_y)
            sword_rect = self.sword.rect
            self.sword.draw(self.tela)

            mouse_pos = pygame.mouse.get_pos()
            self.tela.blit(Hud().cursor_customizado(), mouse_pos)

            pygame.display.update()

Game().run()