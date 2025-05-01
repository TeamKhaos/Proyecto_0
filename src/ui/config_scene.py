import pygame
from settings import WIDTH, HEIGHT, FULLSCREEN
from engine.scene_manager import SceneManager
from assets.colors import * # Importa la paleta de colores

class ConfigScene:
    def __init__(self, nombre):
        self.nombre = nombre
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 40)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 60)
        self.titulo = self.titulo_font.render("Configuración", True, NES_YELLOW)

        self.fullscreen = FULLSCREEN
        self.volumen = 0.5

        self.boton_ancho = 530
        self.boton_alto = 60
        self.x_boton = WIDTH // 2 - self.boton_ancho // 2

        # Nuevas posiciones
        self.y_fs = 150
        self.y_vol = 270
        self.y_barra = self.y_vol + 50
        self.y_volumen_botones = self.y_barra + 30
        self.y_volver = self.y_volumen_botones + 100

        self.boton_fullscreen_rect = pygame.Rect(self.x_boton, self.y_fs, self.boton_ancho, self.boton_alto)

        # Volumen - botones y barra
        self.boton_volumen_menos_rect = pygame.Rect(self.x_boton, self.y_volumen_botones, 50, 50)
        self.boton_volumen_mas_rect = pygame.Rect(self.x_boton + self.boton_ancho - 50, self.y_volumen_botones, 50, 50)

        self.barra_x = self.boton_volumen_menos_rect.right + 10
        self.barra_ancho = self.boton_volumen_mas_rect.left - self.barra_x - 10
        self.barra_y = self.y_volumen_botones + 20
        self.barra_alto = 10

        self.boton_volver_rect = pygame.Rect(self.x_boton, self.y_volver, self.boton_ancho, self.boton_alto)

        self.boton_color_normal = NES_BLUE
        self.boton_color_hover = NES_LIGHT_BLUE
        self.texto_color = NES_WHITE
        self.accent_color = NES_YELLOW

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_fullscreen_rect.collidepoint(evento.pos):
                    self.fullscreen = not self.fullscreen
                    flags = pygame.FULLSCREEN if self.fullscreen else 0
                    pygame.display.set_mode((WIDTH, HEIGHT), flags)
                elif self.boton_volumen_mas_rect.collidepoint(evento.pos):
                    self.volumen = min(1.0, self.volumen + 0.1)
                    pygame.mixer.music.set_volume(self.volumen)
                elif self.boton_volumen_menos_rect.collidepoint(evento.pos):
                    self.volumen = max(0.0, self.volumen - 0.1)
                    pygame.mixer.music.set_volume(self.volumen)
                elif self.boton_volver_rect.collidepoint(evento.pos):
                    from ui.main_menu import PantallaPrincipalScene
                    SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)

        # Título
        pantalla.blit(self.titulo, (WIDTH // 2 - self.titulo.get_width() // 2, 60))

        mouse_pos = pygame.mouse.get_pos()

        # --- Pantalla completa ---
        pygame.draw.rect(pantalla, self.boton_color_hover if self.boton_fullscreen_rect.collidepoint(mouse_pos) else self.boton_color_normal,
                        self.boton_fullscreen_rect, border_radius=10)
        pygame.draw.rect(pantalla, NES_WHITE, self.boton_fullscreen_rect, 2, border_radius=10)

        texto_fs = self.font.render("Pantalla completa:", True, self.texto_color)
        estado_fs = self.font.render("ON" if self.fullscreen else "OFF", True, NES_GREEN if self.fullscreen else NES_RED)
        pantalla.blit(texto_fs, (self.boton_fullscreen_rect.x + 20, self.boton_fullscreen_rect.y + 12))
        pantalla.blit(estado_fs, (self.boton_fullscreen_rect.right - estado_fs.get_width() - 20, self.boton_fullscreen_rect.y + 12))

        # --- Volumen ---
        vol_label = self.font.render(f"Volumen: {int(self.volumen * 100)}%", True, self.texto_color)
        pantalla.blit(vol_label, (WIDTH // 2 - vol_label.get_width() // 2, self.y_vol))

        # Botón -
        pygame.draw.rect(pantalla, self.boton_color_hover if self.boton_volumen_menos_rect.collidepoint(mouse_pos) else self.boton_color_normal,
                        self.boton_volumen_menos_rect, border_radius=8)
        pygame.draw.rect(pantalla, NES_WHITE, self.boton_volumen_menos_rect, 2, border_radius=8)
        pantalla.blit(self.font.render("-", True, self.texto_color), (self.boton_volumen_menos_rect.x + 15, self.boton_volumen_menos_rect.y + 5))

        # Botón +
        pygame.draw.rect(pantalla, self.boton_color_hover if self.boton_volumen_mas_rect.collidepoint(mouse_pos) else self.boton_color_normal,
                        self.boton_volumen_mas_rect, border_radius=8)
        pygame.draw.rect(pantalla, NES_WHITE, self.boton_volumen_mas_rect, 2, border_radius=8)
        pantalla.blit(self.font.render("+", True, self.texto_color), (self.boton_volumen_mas_rect.x + 15, self.boton_volumen_mas_rect.y + 5))

        # Barra de volumen
        pygame.draw.rect(pantalla, NES_GRAY_DARK, (self.barra_x, self.barra_y, self.barra_ancho, self.barra_alto), border_radius=5)
        volumen_progreso = int(self.barra_ancho * self.volumen)
        pygame.draw.rect(pantalla, NES_GREEN, (self.barra_x, self.barra_y, volumen_progreso, self.barra_alto), border_radius=5)

        # --- Volver ---
        pygame.draw.rect(pantalla, self.boton_color_hover if self.boton_volver_rect.collidepoint(mouse_pos) else self.boton_color_normal,
                        self.boton_volver_rect, border_radius=10)
        pygame.draw.rect(pantalla, NES_WHITE, self.boton_volver_rect, 2, border_radius=10)
        volver_label = self.font.render("Volver", True, NES_WHITE)
        volver_rect = volver_label.get_rect(center=self.boton_volver_rect.center)
        pantalla.blit(volver_label, volver_rect)