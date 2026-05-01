import pygame
from engine.asset_manager import AssetManager
from assets.colors import *

class Nave:
    def __init__(self, x=None, y=None, skin="default"):
        self.x = x if x is not None else 368
        self.y = y if y is not None else 500
        self.velocidad = 7
        self.ancho = 64
        self.alto = 64
        self.vida = 100
        self.max_vida = 100
        self.skin = skin
        self.powerup_escopeta = False
        self.timer_powerup = 0
        self.tiempo_creacion = pygame.time.get_ticks()

        # --- Efecto RGB / Ghosting ---
        self.historial_posiciones = [] # Lista de (x, y, frame_img)
        self.max_ghosts = 5
        self.contador_rgb = 0

        # Cargar frames usando AssetManager
        self.frames = []
        base_path = f"assets/images/player/nave_{self.skin}"
        if self.skin == "default":
             base_path = f"assets/images/player/nave_default"
        else:
             base_path = f"assets/images/player/nave_{self.skin}_"

        for i in range(1, 4):
            img_path = f"{base_path}{i}.png"
            img = AssetManager.get_image(img_path, (self.ancho, self.alto))
            self.frames.append(img)

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0: self.vida = 0

    def mover(self, teclas):
        moviendose = False
        old_x, old_y = self.x, self.y

        if teclas[pygame.K_w] and self.y > 0: self.y -= self.velocidad; moviendose = True
        if teclas[pygame.K_s] and self.y < 600 - self.alto: self.y += self.velocidad; moviendose = True
        if teclas[pygame.K_a] and self.x > 0: self.x -= self.velocidad; moviendose = True
        if teclas[pygame.K_d] and self.x < 800 - self.ancho: self.x += self.velocidad; moviendose = True
        
        # Lógica de estelas (Ghosts)
        if moviendose:
            self.historial_posiciones.insert(0, (old_x, old_y, self.obtener_frame_actual()))
            if len(self.historial_posiciones) > self.max_ghosts:
                self.historial_posiciones.pop()
        else:
            if self.historial_posiciones: self.historial_posiciones.pop()

        if self.powerup_escopeta:
            self.timer_powerup -= 1
            if self.timer_powerup <= 0:
                self.powerup_escopeta = False

    def obtener_frame_actual(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_creacion < 1500:
            return 0
        teclas = pygame.key.get_pressed()
        moviendose = teclas[pygame.K_w] or teclas[pygame.K_s] or teclas[pygame.K_a] or teclas[pygame.K_d]
        return 2 if moviendose else 1

    def dibujar(self, pantalla):
        if not self.frames[0]: return

        # 1. Dibujar Estelas RGB (Ghosts)
        self.contador_rgb = (self.contador_rgb + 10) % 360
        for i, (gx, gy, gframe) in enumerate(self.historial_posiciones):
            alpha = 150 - (i * 30)
            if alpha < 0: alpha = 0
            
            # Crear superficie para el ghost con efecto de color
            ghost_surf = self.frames[gframe].copy()
            
            # Efecto RGB: Ciclo de colores basado en el tiempo
            hue = (self.contador_rgb + i * 20) % 360
            color = pygame.Color(0)
            color.hsva = (hue, 80, 100, 100)
            
            # Aplicar color al ghost
            ghost_surf.fill((color.r, color.g, color.b, alpha), special_flags=pygame.BLEND_RGBA_MULT)
            pantalla.blit(ghost_surf, (gx, gy))

        # 2. Dibujar Nave Principal
        frame_idx = self.obtener_frame_actual()
        
        if self.powerup_escopeta and (pygame.time.get_ticks() // 100) % 2 == 0:
            s = self.frames[frame_idx].copy()
            s.fill((0, 255, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            pantalla.blit(s, (self.x, self.y))
        else:
            pantalla.blit(self.frames[frame_idx], (self.x, self.y))

    def obtener_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, self.ancho - 20, self.alto - 20)
