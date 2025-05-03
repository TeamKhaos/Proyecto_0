import pygame

class Boss:
    def __init__(self):
        self.x = 300
        self.y = -150
        self.velocidad = 1
        self.aparecido = False

        # Cargar sprite del jefe
        self.imagen = pygame.image.load("assets/images/boss.png").convert_alpha()
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()

    def aparecer(self):
        self.aparecido = True

    def mover(self):
        if self.aparecido and self.y < 100:
            self.y += self.velocidad

    def dibujar(self, pantalla):
        if self.aparecido:
            pantalla.blit(self.imagen, (self.x, self.y))
