import pygame
from random import randint

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, vida, velocidade, sprites):
        super().__init__()

        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

        info = pygame.display.Info()
        self.largura_desktop = info.current_w
        self.altura_desktop = info.current_h

        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vida = vida
        self.velocidade = velocidade
        self.vivo = True
        self.sprites = sprites
    
    def receber_dano(self, dano):
        self.vida -= dano

        if self.vida <= 0:
            self.morrer()

    def morrer(self):
        self.vivo = False
        self.kill()

    def update(self):
        if not self.vivo:
            return
        self.rect.y -= self.velocidade//2
        self.rect.x -= self.velocidade

class Morcego(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y, vida=1, velocidade=3, sprites=None)
        self.image.fill((0, 200, 0))

class Bruxa(Inimigo):
    def __init__(self, x, y, sprites):
        super().__init__(x, y, vida=1, velocidade=0, sprites=sprites) 
        self.image.fill((200, 0, 0))
        self.estado_movimento = 1  
        self.tempo_inicio_estado = pygame.time.get_ticks() 
        
        # Duração de cada estado em MILISSEGUNDOS
        self.tempo_duracao = {1: 3000, 2: 1000, 3: 3000, 4: 1000}
        
        altura_segura = self.altura_desktop - self.rect.height
        largura_segura = self.largura_desktop - self.rect.width
        
        self.frame_atual = 0
        self.timer_animacao = pygame.time.get_ticks()
        self.velocidade_animacao = 150
        self.sprites_fly = self.sprites.get('Fly_Bruxa', [])

        self.pos_destino_esq = (0, randint(0, altura_segura))
        self.pos_destino_dir = (largura_segura, randint(0, altura_segura))
        
        # Começa na direita para iniciar o ciclo
        self.rect.topleft = self.pos_destino_dir 

        self.estado_movimento = 4
        self.tempo_duracao[4] = 1
        self.tempo_inicio_estado = pygame.time.get_ticks()

    def animar(self):
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.timer_animacao:
            self.frame_atual = (self.frame_atual + 1) % len(self.sprites_fly)
            self.image = self.sprites_fly[self.frame_atual]
            self.timer_animacao = tempo_atual

    def update(self):
        if not self.vivo:
            return
        self.animar()
        
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = tempo_atual - self.tempo_inicio_estado
        
        # --- Transição de Estado ---
        if tempo_passado >= self.tempo_duracao[self.estado_movimento]:
            
            self.estado_movimento = (self.estado_movimento % 4) + 1
            self.tempo_inicio_estado = tempo_atual # Reinicia o timer
            
            if self.estado_movimento == 1: # Indo p/ Esq (próxima posição Y aleatória)
                altura_segura = self.altura_desktop - self.rect.height
                self.pos_destino_esq = (0, randint(0, altura_segura))

            elif self.estado_movimento == 3: # Indo p/ Dir (próxima posição Y aleatória)
                largura_segura = self.largura_desktop - self.rect.width
                altura_segura = self.altura_desktop - self.rect.height
                self.pos_destino_dir = (largura_segura, randint(0, altura_segura))

        # --- Execução do Movimento ---
        if self.estado_movimento == 1: # Indo para a Esquerda
            percentual = min(1.0, tempo_passado / self.tempo_duracao[1]) # Evita percentual > 1
            
            start_pos = self.pos_destino_dir
            end_pos = self.pos_destino_esq
            
            novo_x = start_pos[0] + (end_pos[0] - start_pos[0]) * percentual
            novo_y = start_pos[1] + (end_pos[1] - start_pos[1]) * percentual
            
            self.rect.topleft = (novo_x, novo_y)
            
        elif self.estado_movimento == 2: # Esperando na Esquerda
            self.rect.topleft = self.pos_destino_esq 
            
        elif self.estado_movimento == 3: # Indo para a Direita
            percentual = min(1.0, tempo_passado / self.tempo_duracao[3])
            
            start_pos = self.pos_destino_esq
            end_pos = self.pos_destino_dir
            
            novo_x = start_pos[0] + (end_pos[0] - start_pos[0]) * percentual
            novo_y = start_pos[1] + (end_pos[1] - start_pos[1]) * percentual
            
            self.rect.topleft = (novo_x, novo_y)

        elif self.estado_movimento == 4: # Esperando na Direita
            self.rect.topleft = self.pos_destino_dir

class Diabrete(Inimigo):
    def __init__(self, x, y, velocidade=3, sprites=None):
        super().__init__(x, y, vida=1, velocidade=15)
        self.image.fill((200, 0, 0))

class Touro(Inimigo):
    def __init__(self, x, y, velocidade=3, sprites=None):
        super().__init__(x, y, vida=5, velocidade=3)
        self.image.fill((200, 0, 0))