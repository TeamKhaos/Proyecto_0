import pygame
import math
import random
from enemies.bala import Bala
from assets.colors import NES_RED

class Enemy:
    def __init__(self, x, y, velocidad=2, ia_type="zigzag", target=None):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.ia_type = ia_type
        self.target = target
        
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
        try:
            for i in range(4):
                frame = pygame.image.load(f"assets/images/enemies/Enemy{i}.png").convert_alpha()
                frame = pygame.transform.scale(frame, (64, 64))
                self.frames.append(frame)
        except:
            # Fallback
            self.frames = [None]

        self.frame_actual = 0
        self.tiempo_entre_frames = 5
        self.contador_animacion = 0

    def mover(self):
        if self.ia_type == "zigzag":
            # Movimiento vertical constante
            self.y += self.velocidad
            # Movimiento horizontal en zigzag (senoidal)
            self.x += math.sin(self.y * self.frecuencia + self.offset_x) * 2
        elif self.ia_type == "tracker":
            # Persigue horizontalmente al jugador mientras baja
            self.y += self.velocidad
            if self.target:
                target_center_x = self.target.x + self.target.ancho // 2
                enemy_center_x = self.x + self.ancho // 2
                if enemy_center_x < target_center_x:
                    self.x += 1.5
                elif enemy_center_x > target_center_x:
                    self.x -= 1.5
        elif self.ia_type == "kamikaze":
            # Baja rápido directamente
            self.y += self.velocidad * 1.5

    def puede_disparar(self):
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            # En oleadas avanzadas o tipos especiales, disparan más seguido
            self.shoot_delay = random.randint(80, 200)
            return True
        return False

    def disparar(self):
        # Si es un tracker, apunta ligeramente hacia el jugador
        vx = 0
        if self.ia_type == "tracker" and self.target:
            target_center_x = self.target.x + self.target.ancho // 2
            enemy_center_x = self.x + self.ancho // 2
            # Calcular vx para ir hacia el jugador
            dist_x = target_center_x - enemy_center_x
            dist_y = (self.target.y + self.target.alto // 2) - (self.y + self.alto)
            
            if dist_y > 0:
                # Normalizar y escalar por la velocidad de la bala (ej 4)
                magnitud = math.sqrt(dist_x**2 + dist_y**2)
                vx = (dist_x / magnitud) * 4
                vy = (dist_y / magnitud) * 4
                return Bala(self.x + 32, self.y + 64, vx=vx, vy=vy, color=NES_RED)

        # Disparo estándar
        return Bala(self.x + 32, self.y + 64, velocidad=4, direccion=1, color=NES_RED)

    def actualizar_animacion(self):
        if not self.frames[0]: return
        self.contador_animacion += 1
        if self.contador_animacion >= self.tiempo_entre_frames:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        self.actualizar_animacion()
        if self.frames[0]:
            imagen = self.frames[self.frame_actual]
            pantalla.blit(imagen, (self.x, self.y))
        else:
            pygame.draw.rect(pantalla, NES_RED, (self.x + 10, self.y + 10, 44, 44))

    def obtener_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, 44, 44)
