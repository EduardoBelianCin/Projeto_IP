import pygame
import os

class Hud():
    def draw_hud(self, tela, font, pontos, diamantes, moedas, maçãs, vida, hud_sprites):

        linha1 = font.render(f"Pontos: {pontos}", True, (255,255,255))
        linha2 = font.render(f"diamantes: {diamantes}", True, (255,255,255))
        linha3 = font.render(f"Moedas: {moedas}", True, (255,255,255))
        linha4 = font.render(f"maçãs: {maçãs}", True, (255,255,255))

        tela.blit(linha1, (20, 125))
        tela.blit(linha2, (20, 45))
        tela.blit(linha3, (20, 70))
        tela.blit(linha4, (20, 95))

        if vida >= 90:
            sprite_key = "Vida10"
        elif vida >= 80:
            sprite_key = "vida9"
        elif vida >= 70:
            sprite_key = "vida8"
        elif vida >= 60:
            sprite_key = "vida7"
        elif vida >= 50:
            sprite_key = "vida6"
        elif vida >= 40:
            sprite_key = "vida5"
        elif vida >= 30:
            sprite_key = "vida4"
        elif vida >= 20:
            sprite_key = "vida3"
        elif vida >= 10:
            sprite_key = "vida2"
        elif vida >= 1:
            sprite_key = "vida1"
        else:
            sprite_key = "vida0"

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