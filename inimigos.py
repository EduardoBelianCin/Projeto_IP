import pygame
from random import randint

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, vida, velocidade):
        super().__init__()

        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vida = vida
        self.velocidade = velocidade
        self.vivo = True

        info = pygame.display.Info()
        largura_desktop = info.current_w
        largura_desktop = info.current_h
    
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
        self.rect.x -= self.velocidade

class Morcego(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y, vida=1, velocidade=3)

class Bruxa(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y, vida=1, velocidade=10)

        def movimentacao():
            self.rect.x = randint(0, self.largura_desktop)

class Diabrete(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y, vida=1, velocidade=15)

class Touro(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y, vida=5, velocidade=3)