import pygame
import random
from ui.config_scene import ConfigScene
from scenes.select_level import SelectLevelScene
from assets.colors import *

class Estrella:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.x = random.randint(0, ancho_pantalla)
        self.y = random.randint(0, alto_pantalla)
        self.velocidad = random.uniform(0.2, 1.0)
        self.tamano = random.randint(1, 2)
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla

    def mover(self):
        self.y += self.velocidad
        if self.y > self.alto_pantalla:
            self.y = 0
            self.x = random.randint(0, self.ancho_pantalla)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, NES_WHITE, (int(self.x), int(self.y)), self.tamano)

class PantallaPrincipalScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 72)

        # COOLDOWN: Tiempo de seguridad al entrar (para evitar clics fantasma)
        self.tiempo_entrada = pygame.time.get_ticks()
        self.duracion_bloqueo = 200 # 1 segundo de seguridad

        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2

        # Crear estrellas para el fondo
        self.estrellas = [Estrella(self.ancho_pantalla, self.alto_pantalla) for _ in range(100)]

        self.boton_ancho = 320
        self.boton_alto = 60
        self.espacio_entre_botones = 30

        self.botones = {
            "iniciar": pygame.Rect(0, 0, self.boton_ancho, self.boton_alto),
            "tutorial": pygame.Rect(0, 0, self.boton_ancho, self.boton_alto),
            "configuración": pygame.Rect(0, 0, self.boton_ancho, self.boton_alto),
            "salir": pygame.Rect(0, 0, self.boton_ancho, self.boton_alto),
        }
        
        # Botón de Tamaño de Pantalla (Esquina Superior Derecha)
        self.btn_resize = pygame.Rect(740, 10, 50, 50)

        self._posicionar_botones()

    def _posicionar_botones(self):
        # ... (código anterior)
        total_altura = len(self.botones) * self.boton_alto + (len(self.botones) - 1) * self.espacio_entre_botones
        inicio_y = (self.alto_pantalla // 2 + 50) - total_altura // 2

        for i, rect in enumerate(self.botones.values()):
            rect.center = (self.centro_x, inicio_y + i * (self.boton_alto + self.espacio_entre_botones))

    def manejar_eventos(self, eventos, pantalla=None):
        # Comprobar si estamos en periodo de bloqueo
        if pygame.time.get_ticks() - self.tiempo_entrada < self.duracion_bloqueo:
            # Consumir eventos de salida para que no se cierren pero ignorar los clics
            for event in eventos:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            return

        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                from engine.scene_manager import SceneManager
                from engine.audio_manager import AudioManager
                
                # Clic en el botón de redimensionar (esquina)
                if self.btn_resize.collidepoint(event.pos):
                    AudioManager.play_boton()
                    import settings
                    settings.toggle_fullscreen()
                    return

                if self.botones["iniciar"].collidepoint(event.pos):
                    AudioManager.play_boton()
                    SceneManager.cambiar_escena(SelectLevelScene(self.nombre))
                elif self.botones["tutorial"].collidepoint(event.pos):
                    AudioManager.play_boton()
                    from ui.tutorial_scene import TutorialScene
                    SceneManager.cambiar_escena(TutorialScene(self.nombre))
                elif self.botones["configuración"].collidepoint(event.pos):
                    AudioManager.play_boton()
                    SceneManager.cambiar_escena(ConfigScene(self.nombre))
                elif self.botones["salir"].collidepoint(event.pos):
                    AudioManager.play_boton()
                    pygame.time.delay(200) # Pequeño delay para que se escuche antes de cerrar
                    pygame.quit()
                    exit()

    def actualizar(self):
        # ... (estrellas)
        for estrella in self.estrellas:
            estrella.mover()

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)
        
        for estrella in self.estrellas:
            estrella.dibujar(pantalla)

        # Botón Resize (Dibujo)
        mouse_pos = pygame.mouse.get_pos()
        color_res = NES_BLUE if not self.btn_resize.collidepoint(mouse_pos) else NES_LIGHT_BLUE
        pygame.draw.rect(pantalla, color_res, self.btn_resize, border_radius=5)
        pygame.draw.rect(pantalla, NES_WHITE, self.btn_resize, 2, border_radius=5)
        # Dibujar un pequeño ícono de "expandir"
        pygame.draw.rect(pantalla, NES_WHITE, (750, 20, 30, 30), 2)
        pygame.draw.line(pantalla, NES_WHITE, (750, 20), (780, 50), 2)

        # Título y demás...
        titulo = self.titulo_font.render("Star Rogue", True, NES_YELLOW)
        pantalla.blit(titulo, titulo.get_rect(center=(self.centro_x, 100)))

        # Saludo
        saludo = self.font.render(f"¡Hola, {self.nombre}!", True, NES_LIGHT_GREEN)
        pantalla.blit(saludo, saludo.get_rect(center=(self.centro_x, 180)))

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for texto, rect in self.botones.items():
            esta_sobre = rect.collidepoint(mouse_pos)
            color_boton = NES_BLUE if not esta_sobre else NES_LIGHT_BLUE

            pygame.draw.rect(pantalla, color_boton, rect, border_radius=10)
            if esta_sobre:
                pygame.draw.rect(pantalla, NES_WHITE, rect, width=3, border_radius=10)

            label = self.font.render(texto.capitalize(), True, NES_WHITE)
            pantalla.blit(label, label.get_rect(center=rect.center))