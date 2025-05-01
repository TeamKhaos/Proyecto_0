import pygame
from engine.scene_manager import SceneManager
from ui.main_menu import NombreJugadorScene
from assets.colors import *

class SplashScene:
    def __init__(self):
        self.logo = pygame.image.load("assets/images/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (300, 300))
        self.alpha = 0
        self.logo.set_alpha(self.alpha)

        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 3000  # 3 segundos

        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 24)
        self.texto = self.font.render("Powered by PYGAME", True, NES_GREEN)
        
        # Sonido breve al iniciar
        #self.sonido_intro = pygame.mixer.Sound("assets/sounds/intro.wav")
        #self.sonido_intro.play()

    def manejar_eventos(self, eventos, patanalla = None):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                from engine.scene_manager import SceneManager
                SceneManager.cambiar_escena(NombreJugadorScene())


    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        transcurrido = tiempo_actual - self.tiempo_inicio

        if transcurrido < 1000:
            self.alpha = min(255, int(transcurrido / 1000 * 255))  # Fade in en 1s
            self.logo.set_alpha(self.alpha)
        elif transcurrido > self.duracion:
            SceneManager.cambiar_escena(NombreJugadorScene())

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)  # Fondo negro clásico

        centro_x = pantalla.get_width() // 2
        centro_y = pantalla.get_height() // 2

        # Dibujar logo centrado
        logo_rect = self.logo.get_rect(center=(centro_x, centro_y - 50))
        pantalla.blit(self.logo, logo_rect)

        # Dibujar texto debajo
        texto_rect = self.texto.get_rect(center=(centro_x, centro_y + 130))
        pantalla.blit(self.texto, texto_rect)