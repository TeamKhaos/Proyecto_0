import pygame
import random
from assets.colors import *

class CreditsScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.fuente_titulo = pygame.font.Font("assets/fonts/upheavtt.ttf", 50)
        self.fuente_texto = pygame.font.Font("assets/fonts/upheavtt.ttf", 30)
        self.fuente_pquena = pygame.font.Font("assets/fonts/upheavtt.ttf", 20)
        
        self.ancho = 800
        self.alto = 600
        self.scroll_y = self.alto
        
        self.creditos = [
            ("¡MISIÓN CUMPLIDA!", self.fuente_titulo, NES_YELLOW),
            ("", self.fuente_texto, NES_WHITE),
            (f"PILOTO: {self.nombre.upper()}", self.fuente_texto, NES_GREEN),
            ("", self.fuente_texto, NES_WHITE),
            ("DISEÑO Y PROGRAMACIÓN", self.fuente_pquena, NES_LIGHT_BLUE),
            ("GEMINI CLI AGENT", self.fuente_texto, NES_WHITE),
            ("", self.fuente_texto, NES_WHITE),
            ("ARTE RETRO", self.fuente_pquena, NES_LIGHT_BLUE),
            ("ESTILO NES 8-BIT", self.fuente_texto, NES_WHITE),
            ("", self.fuente_texto, NES_WHITE),
            ("MÚSICA Y SONIDO", self.fuente_pquena, NES_LIGHT_BLUE),
            ("RETRO SOUND PACK", self.fuente_texto, NES_WHITE),
            ("", self.fuente_texto, NES_WHITE),
            ("TECNOLOGÍA", self.fuente_pquena, NES_LIGHT_BLUE),
            ("PYGAME CE", self.fuente_texto, NES_WHITE),
            ("", self.fuente_texto, NES_WHITE),
            ("", self.fuente_texto, NES_WHITE),
            ("¡GRACIAS POR JUGAR!", self.fuente_titulo, NES_ORANGE),
        ]
        
        # Estrellas de fondo
        self.estrellas = [[random.randint(0, self.ancho), random.randint(0, self.alto), random.uniform(0.5, 2)] for _ in range(100)]

    def manejar_eventos(self, eventos, pantalla):
        from engine.scene_manager import SceneManager
        from ui.pantalla_principal import PantallaPrincipalScene
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                if self.scroll_y < 0: # Solo permite salir cuando los créditos ya subieron un poco
                    SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre))

    def actualizar(self):
        self.scroll_y -= 1 # Velocidad del scroll
        
        # Mover estrellas
        for e in self.estrellas:
            e[1] += e[2]
            if e[1] > self.alto: e[1] = 0

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)
        
        # Dibujar estrellas
        for e in self.estrellas:
            pygame.draw.circle(pantalla, NES_WHITE, (int(e[0]), int(e[1])), 1)
            
        # Dibujar créditos
        y_offset = 0
        for texto, fuente, color in self.creditos:
            if texto != "":
                img = fuente.render(texto, True, color)
                rect = img.get_rect(center=(self.ancho // 2, self.scroll_y + y_offset))
                if -50 < rect.y < 650: # Optimización: solo dibujar si está en pantalla
                    pantalla.blit(img, rect)
            y_offset += 50

        # Instrucción para salir
        if self.scroll_y < - (len(self.creditos) * 50):
            msg = self.fuente_pquena.render("PRESIONA CUALQUIER TECLA PARA VOLVER", True, NES_GRAY)
            pantalla.blit(msg, msg.get_rect(center=(self.ancho // 2, 550)))
