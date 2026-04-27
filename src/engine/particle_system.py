import pygame
import random
from assets.colors import *

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        # Velocidad aleatoria en ambas direcciones
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        # Tiempo de vida aleatorio (frames)
        self.vida = random.randint(20, 40)
        self.tamano = random.randint(2, 5)

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        
        # Fricción: reduce velocidad gradualmente
        self.vx *= 0.95
        self.vy *= 0.95

        self.vida -= 1
        # Reducir tamaño gradualmente
        if self.vida % 8 == 0 and self.tamano > 1:
            self.tamano -= 1
        return self.vida > 0

    def dibujar(self, pantalla):
        # Dibujar como rectángulos para un look más retro/pixelado
        pygame.draw.rect(pantalla, self.color, (int(self.x), int(self.y), self.tamano, self.tamano))

class ParticleManager:
    def __init__(self):
        self.particulas = []

    def crear_explosion(self, x, y, color=NES_WHITE, cantidad=15):
        """Crea una explosión de partículas en la posición dada."""
        colores_fuego = [NES_WHITE, NES_YELLOW, NES_ORANGE, NES_RED]
        for _ in range(cantidad):
            # Elegir un color aleatorio si es blanco por defecto o usar el color dado
            c = random.choice(colores_fuego) if color == NES_WHITE else color
            self.particulas.append(Particle(x, y, c))

    def actualizar(self):
        # Actualizar y filtrar partículas muertas
        self.particulas = [p for p in self.particulas if p.actualizar()]

    def dibujar(self, pantalla):
        for p in self.particulas:
            p.dibujar(pantalla)
