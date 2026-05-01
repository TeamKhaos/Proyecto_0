# src/scenes/select_level.py
import pygame
import random
from assets.colors import *
from scenes.level_1 import NivelUnoScene
from scenes.level_2 import NivelDosScene
from scenes.level_3 import NivelTresScene
from engine.progreso_manager import cargar_progreso

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

class Boton:
    def __init__(self, texto, x, y, ancho, alto, bloqueado=False):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.bloqueado = bloqueado
        self.color_normal = NES_BLUE if not bloqueado else NES_GRAY
        self.color_hover = NES_LIGHT_BLUE if not bloqueado else NES_GRAY
        self.color_texto = NES_WHITE if not bloqueado else NES_BLACK
        self.borde_color = NES_BLUE if not bloqueado else NES_GRAY_DARK
        self.borde_ancho = 4

    def dibujar(self, pantalla, fuente, mouse_pos):
        hover = self.rect.collidepoint(mouse_pos) and not self.bloqueado
        color_borde = self.color_hover if hover else self.borde_color

        pygame.draw.rect(pantalla, self.color_normal, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, color_borde, self.rect, self.borde_ancho, border_radius=10)

        txt = self.texto if not self.bloqueado else f"LOCKED"
        texto_render = fuente.render(txt, True, self.color_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def esta_presionado(self, evento):
        return evento.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(evento.pos) and not self.bloqueado

class Estrella:
    def __init__(self):
        self.x = random.randint(0, ANCHO_PANTALLA)
        self.y = random.randint(0, ALTO_PANTALLA)
        self.velocidad = random.uniform(0.2, 1.0)
        self.tamano = random.randint(1, 2)

    def mover(self):
        self.y += self.velocidad
        if self.y > ALTO_PANTALLA:
            self.y = 0
            self.x = random.randint(0, ANCHO_PANTALLA)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, NES_WHITE, (int(self.x), int(self.y)), self.tamano)

class SelectLevelScene:
    def __init__(self, nombre):
        self.nombre_jugador = nombre
        self.fuente = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
        
        # Cargar progreso para saber qué niveles desbloquear
        progreso = cargar_progreso()

        self.botones = [
            Boton("Tutorial", 300, 180, 200, 60), # Añadido arriba
            Boton("Nivel 1", 300, 255, 200, 60),
            Boton("Nivel 2", 300, 330, 200, 60, bloqueado=not progreso["nivel_2_desbloqueado"]),
            Boton("Nivel 3", 300, 405, 200, 60, bloqueado=not progreso["nivel_3_desbloqueado"]),
            Boton("Volver", 300, 480, 200, 60)
        ]

        self.estrellas = [Estrella() for _ in range(50)]

    def manejar_eventos(self, eventos, pantalla):
        from engine.scene_manager import SceneManager
        from ui.pantalla_principal import PantallaPrincipalScene
        from engine.audio_manager import AudioManager

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            for boton in self.botones:
                if boton.esta_presionado(evento):
                    AudioManager.play_boton()
                    if boton.texto == "Volver":
                        SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre_jugador))
                    elif boton.texto == "Tutorial":
                        from ui.tutorial_scene import InteractiveTutorialScene
                        SceneManager.cambiar_escena(InteractiveTutorialScene(self.nombre_jugador))
                    elif boton.texto == "Nivel 1":
                        SceneManager.cambiar_escena(NivelUnoScene(self.nombre_jugador))
                    elif boton.texto == "Nivel 2" and not boton.bloqueado:
                        SceneManager.cambiar_escena(NivelDosScene(self.nombre_jugador))
                    elif boton.texto == "Nivel 3" and not boton.bloqueado:
                        SceneManager.cambiar_escena(NivelTresScene(self.nombre_jugador))

    def actualizar(self):
        for estrella in self.estrellas:
            estrella.mover()

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)
        mouse_pos = pygame.mouse.get_pos()

        for estrella in self.estrellas:
            estrella.dibujar(pantalla)

        # Título
        titulo = self.fuente.render("SELECCION DE NIVEL", True, NES_YELLOW)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO_PANTALLA//2, 100)))

        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente, mouse_pos)
