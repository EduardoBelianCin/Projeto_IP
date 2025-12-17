import pygame
import os
from random import choice, randint

def carregar_sprites_animacao(caminho, num_frames):
    """Carrega sprites de animação de uma pasta"""
    sprites = []
    nome_pasta = caminho.split('/')[-1]
    
    for i in range(num_frames):
        if nome_pasta == "Fly":
            img_path = f"{caminho}/Bruxa{i}.png"
        elif nome_pasta == "Attack":
            img_path = f"{caminho}/fogo{i}.png"
        elif nome_pasta == "Demo":
            img_path = f"{caminho}/demo{i}.png"
        elif nome_pasta == "morcego":
            img_path = f"{caminho}/morcego{i}.png"
        else:
            img_path = f"{caminho}/{nome_pasta}{i}.png"
        
        img = pygame.image.load(img_path).convert_alpha()
        img = pygame.transform.scale_by(img, 2)
        sprites.append(img)
    
    return sprites

class Bruxa:
    """Bruxa que se move horizontalmente e atira projéteis de fogo"""
    
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.vida = 1
        self.velocidade = 8
        self.direcao = 1 if x < 400 else -1
        self.ultimo_tiro = pygame.time.get_ticks()
        self.intervalo_tiro = 1000  # 1 segundo
        self.frame = 0
        self.timer_animacao = 0
        self.sprites = sprites
        self.largura = 40
        self.altura = 40
    
    def atualizar(self, largura_tela):
        """Atualiza movimento e animação"""
        tempo_atual = pygame.time.get_ticks()
        
        # Movimento horizontal
        self.x += self.velocidade * self.direcao
        
        # Inverte direção nas bordas
        if self.x <= 50 or self.x >= largura_tela - 50:
            self.direcao *= -1
        
        # Atualizar animação
        if tempo_atual - self.timer_animacao > 150:
            self.frame = (self.frame + 1) % len(self.sprites)
            self.timer_animacao = tempo_atual
    
    def pode_atirar(self):
        """Verifica se pode atirar"""
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tiro > self.intervalo_tiro:
            self.ultimo_tiro = tempo_atual
            return True
        return False
    
    def desenhar(self, tela):
        """Desenha a bruxa na tela"""
        sprite = self.sprites[self.frame]
        sprite_invertido = pygame.transform.flip(sprite, True, False)
        rect = sprite.get_rect(center=(int(self.x), int(self.y)))

        if self.direcao > 0:
            tela.blit(sprite_invertido, rect)
        else:
            tela.blit(sprite, rect)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return pygame.Rect(self.x - self.largura//2, self.y - self.altura//2, 
                          self.largura, self.altura)


class Morcego:
    """Morcego que persegue o jogador"""
    
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.vida = 1
        self.velocidade = 3.5
        self.frame = 0
        self.timer_animacao = 0
        self.sprites = sprites
        self.largura = 30
        self.altura = 30
    
    def atualizar(self, jogador_x, jogador_y):
        """Atualiza movimento em direção ao jogador"""
        tempo_atual = pygame.time.get_ticks()
        self.jogador_x = jogador_x
        
        # Calcular direção para o jogador
        dx = jogador_x - self.x
        dy = jogador_y - self.y
        distancia = (dx**2 + dy**2)**0.5
        
        if distancia > 0:
            # Normalizar e aplicar velocidade
            self.x += (dx / distancia) * self.velocidade
            self.y += (dy / distancia) * self.velocidade
        
        # Atualizar animação
        if tempo_atual - self.timer_animacao > 100:
            self.frame = (self.frame + 1) % len(self.sprites)
            self.timer_animacao = tempo_atual
    
    def desenhar(self, tela):
        """Desenha o morcego na tela"""
        sprite = self.sprites[self.frame]
        sprite_invertido = pygame.transform.flip(sprite, True, False)
        rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        
        if self.jogador_x > self.x:
            tela.blit(sprite_invertido, rect)
        else:
            tela.blit(sprite, rect)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return pygame.Rect(self.x - self.largura//2, self.y - self.altura//2, 
                          self.largura, self.altura)

