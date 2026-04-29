import pygame
import random
from assets.colors import NES_YELLOW, NES_WHITE, NES_GREEN

class PowerUp:
    def __init__(self, x, y, tipo="escopeta"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = 3
        self.ancho = 32
        self.alto = 32
        self.radio = 16

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        # Dibujar una caja retro con una 'S' (Shotgun/Spread)
        color = NES_GREEN if self.tipo == "escopeta" else NES_YELLOW
        pygame.draw.rect(pantalla, NES_WHITE, (self.x, self.y, self.ancho, self.alto), 2)
        pygame.draw.rect(pantalla, color, (self.x + 4, self.y + 4, self.ancho - 8, self.alto - 8))
        
        # Dibujar una 'S' simple
        fuente = pygame.font.SysFont("Arial", 20, bold=True)
        txt = fuente.render("S", True, NES_WHITE)
        pantalla.blit(txt, txt.get_rect(center=(self.x + self.ancho//2, self.y + self.alto//2)))

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
