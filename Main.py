import pygame
import os
from pygame.locals import *
from sys import exit
from random import randint, choice
from cruzado import *
from coletaveis import *
from hud import Hud
from inimigos import *

pygame.init()
pygame.mixer.init()

som_maca = pygame.mixer.Sound("Audios/Successo.wav")
som_moeda = pygame.mixer.Sound("Audios/SuccessInfographic.ogg")
som_dima = pygame.mixer.Sound("Audios/Success_3.wav")
som_maca.set_volume(0.2)
som_moeda.set_volume(0.2)
som_dima.set_volume(0.2)
spawn_item_event = pygame.USEREVENT + 1
intervalo_spawn = 3000
classes_coletaveis = [Diamante, Moeda, Maça]

def load_sprites_from_folder(folder):    # Animação do templário
        sprites = {}

        templario_folder = os.path.join(folder, "templario")

        for state in ['Idle', 'Walk']:
            sprites[state] = []

            state_folder = os.path.join(templario_folder, state)

            if os.path.exists(state_folder):
                filenames = [f for f in os.listdir(state_folder) if f.endswith(".png")]

                for filename in filenames:
                    img = pygame.image.load(os.path.join(state_folder, filename)).convert_alpha()
                    img = pygame.transform.scale_by(img, 2)
                    sprites[state].append(img)
        return sprites

class Game:

    def __init__(self):

        info = pygame.display.Info()
        self.largura_desktop = info.current_w
        self.altura_desktop = info.current_h
        self.tela = pygame.display.set_mode((self.largura_desktop, self.altura_desktop), pygame.NOFRAME)
        self.largura, self.altura = self.tela.get_size()

        pygame.display.set_caption('A Lenda da Cruzada')
        pygame.display.set_icon(pygame.image.load('icone_teste.png'))

        self.relogio = pygame.time.Clock()
        self.font = pygame.font.SysFont("dejavusans", 30, False, False)

        # Carregar os sprites das animações
        self.sprites = load_sprites_from_folder("sprites")
        # Criar o jogador, passando os sprites
        self.player = Player(self.largura // 2, self.altura // 2, self.sprites)

        Hud().cursor_customizado()

        self.coletaveis_ativos = []

        ## ".convert()" ou ".convert_alpha()" melhora MUITO o desempenho das imagens e sprites, sem ele a performance cai.
        self.BACKGROUND = pygame.image.load("Background_Game.png").convert_alpha()   # Importa a imagem de background
        self.BACKEST = pygame.transform.scale(self.BACKGROUND, (self.largura, self.altura)) # Estica a imagem para o tamanho da janela
        self.BACKBOTTOM = pygame.image.load("Background_Game_Bottom.png").convert_alpha() ## Importa a imagem inferior para adicionar profundidade
        self.BOTTOMEST = pygame.transform.scale(self.BACKBOTTOM, (self.largura, 60))
        self.BACKLAT = pygame.image.load("Background_Game_Laterals.png").convert_alpha() ## Importa a imagem das laterais para adicionar profundidade
        self.LATTEST = pygame.transform.scale(self.BACKLAT, (self.largura, self.altura))

        self.pontos = 0
        self.diamantes = 0
        self.moedas = 0
        self.maçãs = 0

        self.vida = 50
        self.hud_sprites = Hud().load_hud_sprites("sprites/hud/barra de vida")

        self.FULLSCREEN = False

        pygame.time.set_timer(spawn_item_event, intervalo_spawn)

        self.hud_sprites = Hud().load_hud_sprites("sprites/hud/barra de vida")

        self.FULLSCREEN = False

        self.spawn_random_coin()
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
        self.sword = Sword('sprites/templario/espada.png', 60, 90)
        self.sword.update(self.player.x, self.player.y, mouse_x, mouse_y)
        sword_rect = self.sword.rect
        self.sword.draw(self.tela)

    def spawn_random_coin(self):
        classe_do_novo_item = choice(classes_coletaveis)
        novo_item = classe_do_novo_item(0,0)
        novo_item.reposition(self.largura, self.altura)
        self.coletaveis_ativos.append(novo_item)

    def check_collisions(self, templário, sword_rect):
        # Ação de coleta dos itens
        coletados = [] # Lista para marcar itens que devem ser removidos

        for item in self.coletaveis_ativos:
            hitbox_item = item.get_hitbox()
            
            # Ação de coleta (Colisão entre Jogador e Item)
            if templário.colliderect(hitbox_item):
                if isinstance(item, Diamante):
                    self.diamantes += 1
                    self.pontos += item.value
                    som_dima.play()
                elif isinstance(item, Moeda):
                    self.moedas += 1
                    self.pontos += item.value
                    som_moeda.play()
                elif isinstance(item, Maça):
                    self.maçãs += 1
                    self.vida = min(100, self.vida + item.value) 
                    som_maca.play()
                coletados.append(item) # Marca para remoção

            # Ação de destruir (Colisão entre Espada e Item)
            if sword_rect.colliderect(hitbox_item):
                coletados.append(item) # Marca para remoção
        
        # Remove os itens coletados ou destruídos da lista de ativos
        for item in coletados:
            if item in self.coletaveis_ativos:
                self.coletaveis_ativos.remove(item)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos

            self.relogio.tick(30)

            self.tela.fill((0, 0, 0))
            self.tela.blit(self.BACKEST, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == spawn_item_event:
                    self.spawn_random_coin()

            self.player.move(self.largura, self.altura)
            self.sword.update(self.player.x, self.player.y, mouse_x, mouse_y)
            self.rect = self.sword.draw(self.tela)
            for item in self.coletaveis_ativos:
                 item.draw(self.tela)

            # Ordem de desenho (profundidade)
            if self.sword.behind_player:
                templário = self.player.draw(self.tela)
                self.sword.draw(self.tela)
            else:
                self.sword.draw(self.tela)
                templário = self.player.draw(self.tela)
            #EXIBIÇÃO APENAS PARA VISUALIZAR-----------------------------------------------------
            # pygame.draw.rect(self.tela, (255, 0, 0), self.sword.draw(self.tela), 2)
            # pygame.draw.rect(self.tela, (255, 0, 0), templário, 2)
            # for item in self.coletaveis_ativos:
            #     pygame.draw.rect(self.tela, (255,0,0), item.get_hitbox(), 2)

            self.check_collisions(templário, self.rect)
            
            self.tela.blit(self.BOTTOMEST, (0, self.altura-60))
            self.tela.blit(self.LATTEST, (0, 0))

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
            self.tela.blit(Hud().cursor_customizado(), mouse_pos)

            pygame.display.update()

Game().run()