import pygame
from assets.colors import *

class Bala:
    """Representa un proyectil en el juego, usado tanto por jugadores como por enemigos."""
    def __init__(self, x, y, velocidad=7, direccion=-1, color=NES_WHITE, vx=0, vy=None):
        """
        Inicializa la bala.
        :param x: Posición X inicial.
        :param y: Posición Y inicial.
        :param velocidad: Rapidez de movimiento (si vy no se especifica).
        :param direccion: -1 para subir (jugador), 1 para bajar (enemigo). Usado si vy es None.
        :param color: Color del proyectil.
        :param vx: Velocidad horizontal.
        :param vy: Velocidad vertical. Si es None, se calcula con velocidad * direccion.
        """
        self.x = x
        self.y = y
        self.vx = vx
        if vy is None:
            self.vy = velocidad * direccion
        else:
            self.vy = vy
            
        self.color = color
        self.radio = 4

    def mover(self):
        # Actualiza la posición basándose en las velocidades
        self.x += self.vx
        self.y += self.vy

    def dibujar(self, pantalla):
        # Dibuja la bala como un círculo
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)

    def obtener_rect(self):
        # Devuelve el rectángulo de colisión
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