class Demo:
    """Demo que persegue o jogador"""
    
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.vida = 1
        self.velocidade = 10
        self.frame = 0
        self.timer_animacao = 0
        self.sprites = sprites
        self.largura = 30
        self.altura = 30
    
    def atualizar(self, jogador_x, jogador_y):
        """Atualiza movimento em direção ao jogador"""
        tempo_atual = pygame.time.get_ticks()
        self.jogador_x = jogador_x
        
        # Calcular direção para o jogador
        dx = jogador_x - self.x
        dy = jogador_y - self.y
        distancia = (dx**2 + dy**2)**0.5
        
        if distancia > 0:
            # Normalizar e aplicar velocidade
            self.x += (dx / distancia) * self.velocidade
            self.y += (dy / distancia) * self.velocidade
        
        # Atualizar animação
        if tempo_atual - self.timer_animacao > 100:
            self.frame = (self.frame + 1) % len(self.sprites)
            self.timer_animacao = tempo_atual
    
    def desenhar(self, tela):
        """Desenha o demo na tela"""
        sprite = self.sprites[self.frame]
        sprite_invertido = pygame.transform.flip(sprite, True, False)
        rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        
        if self.jogador_x > self.x:
            tela.blit(sprite_invertido, rect)
        else:
            tela.blit(sprite, rect)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return pygame.Rect(self.x - self.largura//2, self.y - self.altura//2, 
                          self.largura, self.altura)

class Projetil:
    """Projétil de fogo disparado pela bruxa"""
    
    def __init__(self, x, y, vel_x, vel_y, sprites):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.frame = 0
        self.timer_animacao = 0
        self.sprites = sprites
        self.largura = 20
        self.altura = 20
    
    def atualizar(self):
        """Atualiza movimento e animação"""
        tempo_atual = pygame.time.get_ticks()
        
        # Movimento
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Atualizar animação
        if tempo_atual - self.timer_animacao > 80:
            self.frame = (self.frame + 1) % len(self.sprites)
            self.timer_animacao = tempo_atual
    
    def desenhar(self, tela):
        """Desenha o projétil na tela"""
        sprite = self.sprites[self.frame]
        rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        tela.blit(sprite, rect)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return pygame.Rect(self.x - self.largura//2, self.y - self.altura//2, 
                          self.largura, self.altura)
    
    def fora_da_tela(self, largura_tela, altura_tela):
        """Verifica se saiu da tela"""
        return (self.x < -50 or self.x > largura_tela + 50 or 
                self.y < -50 or self.y > altura_tela + 50)


