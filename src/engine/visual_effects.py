import pygame
import random

class ScreenShake:
    def __init__(self):
        self.duracion = 0
        self.intensidad = 0
        self.offset_x = 0
        self.offset_y = 0

    def activar(self, duracion, intensidad):
        self.duracion = duracion
        self.intensidad = intensidad

    def actualizar(self):
        if self.duracion > 0:
            self.offset_x = random.randint(-self.intensidad, self.intensidad)
            self.offset_y = random.randint(-self.intensidad, self.intensidad)
            self.duracion -= 1
        else:
            self.offset_x = 0
            self.offset_y = 0

    def aplicar(self, pantalla_virtual):
        if self.offset_x != 0 or self.offset_y != 0:
            temp_surf = pantalla_virtual.copy()
            pantalla_virtual.fill((0, 0, 0))
            pantalla_virtual.blit(temp_surf, (self.offset_x, self.offset_y))

class HealthBar:
    def __init__(self, x, y, ancho, alto, color_base):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color_base = color_base
        self.vida_visual = 100.0
        self.vida_objetivo = 100.0

    def actualizar(self, vida_actual, max_vida):
        self.vida_objetivo = (vida_actual / max_vida) * self.ancho if max_vida > 0 else 0
        # Interpolación suave (Lerp) para el efecto de barra que baja lento
        self.vida_visual += (self.vida_objetivo - self.vida_visual) * 0.1

    def dibujar(self, pantalla):
        # Fondo
        pygame.draw.rect(pantalla, (40, 40, 40), (self.x, self.y, self.ancho, self.alto))
        # Barra de daño (blanca, detrás de la principal)
        if abs(self.vida_visual - self.vida_objetivo) > 1:
            pygame.draw.rect(pantalla, (200, 200, 200), (self.x, self.y, self.vida_visual, self.alto))
        # Barra principal
        pygame.draw.rect(pantalla, self.color_base, (self.x, self.y, self.vida_objetivo, self.alto))
        # Borde brillante
        pygame.draw.rect(pantalla, (255, 255, 255), (self.x - 2, self.y - 2, self.ancho + 4, self.alto + 4), 1)
