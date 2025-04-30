import pygame

class PantallaPrincipalScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.font = pygame.font.SysFont(None, 48)
        self.botones = {
            "iniciar": pygame.Rect(100, 150, 200, 50),
            "config": pygame.Rect(100, 220, 200, 50),
            "salir": pygame.Rect(100, 290, 200, 50),
        }

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.botones["iniciar"].collidepoint(event.pos):
                    print("Iniciar juego")
                elif self.botones["config"].collidepoint(event.pos):
                    print("Configuración (por hacer)")
                elif self.botones["salir"].collidepoint(event.pos):
                    pygame.quit()
                    exit()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill((30, 30, 30))
        saludo = self.font.render(f"Hola, {self.nombre}", True, (255, 255, 0))
        pantalla.blit(saludo, (100, 50))
        for texto, rect in self.botones.items():
            pygame.draw.rect(pantalla, (100, 100, 200), rect)
            label = self.font.render(texto.capitalize(), True, (255, 255, 255))
            pantalla.blit(label, (rect.x + 10, rect.y + 10))
