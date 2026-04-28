import pygame
from ui.pantalla_principal import PantallaPrincipalScene
from assets.colors import *

class NombreJugadorScene:
        def __init__(self):
            self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
            self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 64)

            self.input_text = ""
            self.boton_rect = pygame.Rect(0, 0, 240, 60)
            self.boton_color = NES_GREEN

            self.ancho_pantalla = 800
            self.alto_pantalla = 600
            self.centro_x = self.ancho_pantalla // 2
            self.centro_y = self.alto_pantalla // 2

            self.nombre_jugador = ""  # Variable para guardar el nombre

        def manejar_eventos(self, eventos, pantalla):
            for event in eventos:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        from engine.audio_manager import AudioManager
                        AudioManager.play_boton()
                    
                    if event.key == pygame.K_RETURN and self.input_text.strip():
                        # Pasar pantalla como parámetro
                        self.nombre_jugador = self.input_text.strip()
                        self.transicion_fundido(pantalla)
                        from engine.scene_manager import SceneManager
                        SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre_jugador))
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 20:
                            self.input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic izquierdo
                        pass # El sonido se activará al soltar (UP)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.boton_rect.collidepoint(event.pos) and self.input_text.strip():
                            from engine.audio_manager import AudioManager
                            AudioManager.play_boton()
                            # Pasar pantalla como parámetro
                            self.transicion_fundido(pantalla)
                            from engine.scene_manager import SceneManager
                            SceneManager.cambiar_escena(PantallaPrincipalScene(self.input_text.strip()))

        def actualizar(self):
            pass

        def dibujar(self, pantalla):
            pantalla.fill(NES_BLACK)

            # ------------------ TÍTULO ------------------
            titulo = self.titulo_font.render("¡Piloto, Identifícate!", True, NES_GREEN)
            titulo_rect = titulo.get_rect(center=(self.centro_x, 100))
            pantalla.blit(titulo, titulo_rect)

            # ------------------ SUBTÍTULO ------------------
            subtitulo = self.font.render("Ingresa tu nombre:", True, NES_GREEN)
            subtitulo_rect = subtitulo.get_rect(center=(self.centro_x, self.centro_y - 60))
            pantalla.blit(subtitulo, subtitulo_rect)

            # ------------------ CAMPO DE TEXTO ------------------
            input_box = pygame.Rect(self.centro_x - 200, self.centro_y - 10, 400, 50)
            pygame.draw.rect(pantalla, NES_GREEN, input_box, 3, border_radius=10)

            entrada = self.font.render(self.input_text, True, NES_GREEN)
            entrada_rect = entrada.get_rect(midleft=(input_box.x + 10, input_box.centery))
            pantalla.blit(entrada, entrada_rect)

            # ------------------ BOTÓN ------------------
            self.boton_rect.center = (self.centro_x, self.centro_y + 80)
            mouse_pos = pygame.mouse.get_pos()

            # Hover
            color_borde = NES_ORANGE if self.boton_rect.collidepoint(mouse_pos) else NES_GREEN
            pygame.draw.rect(pantalla, self.boton_color, self.boton_rect, border_radius=10)
            pygame.draw.rect(pantalla, color_borde, self.boton_rect, 4, border_radius=10)

            boton_texto = self.font.render("Confirmar", True, NES_WHITE)
            boton_texto_rect = boton_texto.get_rect(center=self.boton_rect.center)
            pantalla.blit(boton_texto, boton_texto_rect)

        def transicion_fundido(self, pantalla):
            width, height = pantalla.get_size()
            fade = pygame.Surface((width, height))
            fade.fill((0, 0, 0))

            for alpha in range(0, 255, 10):
                fade.set_alpha(alpha)
                self.dibujar(pantalla)  # Usar el parámetro pantalla
                pantalla.blit(fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(30)