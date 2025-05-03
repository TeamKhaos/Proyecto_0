import pygame

class Enemy:
    def __init__(self, x, y, velocidad=2):
        self.x = x
        self.y = y
        self.velocidad = velocidad

        # Cargar sprite del enemigo
        self.imagen = pygame.image.load("assets/images/enemy.png").convert_alpha()
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
