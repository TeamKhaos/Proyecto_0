import pygame
from ui.config_scene import ConfigScene
from assets.colors import *

class PantallaPrincipalScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 72)

        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2

        self.boton_ancho = 320
        self.boton_alto = 60
        self.espacio_entre_botones = 30

        self.botones = {
            "iniciar": pygame.Rect(0, 0, self.boton_ancho, self.boton_alto),
            "configuración": pygame.Rect(0, 0, self.boton_ancho, self.boton_alto),
            "salir": pygame.Rect(0, 0, self.boton_ancho, self.boton_alto),
        }

        self._posicionar_botones()

    def _posicionar_botones(self):
        # Posiciona los botones centrados verticalmente
        total_altura = len(self.botones) * self.boton_alto + (len(self.botones) - 1) * self.espacio_entre_botones
        inicio_y = (self.alto_pantalla // 2 + 50) - total_altura // 2

        for i, rect in enumerate(self.botones.values()):
            rect.center = (self.centro_x, inicio_y + i * (self.boton_alto + self.espacio_entre_botones))

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.botones["iniciar"].collidepoint(event.pos):
                    print("Iniciar juego")  # Aquí puedes cambiar a la escena del juego
                elif self.botones["configuración"].collidepoint(event.pos):
                    from engine.scene_manager import SceneManager
                    SceneManager.cambiar_escena(ConfigScene(self.nombre))
                elif self.botones["salir"].collidepoint(event.pos):
                    pygame.quit()
                    exit()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NES_GRAY_DARK)

        # Título
        titulo = self.titulo_font.render("Nave Retro", True, NES_YELLOW)
        pantalla.blit(titulo, titulo.get_rect(center=(self.centro_x, 100)))

        # Saludo
        saludo = self.font.render(f"¡Hola, {self.nombre}!", True, NES_LIGHT_GREEN)
        pantalla.blit(saludo, saludo.get_rect(center=(self.centro_x, 180)))

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for texto, rect in self.botones.items():
            esta_sobre = rect.collidepoint(mouse_pos)
            color_boton = NES_BLUE if not esta_sobre else NES_LIGHT_BLUE

            pygame.draw.rect(pantalla, color_boton, rect, border_radius=10)
            if esta_sobre:
                pygame.draw.rect(pantalla, NES_WHITE, rect, width=3, border_radius=10)

            label = self.font.render(texto.capitalize(), True, NES_WHITE)
            pantalla.blit(label, label.get_rect(center=rect.center))
