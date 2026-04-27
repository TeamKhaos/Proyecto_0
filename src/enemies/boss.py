import pygame
import math
import random
from enemies.bala import Bala
from assets.colors import NES_RED

class Boss:
    def __init__(self):
        self.x = 300
        self.y = -200
        self.velocidad = 1
        self.vida = 100
        self.max_vida = 100
        self.aparecido = False
        self.derrotado = False
        
        # --- Movimiento Lateral ---
        self.direccion_x = 1
        self.velocidad_x = 2
        
        # --- Disparo ---
        self.shoot_timer = 0
        self.shoot_delay = 60 # Dispara cada segundo
        self.ancho = 200
        self.alto = 200

        self.frames = []
        for i in range(4):
            frame = pygame.image.load(f"assets/images/enemies/boss{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (200, 200))
            self.frames.append(frame)

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
            print("¡El jefe ha sido derrotado!")

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
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return True
        return False

    def disparar(self):
        # Disparo triple en abanico
        balas = []
        # Bala central
        balas.append(Bala(self.x + 100, self.y + 180, velocidad=5, direccion=1, color=NES_RED))
        return balas

    def actualizar_animacion(self):
        self.contador_animacion += 1
        if self.contador_animacion >= self.tiempo_entre_frames:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        if self.aparecido:
            self.actualizar_animacion()
            pantalla.blit(self.frames[self.frame_actual], (self.x, self.y))

    def obtener_rect(self):
        return pygame.Rect(self.x + 20, self.y + 20, 160, 160)
