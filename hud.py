import pygame
import os

class Hud():
    def draw_hud(self, tela, font, pontos, diamantes, moedas, maçãs, vida, hud_sprites):

        padding = 10
        bg_surface = pygame.Surface((275, 155))
        bg_surface.set_alpha(180)
        bg_surface.fill((0,0,0))

        tela.blit(bg_surface, (8,10))

        linha1 = font.render(f"Maçãs: {maçãs}", True, (255,255,255))
        linha2 = font.render(f"Moedas: {moedas}", True, (255,255,255))
        linha3 = font.render(f"Diamantes: {diamantes}", True, (255,255,255))
        linha_score = font.render(f"Pontuação: {pontos}", True, (255,255,255))

        mult_scale = 1.2
        imagem_maca = pygame.image.load("sprites/itens/maca.png")
        imagem_maca = pygame.transform.scale(imagem_maca, (68*mult_scale, 37*mult_scale))
        imagem_moeda = pygame.image.load("sprites/itens/moeda.png")
        imagem_moeda = pygame.transform.scale(imagem_moeda, (68*mult_scale, 37*mult_scale))
        imagem_dima = pygame.image.load("sprites/itens/diamante.png")
        imagem_dima = pygame.transform.scale(imagem_dima, (68*mult_scale*0.8, 37*mult_scale*0.8))

        tela.blit(linha1, (50, 45))
        tela.blit(imagem_maca, (-10, 42))
        tela.blit(linha2, (50, 70))
        tela.blit(imagem_moeda, (-10, 67))
        tela.blit(linha3, (50, 95))
        tela.blit(imagem_dima, (-2, 95))
        tela.blit(linha_score, (20, 125))

        if vida >= 100:
            sprite_key = "Vida10"
        elif vida >= 90:
            sprite_key = "Vida9"
        elif vida >= 80:
            sprite_key = "Vida8"
        elif vida >= 70:
            sprite_key = "Vida7"
        elif vida >= 60:
            sprite_key = "Vida6"
        elif vida >= 50:
            sprite_key = "Vida5"
        elif vida >= 40:
            sprite_key = "Vida4"
        elif vida >= 30:
            sprite_key = "Vida3"
        elif vida >= 20:
            sprite_key = "Vida2"
        elif vida >= 10:
            sprite_key = "Vida1"
        else:
            sprite_key = "Vida0"

        if sprite_key in hud_sprites:
            sprite_vida = hud_sprites[sprite_key]
            tela.blit(sprite_vida, (10, 15))

        tela.blit(sprite_vida, (10, 15))

    def load_hud_sprites(self, arquivos):    # Barra de vida
        hud_sprites = {}
        for filename in os.listdir(arquivos):
            if filename.endswith(".png"):
                key = os.path.splitext(filename)[0]
                img = pygame.image.load(os.path.join(arquivos, filename)).convert_alpha()
                img = pygame.transform.scale(img, (270, 30))
                hud_sprites[key] = img
        return hud_sprites
    
    def cursor_customizado(self):     # Cursor do mouse personalizado
        self.cursor = pygame.image.load("sprites/cursor.png").convert_alpha()
        pygame.mouse.set_visible(False)
        return self.cursor