class GerenciadorInimigos:
    """Gerencia spawn e atualização de todos os inimigos"""
    
    def __init__(self, largura_tela, altura_tela):
        self.largura = largura_tela
        self.altura = altura_tela
        
        # Listas de inimigos
        self.bruxas = []
        self.morcegos = []
        self.demos = []
        self.projeteis = []
        
        # Controle de spawn
        self.ultimo_spawn_bruxa = 0
        self.ultimo_spawn_morcego = 0
        self.ultimo_spawn_demo = 0
        self.intervalo_spawn_bruxa = 15000  # 15 segundos
        self.intervalo_spawn_morcego = 8000  # 8 segundos
        self.intervalo_spawn_demo = 8000  # 8 segundos
        self.max_bruxas = 2
        self.max_morcegos = 5
        self.max_demos = 3
        
        # Carregar sprites
        self.sprites_bruxa = carregar_sprites_animacao("sprites/inimigos/Bruxa/Fly", 4)
        self.sprites_morcego = carregar_sprites_animacao("sprites/inimigos/morcego", 4)
        self.sprites_projetil = carregar_sprites_animacao("sprites/inimigos/Bruxa/Attack", 5)
        self.sprites_demo = carregar_sprites_animacao("sprites/inimigos/Demo", 4)
    
    def spawn_bruxa(self):
        """Cria uma nova bruxa"""
        if len(self.bruxas) < self.max_bruxas:
            # Spawn nas bordas (esquerda ou direita)
            lado = choice(['esquerda', 'direita'])
            if lado == 'esquerda':
                x = 50
            else:
                x = self.largura - 50
            
            y = randint(100, self.altura - 150)
            
            bruxa = Bruxa(x, y, self.sprites_bruxa)
            self.bruxas.append(bruxa)
    
    def spawn_morcego(self):
        """Cria um novo morcego"""
        if len(self.morcegos) < self.max_morcegos:
            # Spawn nas bordas da tela
            lado = choice(['cima', 'baixo', 'esquerda', 'direita'])
            
            if lado == 'cima':
                x = randint(50, self.largura - 50)
                y = 50
            elif lado == 'baixo':
                x = randint(50, self.largura - 50)
                y = self.altura - 100
            elif lado == 'esquerda':
                x = 50
                y = randint(50, self.altura - 100)
            else:
                x = self.largura - 50
                y = randint(50, self.altura - 100)
            
            morcego = Morcego(x, y, self.sprites_morcego)
            self.morcegos.append(morcego)

    def spawn_demo(self):
        """Cria um novo demo"""
        if len(self.demos) < self.max_demos:
            # Spawn nas bordas da tela
            lado = choice(['cima', 'baixo', 'esquerda', 'direita'])
            
            if lado == 'cima':
                x = randint(50, self.largura - 50)
                y = 50
            elif lado == 'baixo':
                x = randint(50, self.largura - 50)
                y = self.altura - 100
            elif lado == 'esquerda':
                x = 50
                y = randint(50, self.altura - 100)
            else:
                x = self.largura - 50
                y = randint(50, self.altura - 100)
            
            demo = Demo(x, y, self.sprites_demo)
            self.demos.append(demo)
    
    def criar_projetil(self, x, y, jogador_x, jogador_y):
        """Cria um projétil de fogo"""
        # Calcular direção para o jogador
        dx = jogador_x - x
        dy = jogador_y - y
        distancia = (dx**2 + dy**2)**0.5
        
        if distancia > 0:
            velocidade_proj = 5
            vel_x = (dx / distancia) * velocidade_proj
            vel_y = (dy / distancia) * velocidade_proj
            
            projetil = Projetil(x, y, vel_x, vel_y, self.sprites_projetil)
            self.projeteis.append(projetil)
    
    def atualizar(self, jogador_x, jogador_y):
        """Atualiza todos os inimigos"""
        tempo_atual = pygame.time.get_ticks()
        
        # Spawn de inimigos
        if tempo_atual - self.ultimo_spawn_bruxa > self.intervalo_spawn_bruxa:
            self.spawn_bruxa()
            self.ultimo_spawn_bruxa = tempo_atual
        
        if tempo_atual - self.ultimo_spawn_morcego > self.intervalo_spawn_morcego:
            self.spawn_morcego()
            self.ultimo_spawn_morcego = tempo_atual

        if tempo_atual - self.ultimo_spawn_demo > self.intervalo_spawn_demo:
            self.spawn_demo()
            self.ultimo_spawn_demo = tempo_atual
        
        # Atualizar bruxas
        for bruxa in self.bruxas:
            bruxa.atualizar(self.largura)
            # Verifica se pode atirar
            if bruxa.pode_atirar():
                self.criar_projetil(bruxa.x, bruxa.y, jogador_x, jogador_y)
        
        # Atualizar morcegos
        for morcego in self.morcegos:
            morcego.atualizar(jogador_x, jogador_y)

        # Atualizar demos
        for demo in self.demos:
            demo.atualizar(jogador_x, jogador_y)
        
        # Atualizar projéteis
        for proj in self.projeteis[:]:
            proj.atualizar()
            # Remover se sair da tela
            if proj.fora_da_tela(self.largura, self.altura):
                self.projeteis.remove(proj)
    
    def desenhar(self, tela):
        """Desenha todos os inimigos"""
        for bruxa in self.bruxas:
            bruxa.desenhar(tela)
        
        for morcego in self.morcegos:
            morcego.desenhar(tela)

        for demo in self.demos:
            demo.desenhar(tela)
        
        for proj in self.projeteis:
            proj.desenhar(tela)
    
    def limpar(self):
        """Limpa todos os inimigos"""
        self.bruxas.clear()
        self.morcegos.clear()
        self.demos.clear()
        self.projeteis.clear()
        self.ultimo_spawn_bruxa = pygame.time.get_ticks()
        self.ultimo_spawn_morcego = pygame.time.get_ticks()
        self.ultimo_spawn_demo = pygame.time.get_ticks()