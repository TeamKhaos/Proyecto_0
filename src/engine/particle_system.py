import pygame
import random
from assets.colors import *

class Particle:
    def __init__(self, x, y, color, tipo="rect"):
        self.x = x
        self.y = y
        self.color = color
        self.tipo = tipo
        # Velocidad aleatoria con mayor rango para explosiones más dinámicas
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        # Tiempo de vida aleatorio
        self.vida_max = random.randint(25, 50)
        self.vida = self.vida_max
        self.tamano_inicial = random.randint(3, 6)
        self.tamano = self.tamano_inicial

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        
        # Fricción suave
        self.vx *= 0.96
        self.vy *= 0.96

        self.vida -= 1
        # Escalar tamaño basado en la vida restante
        self.tamano = (self.vida / self.vida_max) * self.tamano_inicial
        return self.vida > 0

    def dibujar(self, pantalla):
        if self.tamano <= 0: return
        
        # Simular transparencia mediante el color (mezclando con el fondo negro)
        factor = self.vida / self.vida_max
        c = (int(self.color[0]*factor), int(self.color[1]*factor), int(self.color[2]*factor))
        
        if self.tipo == "circle":
            pygame.draw.circle(pantalla, c, (int(self.x), int(self.y)), int(self.tamano))
        else:
            pygame.draw.rect(pantalla, c, (int(self.x), int(self.y), int(self.tamano), int(self.tamano)))

class ParticleManager:
    def __init__(self):
        self.particulas = []

    def crear_explosion(self, x, y, color=NES_WHITE, cantidad=20, tipo="circle"):
        """Crea una explosión mejorada."""
        colores_fuego = [NES_WHITE, NES_YELLOW, NES_ORANGE, NES_RED, NES_LIGHT_BLUE]
        for _ in range(cantidad):
            c = random.choice(colores_fuego) if color == NES_WHITE else color
            self.particulas.append(Particle(x, y, c, tipo=tipo))

    def actualizar(self):
        # Actualizar y filtrar partículas muertas
        self.particulas = [p for p in self.particulas if p.actualizar()]

    def dibujar(self, pantalla):
        for p in self.particulas:
            p.dibujar(pantalla)
