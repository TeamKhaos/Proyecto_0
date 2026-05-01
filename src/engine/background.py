import pygame
import random
from assets.colors import *

class Estrella:
    def __init__(self, x, y, velocidad, tamano, color):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.tamano = tamano
        self.color = color

    def mover(self, alto_pantalla):
        self.y += self.velocidad
        if self.y > alto_pantalla:
            self.y = 0
            self.x = random.randint(0, 800)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.tamano)

class ObjetoEspacial:
    def __init__(self, ancho_pantalla, alto_pantalla, esquema="default"):
        self.ancho_p = ancho_pantalla
        self.alto_p = alto_pantalla
        self.reset()
        self.esquema = esquema

    def reset(self):
        self.x = random.randint(0, self.ancho_p)
        self.y = -random.randint(200, 1000) # Aparece arriba
        self.velocidad = random.uniform(0.3, 0.8)
        self.tamano = random.randint(40, 100)
        
        # Color basado en esquema
        if hasattr(self, 'esquema'):
            if self.esquema == "nivel_2":
                self.color = random.choice([NES_BLUE, (50, 0, 100), (0, 0, 150)])
            elif self.esquema == "nivel_3":
                self.color = random.choice([NES_ORANGE, NES_RED, (100, 0, 0)])
            else:
                self.color = random.choice([NES_GRAY, (30, 30, 60), (0, 50, 100)])
        else:
            self.color = (50, 50, 80)

    def mover(self):
        self.y += self.velocidad
        if self.y > self.alto_p + self.tamano:
            self.reset()

    def dibujar(self, pantalla):
        # Dibujar un círculo con un borde para simular un planeta/nebulosa
        # Usamos una superficie con alpha para que no sea un bloque sólido
        surf = pygame.Surface((self.tamano * 2, self.tamano * 2), pygame.SRCALPHA)
        # Dibujar núcleo difuminado (simulado con círculos concéntricos)
        for i in range(5):
            alpha = 100 - (i * 20)
            r = self.tamano - (i * (self.tamano // 5))
            if r > 0:
                pygame.draw.circle(surf, (*self.color, alpha), (self.tamano, self.tamano), r)
        
        pantalla.blit(surf, (int(self.x - self.tamano), int(self.y - self.tamano)))

class ParallaxManager:
    def __init__(self, ancho, alto, esquema="default"):
        self.ancho = ancho
        self.alto = alto
        self.capas = []
        self.objetos_espaciales = [ObjetoEspacial(ancho, alto, esquema) for _ in range(2)]
        
        if esquema == "nivel_2":
            colores = [NES_GRAY, NES_BLUE, NES_LIGHT_BLUE]
            densidades = [100, 50, 20]
        elif esquema == "nivel_3":
            colores = [NES_GRAY, NES_ORANGE, NES_RED]
            densidades = [120, 60, 25]
        else: # nivel 1 o default
            colores = [NES_GRAY, NES_WHITE, NES_LIGHT_BLUE]
            densidades = [80, 40, 15]

        # Capa lejana
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(0.1, 0.5), 1, colores[0]) for _ in range(densidades[0])])
        # Capa media
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(0.6, 1.2), 2, colores[1]) for _ in range(densidades[1])])
        # Capa cercana
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(1.5, 2.5), 3, colores[2]) for _ in range(densidades[2])])

    def actualizar(self):
        for capa in self.capas:
            for estrella in capa:
                estrella.mover(self.alto)
        for obj in self.objetos_espaciales:
            obj.mover()

    def dibujar(self, pantalla):
        # Dibujar primero los objetos lejanos (planetas)
        for obj in self.objetos_espaciales:
            obj.dibujar(pantalla)
            
        for capa in self.capas:
            for estrella in capa:
                estrella.dibujar(pantalla)
