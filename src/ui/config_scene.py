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

        # Estado actual
        self.fullscreen = FULLSCREEN
        self.volumen = 0.5

        # Controles - Centrados y con más espacio
        self.boton_ancho = 300
        self.boton_alto = 60
        self.espacio_vertical = 80
        self.x_boton = WIDTH // 2 - self.boton_ancho // 2
        self.y_inicial = 180

        self.boton_fullscreen_rect = pygame.Rect(self.x_boton, self.y_inicial, self.boton_ancho, self.boton_alto)
        self.boton_volumen_mas_rect = pygame.Rect(self.x_boton + self.boton_ancho - 60, self.y_inicial + self.espacio_vertical, 50, 50)
        self.boton_volumen_menos_rect = pygame.Rect(self.x_boton, self.y_inicial + self.espacio_vertical, 50, 50)
        self.boton_volver_rect = pygame.Rect(self.x_boton, self.y_inicial + 2 * self.espacio_vertical, self.boton_ancho, self.boton_alto)

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
        pantalla.blit(self.titulo, (WIDTH // 2 - self.titulo.get_width() // 2, 80)) # Centrar título

        # Botón Pantalla Completa
        color_fs = self.boton_color_normal
        if self.boton_fullscreen_rect.collidepoint(pygame.mouse.get_pos()):
            color_fs = self.boton_color_hover
            pygame.draw.rect(pantalla, NES_WHITE, self.boton_fullscreen_rect, 3)
        pygame.draw.rect(pantalla, color_fs, self.boton_fullscreen_rect, border_radius=8)
        texto_fs = self.font.render("Pantalla completa:", True, self.texto_color)
        estado_fs = self.font.render("ON" if self.fullscreen else "OFF", True, self.accent_color)
        pantalla.blit(texto_fs, (self.boton_fullscreen_rect.x + 20, self.boton_fullscreen_rect.y + 15))
        pantalla.blit(estado_fs, (self.boton_fullscreen_rect.right - estado_fs.get_width() - 20, self.boton_fullscreen_rect.y + 15))

        # Control de Volumen
        vol_label = self.font.render("Volumen:", True, self.texto_color)
        vol_value = self.font.render(f"{int(self.volumen * 100)}%", True, self.accent_color)
        pantalla.blit(vol_label, (self.x_boton + 20, self.boton_volumen_menos_rect.y + 10))
        pantalla.blit(vol_value, (self.boton_volumen_mas_rect.x + 60, self.boton_volumen_menos_rect.y + 10))

        # Botón Menos Volumen
        color_menos = self.boton_color_normal
        if self.boton_volumen_menos_rect.collidepoint(pygame.mouse.get_pos()):
            color_menos = self.boton_color_hover
            pygame.draw.rect(pantalla, NES_WHITE, self.boton_volumen_menos_rect, 3)
        pygame.draw.rect(pantalla, color_menos, self.boton_volumen_menos_rect, border_radius=8)
        pantalla.blit(self.font.render("-", True, self.texto_color), (self.boton_volumen_menos_rect.x + 15, self.boton_volumen_menos_rect.y + 10))

        # Botón Más Volumen
        color_mas = self.boton_color_normal
        if self.boton_volumen_mas_rect.collidepoint(pygame.mouse.get_pos()):
            color_mas = self.boton_color_hover
            pygame.draw.rect(pantalla, NES_WHITE, self.boton_volumen_mas_rect, 3)
        pygame.draw.rect(pantalla, color_mas, self.boton_volumen_mas_rect, border_radius=8)
        pantalla.blit(self.font.render("+", True, self.texto_color), (self.boton_volumen_mas_rect.x + 15, self.boton_volumen_mas_rect.y + 10))

        # Botón Volver
        color_volver = self.boton_color_normal
        if self.boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
            color_volver = self.boton_color_hover
            pygame.draw.rect(pantalla, NES_WHITE, self.boton_volver_rect, 3)
        pygame.draw.rect(pantalla, color_volver, self.boton_volver_rect, border_radius=8)
        volver_label = self.font.render("Volver", True, self.texto_color)
        volver_rect = volver_label.get_rect(center=self.boton_volver_rect.center)
        pantalla.blit(volver_label, volver_rect)