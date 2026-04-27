import pygame
from assets.colors import *

class Bala:
    """Representa un proyectil en el juego, usado tanto por jugadores como por enemigos."""
    def __init__(self, x, y, velocidad=7, direccion=-1, color=NES_WHITE):
        """
        Inicializa la bala.
        :param x: Posición X inicial.
        :param y: Posición Y inicial.
        :param velocidad: Rapidez de movimiento.
        :param direccion: -1 para subir (jugador), 1 para bajar (enemigo).
        :param color: Color del proyectil.
        """
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.direccion = direccion
        self.color = color
        self.radio = 4

    def mover(self):
        # Actualiza la posición basándose en la dirección (1 o -1)
        self.y += (self.velocidad * self.direccion)

    def dibujar(self, pantalla):
        # Dibuja la bala como un círculo
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)

    def obtener_rect(self):
        # Devuelve el rectángulo de colisión
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
