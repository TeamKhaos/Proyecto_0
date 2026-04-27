import pygame
import math
import random
from enemies.bala import Bala
from assets.colors import NES_RED

class Enemy:
    def __init__(self, x, y, velocidad=2):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        
        # --- IA y Movimiento ---
        self.offset_x = random.uniform(0, math.pi * 2) # Para que no todos se muevan igual
        self.amplitud = random.randint(20, 50)
        self.frecuencia = 0.05
        
        # --- Disparo ---
        self.shoot_delay = random.randint(60, 180) # Disparan cada 1-3 segundos
        self.shoot_timer = 0
        self.ancho = 64
        self.alto = 64

        # --- Animación ---
        self.frames = []
        for i in range(4):
            frame = pygame.image.load(f"assets/images/enemies/Enemy{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (64, 64))
            self.frames.append(frame)

        self.frame_actual = 0
        self.tiempo_entre_frames = 5
        self.contador_animacion = 0

    def mover(self):
        # Movimiento vertical constante
        self.y += self.velocidad
        # Movimiento horizontal en zigzag (senoidal)
        self.x += math.sin(self.y * self.frecuencia + self.offset_x) * 2

    def puede_disparar(self):
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot_delay = random.randint(100, 250)
            return True
        return False

    def disparar(self):
        # Crea una bala enemiga que baja (dirección 1)
        return Bala(self.x + 32, self.y + 64, velocidad=4, direccion=1, color=NES_RED)

    def actualizar_animacion(self):
        self.contador_animacion += 1
        if self.contador_animacion >= self.tiempo_entre_frames:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        self.actualizar_animacion()
        imagen = self.frames[self.frame_actual]
        pantalla.blit(imagen, (self.x, self.y))

    def obtener_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, 44, 44) # Rectángulo algo más pequeño para colisiones más justas
