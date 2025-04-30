import pygame
from ui.pantalla_principal import PantallaPrincipalScene

class NombreJugadorScene:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 48)
        self.input_text = ""

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
        pantalla.fill((0, 0, 0))
        texto = self.font.render("Ingresa tu nombre:", True, (255, 255, 255))
        entrada = self.font.render(self.input_text, True, (0, 255, 0))
        pantalla.blit(texto, (100, 100))
        pantalla.blit(entrada, (100, 160))
