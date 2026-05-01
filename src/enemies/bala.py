import pygame
from assets.colors import *

class Bala:
    """Representa un proyectil mejorado con efectos visuales."""
    def __init__(self, x, y, velocidad=7, direccion=-1, color=NES_WHITE, vx=0, vy=None):
        self.x = x
        self.y = y
        self.vx = vx
        if vy is None:
            self.vy = velocidad * direccion
        else:
            self.vy = vy
            
        self.color = color
        self.radio = 4
        
        # Historial para la estela (trail)
        self.historial = []
        self.max_historial = 5

    def mover(self):
        # Guardar posición para la estela
        self.historial.insert(0, (self.x, self.y))
        if len(self.historial) > self.max_historial:
            self.historial.pop()

        self.x += self.vx
        self.y += self.vy

    def dibujar(self, pantalla):
        # 1. Dibujar Estela (Trail)
        for i, (hx, hy) in enumerate(self.historial):
            # Desvanecimiento de color y tamaño
            alpha = 150 - (i * 30)
            if alpha < 0: alpha = 0
            radio_trail = self.radio - (i * 0.5)
            if radio_trail < 1: radio_trail = 1
            
            # Dibujar círculo de estela con transparencia (simulada con color más oscuro sobre negro)
            # Para un glow real se usaría una superficie con alpha, pero esto es más rápido
            factor = alpha / 255
            c_trail = (self.color[0]*factor, self.color[1]*factor, self.color[2]*factor)
            pygame.draw.circle(pantalla, c_trail, (int(hx), int(hy)), int(radio_trail))

        # 2. Dibujar Brillo (Glow) exterior
        glow_color = (min(self.color[0] + 50, 255), min(self.color[1] + 50, 255), min(self.color[2] + 50, 255))
        pygame.draw.circle(pantalla, glow_color, (int(self.x), int(self.y)), self.radio + 2)
        
        # 3. Dibujar Núcleo (Core)
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)
        # Un pequeño punto blanco en el centro para el brillo
        pygame.draw.circle(pantalla, NES_WHITE, (int(self.x), int(self.y)), self.radio // 2)

    def obtener_rect(self):
        # Devuelve el rectángulo de colisión
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

class BalaGranada(Bala):
    """Proyectil especial que explota al tocar el suelo."""
    def __init__(self, x, y, velocidad=5, color=NES_ORANGE):
        super().__init__(x, y, velocidad=velocidad, direccion=1, color=color)
        self.radio = 18 # Proyectil gigante
        self.explotada = False

    def mover(self):
        super().mover()
        # Si toca el borde inferior (aprox 600), marca para explotar
        if self.y >= 580 and not self.explotada:
            self.explotada = True
            return True # Señal para el manager de que debe generar fragmentos
        return False
