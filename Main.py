import pygame
import os
from pygame.locals import *
from sys import exit
from random import randint, choice
from cruzado import *
from coletaveis import *
from hud import Hud
from inimigos import *
from time import sleep as slp

from inimigos import GerenciadorInimigos

pygame.init()
pygame.mixer.init()

canalbruxa = pygame.mixer.Channel(1)
canalmorcego = pygame.mixer.Channel(2)

som_maca = pygame.mixer.Sound("Audios/Successo.wav")
som_moeda = pygame.mixer.Sound("Audios/SuccessInfographic.ogg")
som_dima = pygame.mixer.Sound("Audios/Success_3.wav")

som_espada_hit = pygame.mixer.Sound("Audios/sword_hit.mp3")
som_espada_hit.set_volume(1)


## Sons de inimigos:
som_bruxa_morte = pygame.mixer.Sound("Audios/Grito_Bruxa.mp3")
som_bruxa_morte.set_volume(0.4)
som_bruxa_riso  = pygame.mixer.Sound("Audios/Riso_Bruxa.mp3")
som_bruxa_riso.set_volume(0.4)
som_fogo_ataque = pygame.mixer.Sound("Audios/Som_Fogo_Ataque.mp3")
som_fogo_ataque.set_volume(0.4)
som_bruxa_voo = pygame.mixer.Sound("Audios/Bruxa_voo.mp3")
som_bruxa_voo.set_volume(0.2)

som_morcego_morte = pygame.mixer.Sound("Audios/Morcego_morte.mp3")
som_morcego_morte.set_volume(0.5)
som_morcego_voo = pygame.mixer.Sound("Audios/Morcego_voo.mp3")
som_morcego_voo.set_volume(0.3)

som_demo_spawn = pygame.mixer.Sound("Audios/audiodemo.wav")
som_demo_spawn.set_volume(0.05)

som_boss = pygame.mixer.Sound("Audios/inicioboss.mp3")
som_boss.set_volume(0.1)

# Som de Vitória ---
som_vitoria = pygame.mixer.Sound("Audios/victory.mp3")
som_vitoria.set_volume(1)

# Som de Derrota ---
som_derrota = pygame.mixer.Sound("Audios/derrota.mp3")
som_derrota.set_volume(1)


