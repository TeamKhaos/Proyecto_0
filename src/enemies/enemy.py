import pygame

class Enemy:
    def __init__(self, x, y, velocidad=2):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        

        # Animación
        self.frames = []
        for i in range(4):
            frame = pygame.image.load(f"assets/images/enemies/Enemy{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (64, 64))  # Ajusta el tamaño si quieres
            self.frames.append(frame)

        self.frame_actual = 0
        self.tiempo_entre_frames = 5  # Mayor = más lento, menor = más rápido
        self.contador_animacion = 0

    def mover(self):
        self.y += self.velocidad

    def actualizar_animacion(self):
        self.contador_animacion += 1
        if self.contador_animacion >= self.tiempo_entre_frames:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        self.actualizar_animacion()
        imagen = self.frames[self.frame_actual]
        pantalla.blit(imagen, (self.x, self.y))
