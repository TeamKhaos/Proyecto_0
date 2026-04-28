import pygame
from assets.colors import *

class TutorialScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 30)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 64)
        
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        
        # Botón Volver
        self.boton_volver = pygame.Rect(0, 0, 240, 60)
        self.boton_volver.center = (self.centro_x, 520)

        # Definir los controles a mostrar
        self.controles = [
            ("W, A, S, D", "Mover la Nave"),
            ("Tecla J", "Disparar Proyectiles"),
            ("Tecla ESC", "Pausar el Juego"),
            ("Mouse", "Interactuar con Menús")
        ]

    def manejar_eventos(self, eventos, pantalla=None):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.boton_volver.collidepoint(event.pos):
                    from engine.audio_manager import AudioManager
                    AudioManager.play_boton()
                    from engine.scene_manager import SceneManager
                    from ui.pantalla_principal import PantallaPrincipalScene
                    SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)
        
        # Título
        titulo = self.titulo_font.render("CONTROLES", True, NES_YELLOW)
        pantalla.blit(titulo, titulo.get_rect(center=(self.centro_x, 80)))

        # Dibujar lista de controles
        inicio_y = 180
        for i, (tecla, accion) in enumerate(self.controles):
            # Texto de la tecla
            txt_tecla = self.font.render(tecla, True, NES_GREEN)
            pantalla.blit(txt_tecla, (self.centro_x - 300, inicio_y + i * 70))
            
            # Línea decorativa
            pygame.draw.line(pantalla, NES_WHITE, (self.centro_x - 310, inicio_y + i * 70 + 35), (self.centro_x + 310, inicio_y + i * 70 + 35), 1)
            
            # Texto de la acción
            txt_accion = self.font.render(accion, True, NES_WHITE)
            pantalla.blit(txt_accion, (self.centro_x + 20, inicio_y + i * 70))

        # Dibujar botón volver
        mouse_pos = pygame.mouse.get_pos()
        esta_sobre = self.boton_volver.collidepoint(mouse_pos)
        color_boton = NES_BLUE if not esta_sobre else NES_LIGHT_BLUE
        
        pygame.draw.rect(pantalla, color_boton, self.boton_volver, border_radius=10)
        if esta_sobre:
            pygame.draw.rect(pantalla, NES_WHITE, self.boton_volver, width=3, border_radius=10)
            
        label = self.font.render("VOLVER", True, NES_WHITE)
        pantalla.blit(label, label.get_rect(center=self.boton_volver.center))