# Música de fundo do menu
pygame.mixer.music.load("Audios/menu_music.mp3")
pygame.mixer.music.set_volume(0.5)
musica_menu_disponivel = True

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

        self.boss = None
        self.boss_vivo = False
        self.boss_derrotado = False

        self.cursor = Hud().cursor_customizado()

        self.img_menu = pygame.image.load("telas/menu.png").convert_alpha()
        self.img_vitoria = pygame.image.load("telas/vitoria.png").convert_alpha()
        self.img_derrota = pygame.image.load("telas/derrota.png").convert_alpha()
        self.img_logo = pygame.image.load("telas/logo.png").convert_alpha()
        self.img_menu = pygame.transform.scale(self.img_menu, (self.largura, self.altura))
        self.img_vitoria = pygame.transform.scale(self.img_vitoria, (self.largura, self.altura))
        self.img_derrota = pygame.transform.scale(self.img_derrota, (self.largura, self.altura))
        self.img_logo = pygame.transform.scale(self.img_logo, (self.largura/2, self.altura/2))

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
        
        # Botão Jogar Novamente (tela de vitória)
        self.botao_jogar_novamente = pygame.Rect(0, 0, 300, 60)
        self.botao_jogar_novamente.center = (self.largura // 2, self.altura // 2 + 50)
        
        # Estados do jogo
        self.estado = "MENU"  # MENU, JOGANDO, VITORIA
        
        # Controle de música
        self.musica_menu_tocando = False
        self.fazendo_fade_out = False
        self.volume_fade = 0.3  # Volume inicial da música
        
        # Botões do Menu Principal
        largura_botao = 250
        altura_botao = 70
        espaco_entre_botoes = 30
        
        self.botao_jogar = pygame.Rect(0, 0, largura_botao, altura_botao)
        self.botao_jogar.center = (self.largura // 2, self.altura // 2 + 50)
        
        self.botao_sair = pygame.Rect(0, 0, largura_botao, altura_botao)
        self.botao_sair.center = (self.largura // 2, self.altura // 2 + 50 + altura_botao + espaco_entre_botoes)
        
        # Animação do personagem no menu
        self.sprites_menu = self.sprites.get('Idle', [])
        self.frame_menu = 0
        self.timer_menu = 0
        
        # Sistema de textos flutuantes
        self.textos_flutuantes = []
        
        # Gerenciador de inimigos
        self.gerenciador_inimigos = GerenciadorInimigos(self.largura, self.altura)

        self.MBB = False
        self.MBL = False
        self.stopderrota = False
        self.stopvitoria = False
        
    def adicionar_texto_flutuante(self, texto, x, y, cor):
        """Adiciona um texto flutuante na posição especificada"""
        self.textos_flutuantes.append({
            'texto': texto,
            'x': x,
            'y': y,
            'cor': cor,
            'tempo_criacao': pygame.time.get_ticks(),
            'alpha': 255
        })
    
    def atualizar_textos_flutuantes(self):
        """Atualiza e remove textos flutuantes antigos"""
        tempo_atual = pygame.time.get_ticks()
        textos_para_remover = []
        
        for texto in self.textos_flutuantes:
            tempo_vida = tempo_atual - texto['tempo_criacao']
            
            # Remove após 1.5 segundos
            if tempo_vida > 1500:
                textos_para_remover.append(texto)
            else:
                # Move para cima
                texto['y'] -= 1.5
                # Fade out gradual
                texto['alpha'] = max(0, 255 - (tempo_vida * 0.17))
        
        # Remove textos antigos
        for texto in textos_para_remover:
            self.textos_flutuantes.remove(texto)
    
    def desenhar_textos_flutuantes(self):
        """Desenha todos os textos flutuantes na tela"""
        fonte = pygame.font.SysFont("Arial", 28, True)
        
        for texto in self.textos_flutuantes:
            # Criar superfície com o texto
            superficie_texto = fonte.render(texto['texto'], True, texto['cor'])
            
            # Aplicar transparência
            superficie_texto.set_alpha(int(texto['alpha']))
            
            # Centralizar o texto na posição
            rect = superficie_texto.get_rect(center=(int(texto['x']), int(texto['y'])))
            
            # Desenhar sombra para melhor legibilidade
            sombra = fonte.render(texto['texto'], True, (0, 0, 0))
            sombra.set_alpha(int(texto['alpha'] * 0.5))
            rect_sombra = sombra.get_rect(center=(int(texto['x']) + 2, int(texto['y']) + 2))
            self.tela.blit(sombra, rect_sombra)
            
            # Desenhar texto
            self.tela.blit(superficie_texto, rect)
    
    def desenhar_barra_progresso(self):
        """Desenha a barra de progresso para 1000 pontos"""
        # Configurações da barra
        largura_barra = 400
        altura_barra = 35
        x_barra = (self.largura - largura_barra) // 2
        y_barra = 20
        
        # Calcular progresso (0 a 1)
        progresso = min(self.pontos / 1000, 1.0)
        largura_preenchida = int(largura_barra * progresso)
        
        # Fundo da barra (escuro)
        fundo = pygame.Rect(x_barra, y_barra, largura_barra, altura_barra)
        pygame.draw.rect(self.tela, (40, 40, 50), fundo, border_radius=10)
        
        # Barra de progresso (gradiente de cor baseado no progresso)
        if largura_preenchida > 0:
            # Cor muda de verde -> amarelo -> dourado conforme progresso
            if progresso < 0.5:
                cor_barra = (50, 200, 50)  # Verde
            elif progresso < 0.8:
                cor_barra = (200, 200, 50)  # Amarelo
            else:
                cor_barra = (255, 215, 0)  # Dourado
            
            preenchimento = pygame.Rect(x_barra, y_barra, largura_preenchida, altura_barra)
            pygame.draw.rect(self.tela, cor_barra, preenchimento, border_radius=10)
        
        # Borda dourada
        pygame.draw.rect(self.tela, (255, 215, 0), fundo, 3, border_radius=10)
        
        # Texto de progresso no centro da barra
        fonte = pygame.font.SysFont("Arial", 20, True)
        texto_progresso = f"{self.pontos}/1000"
        superficie_texto = fonte.render(texto_progresso, True, (255, 255, 255))
        
        # Sombra do texto
        sombra = fonte.render(texto_progresso, True, (0, 0, 0))
        rect_sombra = sombra.get_rect(center=(self.largura // 2 + 1, y_barra + altura_barra // 2 + 1))
        self.tela.blit(sombra, rect_sombra)
        
        # Texto principal
        rect_texto = superficie_texto.get_rect(center=(self.largura // 2, y_barra + altura_barra // 2))
        self.tela.blit(superficie_texto, rect_texto)
        
        # Label "OBJETIVO" acima da barra
        fonte_label = pygame.font.SysFont("Arial", 16, True)
        label = fonte_label.render("OBJETIVO", True, (200, 200, 200))
        rect_label = label.get_rect(center=(self.largura // 2, y_barra - 15))
        self.tela.blit(label, rect_label)
    
    def check_colisoes_inimigos(self, player_rect, sword_rect):
        """Verifica colisões entre jogador/espada e inimigos"""
        gerenc = self.gerenciador_inimigos
        
        # Colisão jogador com bruxas
        for bruxa in gerenc.bruxas[:]:
            if(canalbruxa.get_busy() == False):
                canalbruxa.play(som_bruxa_voo)
            bruxa_rect = bruxa.get_rect()
            
            if player_rect.colliderect(bruxa_rect):
                som_bruxa_riso.play()
                self.vida -= 20
                self.adicionar_texto_flutuante("-20 VIDA", self.player.x, self.player.y - 30, (255, 50, 50))
                gerenc.bruxas.remove(bruxa)
            
            # Colisão espada com bruxa
            if sword_rect.colliderect(bruxa_rect):
                som_espada_hit.play()
                bruxa.vida -= 1
                if bruxa.vida <= 0:
                    som_bruxa_morte.play()
                    self.pontos += 30
                    self.adicionar_texto_flutuante("+30 pts", bruxa.x, bruxa.y, (255, 215, 0))
                    gerenc.bruxas.remove(bruxa)
                else:
                    self.adicionar_texto_flutuante("HIT!", bruxa.x, bruxa.y, (255, 100, 100))
        
        # Colisão jogador com morcegos
        for morcego in gerenc.morcegos[:]:
            if(canalmorcego.get_busy() == False):
                canalmorcego.play(som_morcego_voo)
            morcego_rect = morcego.get_rect()
            
            if player_rect.colliderect(morcego_rect):
                som_morcego_morte.play()
                self.vida -= 12
                self.adicionar_texto_flutuante("-12 VIDA", self.player.x, self.player.y - 30, (255, 50, 50))
                gerenc.morcegos.remove(morcego)
            
            # Colisão espada com morcego
            if sword_rect.colliderect(morcego_rect):
                som_espada_hit.play()
                som_morcego_morte.play()
                self.pontos += 15
                self.adicionar_texto_flutuante("+15 pts", morcego.x, morcego.y, (255, 215, 0))
                gerenc.morcegos.remove(morcego)

        for demo in gerenc.demos[:]:
            som_demo_spawn.play()
            demo_rect = demo.get_rect()
            
            if player_rect.colliderect(demo_rect):
                self.vida -= 12
                self.adicionar_texto_flutuante("-12 VIDA", self.player.x, self.player.y - 30, (255, 50, 50))
                gerenc.demos.remove(demo)
            
            # Colisão espada com demo
            if sword_rect.colliderect(demo_rect):
                self.pontos += 15
                self.adicionar_texto_flutuante("+15 pts", demo.x, demo.y, (255, 215, 0))
                gerenc.demos.remove(demo)
        
        # Colisão jogador com projéteis
        for proj in gerenc.projeteis[:]:
            proj_rect = proj.get_rect()
            
            if player_rect.colliderect(proj_rect):
                som_fogo_ataque.play()
                if gerenc.bruxas: ## Previne que a risada aconteça sem nenhuma bruxa
                    som_bruxa_riso.play()
                self.vida -= 20
                self.adicionar_texto_flutuante("-20 VIDA", self.player.x, self.player.y - 30, (255, 50, 50))
                gerenc.projeteis.remove(proj)
        
        # Game Over se vida acabar
        if self.vida <= 0:
            self.vida = 0
            self.estado = "DERROTA"
            self.adicionar_texto_flutuante("GAME OVER!", self.largura // 2, self.altura // 2, (255, 0, 0))
    
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
        self.textos_flutuantes.clear()  # Limpa textos flutuantes
        self.gerenciador_inimigos.limpar()
        self.spawn_random_coin()
        # Reposicionar o jogador
        self.player.x = self.largura // 2
        self.player.y = self.altura // 2
        # Iniciar fade out da música
        self.fazendo_fade_out = True
        self.volume_fade = 0.3
        self.estado = "JOGANDO"
        
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
                    # Texto flutuante para diamante
                    self.adicionar_texto_flutuante(f"+{item.value} pts", item.x, item.y, (0, 255, 255))
                elif isinstance(item, Moeda):
                    self.moedas += 1
                    self.pontos += item.value
                    som_moeda.play()
                    # Texto flutuante para moeda
                    self.adicionar_texto_flutuante(f"+{item.value} pts", item.x, item.y, (255, 215, 0))
                elif isinstance(item, Maça):
                    self.maçãs += 1
                    vida_antes = self.vida
                    self.vida = min(100, self.vida + item.value)
                    vida_recuperada = self.vida - vida_antes
                    som_maca.play()
                    # Texto flutuante para maçã
                    self.adicionar_texto_flutuante(f"+{vida_recuperada} VIDA", item.x, item.y, (255, 100, 100))
                coletados.append(item) # Marca para remoção

            # Ação de destruir (Colisão entre Espada e Item)
            if sword_rect.colliderect(hitbox_item):
                # Texto flutuante ao destruir com espada
                som_espada_hit.play()
                self.adicionar_texto_flutuante("DESTRUIDO!", item.x, item.y, (255, 50, 50))
                coletados.append(item) # Marca para remoção
        
        # Remove os itens coletados ou destruídos da lista de ativos
        for item in coletados:
            if item in self.coletaveis_ativos:
                self.coletaveis_ativos.remove(item)

    def exibir_menu(self, mouse_pos):
        """Desenha o menu principal"""
        # Fundo do menu (mesmo do jogo mas mais escuro)
        self.tela.blit(self.BACKEST, (0, 0))
        rect_imagem = self.img_menu.get_rect(center=(self.largura // 2, self.altura // 2))
        self.tela.blit(self.img_menu, rect_imagem)

        overlay = pygame.Surface((self.largura, self.altura))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))

        # Logo do jogo
        rect_logo = self.img_logo.get_rect(center=(self.largura // 2, self.altura // 5))
        self.tela.blit(self.img_logo, rect_logo)
        
        # legenda do jogo
        fonte_subtitulo = pygame.font.SysFont("Arial", 35, True)
        txt_sub = fonte_subtitulo.render("Colete 1000 pontos para vencer!", True, (255, 255, 255))
        self.tela.blit(txt_sub, txt_sub.get_rect(center=(self.largura/2, 500)))
        
        # Botão JOGAR
        cor_jogar = (50, 150, 50) if self.botao_jogar.collidepoint(mouse_pos) else (30, 100, 30)
        pygame.draw.rect(self.tela, cor_jogar, self.botao_jogar, border_radius=15)
        pygame.draw.rect(self.tela, (255, 215, 0), self.botao_jogar, 4, border_radius=15)
        
        fonte_botao = pygame.font.SysFont("Arial", 40, True)
        txt_jogar = fonte_botao.render("JOGAR", True, (255, 255, 255))
        self.tela.blit(txt_jogar, txt_jogar.get_rect(center=self.botao_jogar.center))
        
        # Botão SAIR
        cor_sair = (150, 50, 50) if self.botao_sair.collidepoint(mouse_pos) else (100, 30, 30)
        pygame.draw.rect(self.tela, cor_sair, self.botao_sair, border_radius=15)
        pygame.draw.rect(self.tela, (255, 215, 0), self.botao_sair, 4, border_radius=15)
        
        txt_sair = fonte_botao.render("SAIR", True, (255, 255, 255))
        self.tela.blit(txt_sair, txt_sair.get_rect(center=self.botao_sair.center))
        
        # Créditos no rodapé
        fonte_creditos = pygame.font.SysFont("Arial", 20, False)
        txt_creditos = fonte_creditos.render("Desenvolvido com Pygame", True, (150, 150, 150))
        self.tela.blit(txt_creditos, txt_creditos.get_rect(center=(self.largura/2, self.altura - 30)))

    def exibir_vitoria(self, mouse_pos):
        self.tela.blit(self.BACKEST, (0, 0))
        rect_imagem = self.img_vitoria.get_rect(center=(self.largura // 2, self.altura // 2))
        self.tela.blit(self.img_vitoria, rect_imagem)

        overlay = pygame.Surface((self.largura, self.altura))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))
        
        fonte_tit = pygame.font.SysFont("Arial", 60, True)
        fonte_sub = pygame.font.SysFont("Arial", 30, True)
        txt1 = fonte_tit.render("Parabéns, Cavaleiro!", True, (255, 215, 0))
        txt2 = fonte_sub.render("Você Salvou o Mundo das Forças das Trevas!", True, (255, 255, 255))
        self.tela.blit(txt1, txt1.get_rect(center=(self.largura/2, self.altura/2 - 140)))
        self.tela.blit(txt2, txt2.get_rect(center=(self.largura/2, self.altura/2 - 70)))
        
        # Desenhar botão "Jogar Novamente"
        cor_botao = (50, 150, 50) if self.botao_jogar_novamente.collidepoint(mouse_pos) else (30, 100, 30)
        
        pygame.draw.rect(self.tela, cor_botao, self.botao_jogar_novamente, border_radius=10)
        pygame.draw.rect(self.tela, (255, 215, 0), self.botao_jogar_novamente, 3, border_radius=10)
        
        fonte_botao = pygame.font.SysFont("Arial", 35, True)
        txt_botao = fonte_botao.render("Jogar Novamente", True, (255, 255, 255))
        txt_rect = txt_botao.get_rect(center=self.botao_jogar_novamente.center)
        self.tela.blit(txt_botao, txt_rect)

        # Desenhar botão "SAIR"
        cor_sair = (150, 50, 50) if self.botao_sair.collidepoint(mouse_pos) else (100, 30, 30)
        pygame.draw.rect(self.tela, cor_sair, self.botao_sair, border_radius=15)
        pygame.draw.rect(self.tela, (255, 215, 0), self.botao_sair, 4, border_radius=15)
        
        txt_sair = fonte_botao.render("SAIR", True, (255, 255, 255))
        self.tela.blit(txt_sair, txt_sair.get_rect(center=self.botao_sair.center))

    def exibir_derrota(self, mouse_pos):
        self.tela.blit(self.BACKEST, (0, 0))
        rect_imagem = self.img_derrota.get_rect(center=(self.largura // 2, self.altura // 2))
        self.tela.blit(self.img_derrota, rect_imagem)

        overlay = pygame.Surface((self.largura, self.altura))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.tela.blit(overlay, (0, 0))
        
        fonte_tit = pygame.font.SysFont("Arial", 60, True)
        fonte_sub = pygame.font.SysFont("Arial", 30, True)
        txt1 = fonte_tit.render("Você perdeu, Cavaleiro!", True, (255, 215, 0))
        txt2 = fonte_sub.render("Você sucumbiu perante os inimigos!", True, (255, 255, 255))
        self.tela.blit(txt1, txt1.get_rect(center=(self.largura/2, self.altura/2 - 140)))
        self.tela.blit(txt2, txt2.get_rect(center=(self.largura/2, self.altura/2 - 70)))
        
        # Desenhar botão "Jogar Novamente"
        cor_botao = (50, 150, 50) if self.botao_jogar_novamente.collidepoint(mouse_pos) else (30, 100, 30)
        
        pygame.draw.rect(self.tela, cor_botao, self.botao_jogar_novamente, border_radius=10)
        pygame.draw.rect(self.tela, (255, 215, 0), self.botao_jogar_novamente, 3, border_radius=10)
        
        fonte_botao = pygame.font.SysFont("Arial", 35, True)
        txt_botao = fonte_botao.render("Jogar Novamente", True, (255, 255, 255))
        txt_rect = txt_botao.get_rect(center=self.botao_jogar_novamente.center)
        self.tela.blit(txt_botao, txt_rect)

        # Desenhar botão "SAIR"
        cor_sair = (150, 50, 50) if self.botao_sair.collidepoint(mouse_pos) else (100, 30, 30)
        pygame.draw.rect(self.tela, cor_sair, self.botao_sair, border_radius=15)
        pygame.draw.rect(self.tela, (255, 215, 0), self.botao_sair, 4, border_radius=15)
        
        txt_sair = fonte_botao.render("SAIR", True, (255, 255, 255))
        self.tela.blit(txt_sair, txt_sair.get_rect(center=self.botao_sair.center))
    
    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos

            self.relogio.tick(30)
            tempo_atual = pygame.time.get_ticks()

            # ========== MENU PRINCIPAL ==========
            if self.estado == "MENU":
                # Tocar música do menu (loop infinito) - apenas se disponível
                if not self.musica_menu_tocando and musica_menu_disponivel:
                    pygame.mixer.music.play(-1)  # -1 = loop infinito
                    pygame.mixer.music.set_volume(0.3)
                    self.musica_menu_tocando = True
                    self.volume_fade = 0.3
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        # Clicou no botão JOGAR
                        if self.botao_jogar.collidepoint(event.pos):
                            self.reiniciar_jogo()
                        
                        # Clicou no botão SAIR
                        if self.botao_sair.collidepoint(event.pos):
                            pygame.quit()
                            exit()
                
                self.exibir_menu(mouse_pos)
                self.tela.blit(self.cursor, mouse_pos)
            
            # ========== JOGANDO ==========
            elif self.estado == "JOGANDO":
                # Fade out gradual da música do menu (apenas se estiver disponível)
                if self.fazendo_fade_out and musica_menu_disponivel:
                    self.volume_fade -= 0.01  # Diminui 0.01 por frame (suave)
                    if self.volume_fade <= 0:
                        self.volume_fade = 0
                        pygame.mixer.music.stop()
                        self.musica_menu_tocando = False
                        self.fazendo_fade_out = False
                    else:
                        pygame.mixer.music.set_volume(self.volume_fade)

                if(pygame.mixer.music.get_busy() == False)and(self.MBB==False):
                    pygame.mixer.music.load("Audios/Musica_Background_begin.mp3")
                    pygame.mixer_music.play()
                    pygame.mixer.music.set_volume(0.5)
                    self.MBB = True
                elif(pygame.mixer.music.get_busy() == False)and(self.MBB==True)and(self.MBL==False):
                    pygame.mixer.music.load("Audios/Musica_Background_loop.mp3")
                    pygame.mixer_music.play(-1)
                    pygame.mixer.music.set_volume(0.5)
                    self.MBL = True
                
                # Checar sapwn do boss
                if self.pontos >= 1000 and not self.boss_vivo and not self.boss_derrotado:
                    som_boss.play()
                    from inimigos import Boss # Certifique-se de ter a classe Boss no inimigos.py
                    self.boss = Boss(self.largura, self.altura)
                    self.boss_vivo = True
                    self.adicionar_texto_flutuante("O CHEFE DESPERTOU!", self.largura//2, self.altura//2, (255, 0, 0))

                if self.boss_vivo and self.boss:
                    self.boss.mover(self.player.x, self.player.y)
                    
                    # Colisão: Espada atinge o Boss
                    if self.rect.colliderect(self.boss.rect):
                        if pygame.time.get_ticks() % 5 == 0: # Evita que o dano seja por frame (muito rápido)
                            self.boss.vida -= 5
                            som_espada_hit.play()
                            self.adicionar_texto_flutuante("-5", self.boss.x, self.boss.y, (255, 255, 255))

                    # Colisão: Boss atinge o Jogador
                    if templário.colliderect(self.boss.rect):
                        if pygame.time.get_ticks() % 20 == 0:
                            self.vida -= 10
                            self.adicionar_texto_flutuante("-10 VIDA", self.player.x, self.player.y, (255, 0, 0))

                    # Morte do Boss = VITÓRIA
                    if self.boss.vida <= 0:
                        self.boss_vivo = False
                        self.boss_derrotado = True
                        self.boss = None
                        self.estado = "VITORIA"
                        som_vitoria.play()

                self.tela.fill((0, 0, 0))
                self.tela.blit(self.BACKEST, (0, 0))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    
                    # Tecla ESC volta ao menu
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.estado = "MENU"

                    if event.type == spawn_item_event:
                        self.spawn_random_coin()

                self.player.move(self.largura, self.altura)
                self.sword.update(self.player.x, self.player.y, mouse_x, mouse_y)
                self.rect = self.sword.draw(self.tela)
                
                # Atualizar inimigos
                if self.boss_vivo == False:
                    self.gerenciador_inimigos.atualizar(self.player.x, self.player.y)
                else:
                    self.gerenciador_inimigos.limpar()
                
                # Desenhar itens coletáveis
                for item in self.coletaveis_ativos:
                        item.draw(self.tela)

                # Ordem de desenho (profundidade)
                if self.sword.behind_player:
                    templário = self.player.draw(self.tela)
                    self.sword.draw(self.tela)
                else:
                    self.sword.draw(self.tela)
                    templário = self.player.draw(self.tela)
                
                # Desenhar inimigos
                self.gerenciador_inimigos.desenhar(self.tela)

                self.check_collisions(templário, self.rect)
                self.check_colisoes_inimigos(templário, self.rect)

                if self.boss_vivo and self.boss:
                    self.boss.draw(self.tela)
                    self.boss.draw_health_bar(self.tela, self.largura)
                
                # Atualizar e desenhar textos flutuantes
                self.atualizar_textos_flutuantes()
                
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
                
                # Desenhar barra de progresso
                self.desenhar_barra_progresso()
                
                # Desenhar textos flutuantes por cima de tudo
                self.desenhar_textos_flutuantes()

                self.tela.blit(Hud().cursor_customizado(), mouse_pos)
            
            # ========== TELA DE VITÓRIA ==========
            elif self.estado == "VITORIA":
                pygame.mixer.music.stop()
                if(self.stopvitoria == False):
                    pygame.mixer.stop()
                    self.stopvitoria = True

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    
                    # Detectar clique no botão (apenas com botão esquerdo do mouse)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if self.botao_jogar_novamente.collidepoint(event.pos):
                            self.reiniciar_jogo()

                        if self.botao_sair.collidepoint(event.pos):
                            pygame.quit()
                            exit()
                
                self.exibir_vitoria(mouse_pos)
                self.tela.blit(Hud().cursor_customizado(), mouse_pos)

            elif self.estado == "DERROTA":
                pygame.mixer.music.stop()

                if(self.stopderrota == False):
                    pygame.mixer.stop()
                    self.stopderrota = True
                    som_derrota.play()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    
                    # Detectar clique no botão (apenas com botão esquerdo do mouse)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if self.botao_jogar_novamente.collidepoint(event.pos):
                            self.reiniciar_jogo()
                        
                        if self.botao_sair.collidepoint(event.pos):
                            pygame.quit()
                            exit()

                
                self.exibir_derrota(mouse_pos)
                self.tela.blit(Hud().cursor_customizado(), mouse_pos)

            pygame.display.update()

Game().run()