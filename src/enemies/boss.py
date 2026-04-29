import pygame
import math
import random
from enemies.bala import Bala
from assets.colors import NES_RED, NES_ORANGE, NES_YELLOW

class Boss:
    def __init__(self, target=None):
        self.x = 300
        self.y = -200
        self.velocidad = 1
        self.vida = 100
        self.max_vida = 100
        self.aparecido = False
        self.derrotado = False
        self.target = target
        
        # --- Movimiento Lateral ---
        self.direccion_x = 1
        self.velocidad_x = 2
        
        # --- Disparo ---
        self.shoot_timer = 0
        self.shoot_delay = 60 
        self.ancho = 200
        self.alto = 200
        self.patron_actual = 0 # 0: Fan, 1: Spiral, 2: Targeted
        self.angulo_espiral = 0

        self.frames = []
        try:
            for i in range(4):
                frame = pygame.image.load(f"assets/images/enemies/boss{i}.png").convert_alpha()
                frame = pygame.transform.scale(frame, (200, 200))
                self.frames.append(frame)
        except:
            self.frames = [None]

        self.frame_actual = 0
        self.contador_animacion = 0
        self.tiempo_entre_frames = 6

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.vida = 0
            self.morir()
            
    def morir(self):
        if not self.derrotado:
            self.derrotado = True
            self.aparecido = False

    def aparecer(self):
        self.aparecido = True

    def mover(self):
        if not self.aparecido: return

        # Entrada inicial
        if self.y < 80:
            self.y += self.velocidad
        else:
            # Movimiento lateral
            self.x += self.velocidad_x * self.direccion_x
            if self.x <= 50 or self.x >= 550:
                self.direccion_x *= -1

    def puede_disparar(self):
        if not self.aparecido or self.y < 80: return False
        self.shoot_timer += 1
        
        # Cambiar patrón según la vida
        if self.vida > 70: self.patron_actual = 0
        elif self.vida > 40: self.patron_actual = 1
        else: self.patron_actual = 2

        current_delay = self.shoot_delay
        if self.patron_actual == 1: current_delay = 15 # Espiral dispara rápido
        if self.patron_actual == 2: current_delay = 45 # Targeted
            
        if self.shoot_timer >= current_delay:
            self.shoot_timer = 0
            return True
        return False

    def disparar(self):
        balas = []
        cx, cy = self.x + 100, self.y + 180
        
        if self.patron_actual == 0: # Fan
            for angulo in range(-30, 31, 15):
                rad = math.radians(angulo + 90)
                vx = math.cos(rad) * 4
                vy = math.sin(rad) * 4
                balas.append(Bala(cx, cy, vx=vx, vy=vy, color=NES_RED))
        
        elif self.patron_actual == 1: # Spiral
            rad = math.radians(self.angulo_espiral)
            vx = math.cos(rad) * 5
            vy = math.sin(rad) * 5
            balas.append(Bala(cx, cy, vx=vx, vy=vy, color=NES_ORANGE))
            self.angulo_espiral += 25
            if self.angulo_espiral >= 360: self.angulo_espiral = 0
            
        elif self.patron_actual == 2: # Targeted
            if self.target:
                tx, ty = self.target.x + 32, self.target.y + 32
                dist_x = tx - cx
                dist_y = ty - cy
                magnitud = math.sqrt(dist_x**2 + dist_y**2)
                if magnitud > 0:
                    vx = (dist_x / magnitud) * 6
                    vy = (dist_y / magnitud) * 6
                    balas.append(Bala(cx, cy, vx=vx, vy=vy, color=NES_YELLOW))
            else:
                balas.append(Bala(cx, cy, velocidad=6, direccion=1, color=NES_YELLOW))
                
        return balas

    def actualizar_animacion(self):
        if not self.frames[0]: return
        self.contador_animacion += 1
        if self.contador_animacion >= self.tiempo_entre_frames:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        if self.aparecido:
            self.actualizar_animacion()
            if self.frames[0]:
                pantalla.blit(self.frames[self.frame_actual], (self.x, self.y))
            else:
                pygame.draw.rect(pantalla, NES_RED, (self.x + 20, self.y + 20, 160, 160))

    def obtener_rect(self):
        return pygame.Rect(self.x + 20, self.y + 20, 160, 160)
