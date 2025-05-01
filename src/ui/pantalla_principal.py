import pygame
from ui.config_scene import ConfigScene
from assets.colors import *

class PantallaPrincipalScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 48)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 72)
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        self.centro_y = self.alto_pantalla // 2
        self.boton_ancho = 280
        self.boton_alto = 70
        self.espacio_vertical_titulo = 120 # Más espacio entre título y saludo
        self.espacio_vertical_botones = 90 # Aún más espacio entre botones
        self.boton_color_normal = NES_BLUE
        self.boton_color_hover = NES_LIGHT_BLUE
        self.boton_texto_color = NES_WHITE

        # Calcular la posición vertical del primer botón
        self.primer_boton_y = self.centro_y + 30 # Mover los botones un poco hacia abajo

        self.botones = {
            "iniciar": pygame.Rect(self.centro_x - self.boton_ancho // 2, self.primer_boton_y - self.espacio_vertical_botones, self.boton_ancho, self.boton_alto),
            "configuración": pygame.Rect(self.centro_x - self.boton_ancho // 2, self.primer_boton_y, self.boton_ancho, self.boton_alto),
            "salir": pygame.Rect(self.centro_x - self.boton_ancho // 2, self.primer_boton_y + self.espacio_vertical_botones, self.boton_ancho, self.boton_alto),
        }

    def manejar_eventos(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.botones["iniciar"].collidepoint(event.pos):
                    print("Iniciar juego")
                    # Aquí iría la lógica para iniciar el juego
                elif self.botones["configuración"].collidepoint(event.pos):
                    from engine.scene_manager import SceneManager
                    SceneManager.cambiar_escena(ConfigScene(self.nombre))
                elif self.botones["salir"].collidepoint(event.pos):
                    pygame.quit()
                    exit()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)

        # Título centrado en la parte superior
        titulo = self.titulo_font.render("Nave Retro", True, NES_YELLOW)
        titulo_rect = titulo.get_rect(center=(self.centro_x, 100))
        pantalla.blit(titulo, titulo_rect)

        # Saludo al jugador centrado debajo del título con más espacio
        saludo = self.font.render(f"¡Hola, {self.nombre}!", True, NES_LIGHT_GREEN)
        saludo_rect = saludo.get_rect(center=(self.centro_x, 100 + self.espacio_vertical_titulo))
        pantalla.blit(saludo, saludo_rect)

        # Dibujar los botones con más espacio entre ellos
        for texto, rect in self.botones.items():
            color_boton = self.boton_color_normal
            if rect.collidepoint(pygame.mouse.get_pos()):
                color_boton = self.boton_color_hover
                pygame.draw.rect(pantalla, NES_WHITE, rect, 3)

            pygame.draw.rect(pantalla, color_boton, rect, border_radius=8)
            label = self.font.render(texto.capitalize(), True, self.boton_texto_color)
            label_rect = label.get_rect(center=rect.center)
            pantalla.blit(label, label_rect)