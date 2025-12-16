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

# Som de Vitória 
som_vitoria = pygame.mixer.Sound("Audios/victory.mp3")
som_vitoria.set_volume(0.5)

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

        ##".convert()" ou ".convert_alpha()" melhora MUITO o desempenho das imagens e sprites, sem ele a performance cai.
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

        #  Variáveis de Controle
        self.fim_de_jogo = False
        self.inicio_vitoria_tempo = 0
        self.sprites_vitoria = self.sprites.get('Walk', []) 
        self.frame_animacao = 0
        self.timer_animacao = 0
        
        # Botão Jogar Novamente
        self.botao_rect = pygame.Rect(0, 0, 300, 60)
        self.botao_rect.center = (self.largura // 2, self.altura // 2 + 200)
        
    def reiniciar_jogo(self):
        """Reinicia o jogo resetando todas as variáveis"""
        self.pontos = 0
        self.diamantes = 0
        self.moedas = 0
        self.maçãs = 0
        self.vida = 50
        self.fim_de_jogo = False
        self.inicio_vitoria_tempo = 0
        self.frame_animacao = 0
        self.timer_animacao = 0
        self.coletaveis_ativos.clear()
        self.spawn_random_coin()
        # Reposicionar o jogador
        self.player.x = self.largura // 2
        self.player.y = self.altura // 2
        
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

    #  Função da Tela de Vitória 
    def exibir_vitoria(self, mouse_pos):
        self.tela.fill((20, 20, 40))
        agora = pygame.time.get_ticks()
        if agora - self.timer_animacao > 100:
            self.frame_animacao = (self.frame_animacao + 1) % len(self.sprites_vitoria)
            self.timer_animacao = agora
        sprite = self.sprites_vitoria[self.frame_animacao]
        sprite_grande = pygame.transform.scale_by(sprite, 2.5)
        rect_sprite = sprite_grande.get_rect(center=(self.largura // 2, self.altura // 2 + 60))
        self.tela.blit(sprite_grande, rect_sprite)
        
        fonte_tit = pygame.font.SysFont("Arial", 60, True)
        fonte_sub = pygame.font.SysFont("Arial", 30, True)
        txt1 = fonte_tit.render("Parabéns, Cavaleiro!", True, (255, 215, 0))
        txt2 = fonte_sub.render("Você coletou os 1000 pontos!", True, (255, 255, 255))
        self.tela.blit(txt1, txt1.get_rect(center=(self.largura/2, self.altura/2 - 140)))
        self.tela.blit(txt2, txt2.get_rect(center=(self.largura/2, self.altura/2 - 70)))
        
        # Desenhar botão "Jogar Novamente"
        cor_botao = (50, 150, 50) if self.botao_rect.collidepoint(mouse_pos) else (30, 100, 30)
        
        pygame.draw.rect(self.tela, cor_botao, self.botao_rect, border_radius=10)
        pygame.draw.rect(self.tela, (255, 215, 0), self.botao_rect, 3, border_radius=10)
        
        fonte_botao = pygame.font.SysFont("Arial", 35, True)
        txt_botao = fonte_botao.render("Jogar Novamente", True, (255, 255, 255))
        txt_rect = txt_botao.get_rect(center=self.botao_rect.center)
        self.tela.blit(txt_botao, txt_rect)
    
    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos

            self.relogio.tick(30)
            tempo_atual = pygame.time.get_ticks() # Precisa disso para o timer

            # adicionei o cheque de vitoria 
            if self.pontos >= 100 and not self.fim_de_jogo:
                self.fim_de_jogo = True
                self.inicio_vitoria_tempo = tempo_atual
                som_vitoria.play()
            
            if self.fim_de_jogo:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    
                    # Detectar clique no botão (apenas com botão esquerdo do mouse)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if self.botao_rect.collidepoint(event.pos):
                            self.reiniciar_jogo()
                
                self.exibir_vitoria(mouse_pos)
                
                # Desenhar cursor customizado na tela de vitória
                self.tela.blit(Hud().cursor_customizado(), mouse_pos)
            else:
            # (DAQUI PARA BAIXO É O CÓDIGO ORIGINAL, SÓ INDENTADO)

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