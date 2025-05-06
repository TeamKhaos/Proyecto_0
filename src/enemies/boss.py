import pygame

class Boss:
    def __init__(self):
        
        self.x = 300
        self.y = -150
        self.velocidad = 1
        self.aparecido = False

        # Cargar los 6 frames de animación del boss
        self.frames = []
        for i in range(4):
            frame = pygame.image.load(f"assets/images/enemies/boss{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (200, 200))
            self.frames.append(frame)


        self.frame_actual = 0
        self.contador_animacion = 0
        self.tiempo_entre_frames = 6  # Ajusta según qué tan rápido quieras que se anime

    def aparecer(self):
        self.aparecido = True

    def mover(self):
        if self.aparecido and self.y < 100:
            self.y += self.velocidad

    def actualizar_animacion(self):
        self.contador_animacion += 1
        if self.contador_animacion >= self.tiempo_entre_frames:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        if self.aparecido:
            self.actualizar_animacion()
            pantalla.blit(self.frames[self.frame_actual], (self.x, self.y))
