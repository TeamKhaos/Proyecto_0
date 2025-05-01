import pygame
from ui.pantalla_principal import PantallaPrincipalScene
from assets.colors import * # Asegúrate de tener la paleta NES definida aquí

class NombreJugadorScene:
    def __init__(self):
        # Carga la fuente personalizada desde assets/fonts
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 48)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 60)

        self.input_text = ""
        self.boton_rect = pygame.Rect(0, 0, 200, 50)  # Botón para confirmar
        self.boton_color = NES_RED  # Color del botón (Rojo NES)

        # Calcular las posiciones centradas
        self.ancho_pantalla = 800  # Suponiendo que el tamaño de la ventana es 600x400
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        self.centro_y = self.alto_pantalla // 2

    def manejar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.input_text:
                    from engine.scene_manager import SceneManager
                    SceneManager.cambiar_escena(PantallaPrincipalScene(self.input_text))
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        # Fondo oscuro clásico
        pantalla.fill(NES_BLACK)

        # Título en un color brillante
        titulo = self.titulo_font.render("Bienvenido al Juego!", True, NES_YELLOW)
        titulo_rect = titulo.get_rect(center=(self.centro_x, 80))
        pantalla.blit(titulo, titulo_rect)

        # Texto de entrada en blanco o un gris claro
        texto = self.font.render("Ingresa tu nombre:", True, NES_WHITE)
        texto_rect = texto.get_rect(center=(self.centro_x, self.centro_y - 40))
        pantalla.blit(texto, texto_rect)

        # Campo de texto (cuadro de entrada) con borde y texto en otro color
        pygame.draw.rect(pantalla, NES_GRAY_LIGHT, pygame.Rect(self.centro_x - 200, self.centro_y, 400, 50), 2) # Borde gris claro
        entrada = self.font.render(self.input_text, True, NES_GREEN) # Texto en verde NES
        entrada_rect = entrada.get_rect(center=(self.centro_x, self.centro_y + 25))
        pantalla.blit(entrada, entrada_rect)

        # Botón de confirmar en un color llamativo
        self.boton_rect.center = (self.centro_x, self.centro_y + 100)
        pygame.draw.rect(pantalla, self.boton_color, self.boton_rect)
        boton_texto = self.font.render("Confirmar", True, NES_BLUE) # Texto del botón en azul NES
        boton_texto_rect = boton_texto.get_rect(center=self.boton_rect.center)
        pantalla.blit(boton_texto, boton_texto_rect)

        # Efecto al pasar el mouse sobre el botón (un tono más claro del color del botón)
        if self.boton_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, (255, 100, 100), self.boton_rect, 5) # Resalta el borde en un rojo ligeramente más claro