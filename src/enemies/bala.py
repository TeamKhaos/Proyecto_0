import pygame
from assets.colors import *
class BalaEnemiga:
    # Representa una bala disparada por un enemigo en el juego.
    def __init__(self, x, y):
        # Inicializa la bala con una posición, velocidad y radio.
        # x (int): La coordenada x inicial de la bala.
        # y (int): La coordenada y inicial de la bala.
        self.x = x
        self.y = y
        self.velocidad = 7
        self.radio = 3
    def mover(self):
        # Actualiza la posición de la bala, moviéndola hacia arriba en la pantalla.
        self.y -= self.velocidad
    def dibujar(self, pantalla):
        # Dibuja la bala en la pantalla como un círculo.
        # pantalla (pygame.Surface): La superficie de la pantalla donde se dibujará la bala.
        # Dibuja la bala como un círculo, usando el color NES_WHITE
        pygame.draw.circle(pantalla, NES_WHITE, (self.x, self.y), self.radio)
    def obtener_rect(self):
        # Devuelve un objeto pygame.Rect que representa el área de colisión de la bala.
        # Pygame.Rect: El rectángulo de colisión de la bala.
        # Crea y devuelve un rectángulo para la detección de colisiones
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)