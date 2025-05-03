import pygame

class BalaEnemiga:
    def __init__(self, x, y, velocidad=5):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.imagen = pygame.image.load("assets/images/enemies/bala1.png").convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (16, 32))  # Ajusta tamaño

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def fuera_de_pantalla(self, alto_pantalla):
        return self.y > alto_pantalla
