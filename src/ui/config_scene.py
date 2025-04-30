import pygame
from settings import WIDTH, HEIGHT, FULLSCREEN
from engine.scene_manager import SceneManager

class ConfigScene:
    def __init__(self, nombre):  # ← constructor corregido
        self.nombre = nombre
        self.font = pygame.font.SysFont(None, 40)
        self.titulo = pygame.font.SysFont(None, 60).render("Configuración", True, (255, 255, 255))

        # Estado actual
        self.fullscreen = FULLSCREEN
        self.volumen = 0.5

        # Controles
        self.boton_fullscreen = pygame.Rect(100, 150, 300, 50)
        self.boton_volumen_mas = pygame.Rect(100, 230, 50, 50)
        self.boton_volumen_menos = pygame.Rect(160, 230, 50, 50)
        self.boton_volver = pygame.Rect(100, 320, 200, 50)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_fullscreen.collidepoint(evento.pos):
                    self.fullscreen = not self.fullscreen
                    flags = pygame.FULLSCREEN if self.fullscreen else 0
                    pygame.display.set_mode((WIDTH, HEIGHT), flags)
                elif self.boton_volumen_mas.collidepoint(evento.pos):
                    self.volumen = min(1.0, self.volumen + 0.1)
                    pygame.mixer.music.set_volume(self.volumen)
                elif self.boton_volumen_menos.collidepoint(evento.pos):
                    self.volumen = max(0.0, self.volumen - 0.1)
                    pygame.mixer.music.set_volume(self.volumen)
                elif self.boton_volver.collidepoint(evento.pos):
                    from ui.main_menu import PantallaPrincipalScene
                    SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill((20, 20, 20))
        pantalla.blit(self.titulo, (100, 50))

        texto_fs = "Pantalla completa: ON" if self.fullscreen else "Pantalla completa: OFF"
        texto_vol = f"Volumen: {int(self.volumen * 100)}%"

        fs_label = self.font.render(texto_fs, True, (255, 255, 255))
        vol_label = self.font.render(texto_vol, True, (255, 255, 255))
        volver_label = self.font.render("Volver", True, (255, 255, 255))

        pygame.draw.rect(pantalla, (50, 100, 200), self.boton_fullscreen)
        pantalla.blit(fs_label, (self.boton_fullscreen.x + 10, self.boton_fullscreen.y + 10))

        pygame.draw.rect(pantalla, (100, 100, 100), self.boton_volumen_mas)
        pantalla.blit(self.font.render("+", True, (255, 255, 255)), (self.boton_volumen_mas.x + 15, self.boton_volumen_mas.y + 10))

        pygame.draw.rect(pantalla, (100, 100, 100), self.boton_volumen_menos)
        pantalla.blit(self.font.render("-", True, (255, 255, 255)), (self.boton_volumen_menos.x + 15, self.boton_volumen_menos.y + 10))

        pantalla.blit(vol_label, (230, 240))

        pygame.draw.rect(pantalla, (100, 50, 50), self.boton_volver)
        pantalla.blit(volver_label, (self.boton_volver.x + 10, self.boton_volver.y + 10))
