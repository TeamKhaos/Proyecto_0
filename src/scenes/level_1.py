import pygame
from assets.colors import *  # Asegúrate de tener los colores definidos en este archivo
from enemies.enemy_manager import EnemyManager
from enemies.boss import Boss
class Nave:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else 400
        self.y = y if y is not None else 500
        self.velocidad = 5
        self.ancho = 40
        self.alto = 30


    def mover(self, teclas):
        if teclas[pygame.K_w]:  # Arriba
            self.y -= self.velocidad
        if teclas[pygame.K_s]:  # Abajo
            self.y += self.velocidad
        if teclas[pygame.K_a]:  # Izquierda
            self.x -= self.velocidad
        if teclas[pygame.K_d]:  # Derecha
            self.x += self.velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, NES_GREEN, (self.x, self.y, self.ancho, self.alto))
# esto es para la colision de la nave y si no vale puedo borrarlo
    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)


class NivelUnoScene:
    def __init__(self, nombre_jugador):
        pygame.mixer.music.load("assets/music/music_background.mp3")
        self.pausa_1 = pygame.mixer.Sound("assets/sounds/pause_1.wav")
        self.pausa_2 = pygame.mixer.Sound("assets/sounds/pause_2.wav")
        self.reproducido_pausa = False  # Controla si ya se reprodujo el sonido
        self.nombre = nombre_jugador
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 64)

        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        self.centro_y = self.alto_pantalla // 2

        self.nave = Nave()
        self.pausa = False

        self.boton_rect = pygame.Rect(0, 0, 240, 60)
        self.boton_color = NES_BLUE

        self.enemy_manager = EnemyManager()
        self.boss = Boss()
        self.contador_frames = 0  

    def manejar_eventos(self, eventos, pantalla):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pausa = True
                if self.pausa:
                    if event.key == pygame.K_RETURN:  # Si presionamos Enter para volver
                        self.pausa = False  # Desactivar pausa
                if not self.pausa:
                    if event.key == pygame.K_w:  # Arriba
                        self.nave.y -= 25
                    elif event.key == pygame.K_s:  # Abajo
                        self.nave.y += 25
                    elif event.key == pygame.K_a:  # Izquierda
                        self.nave.x -= 25
                    elif event.key == pygame.K_d:  # Derecha
                        self.nave.x += 25

    def actualizar(self):
        if not self.pausa:
            teclas = pygame.key.get_pressed()
            self.nave.mover(teclas)

            self.contador_frames += 1
            self.enemy_manager.actualizar()

            if self.contador_frames == 1200:
                self.boss.aparecer()

            self.boss.mover()

        pass

    def dibujar(self, pantalla):
        if self.pausa:
            self.mostrar_menu_pausa(pantalla)
        else:
            pantalla.fill(NES_BLACK)

            # ------------------ TÍTULO ------------------
            titulo = self.titulo_font.render("Nivel 1", True, NES_GREEN)
            titulo_rect = titulo.get_rect(center=(self.centro_x, 100))
            pantalla.blit(titulo, titulo_rect)

            # ------------------ NAVE ------------------
            self.nave.dibujar(pantalla)
            # enemigos
            self.enemy_manager.dibujar(pantalla)
            self.boss.dibujar(pantalla)

    
    def dibujar_fondo_congelado(self, pantalla):
        pantalla.fill(NES_BLACK)
        titulo = self.titulo_font.render("Nivel 1", True, NES_GREEN)
        pantalla.blit(titulo, titulo.get_rect(center=(self.centro_x, 100)))
        self.nave.dibujar(pantalla)

    def mostrar_menu_pausa(self, pantalla):
        # Dibujar fondo del juego (congelado) antes de superponer el menú
        self.dibujar_fondo_congelado(pantalla)

        # Capa transparente para menú de pausa
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Negro con transparencia
        pantalla.blit(overlay, (0, 0))

        # Texto de "PAUSA"
        pausa_texto = self.font.render("PAUSA", True, NES_RED)
        pausa_rect = pausa_texto.get_rect(center=(self.centro_x, self.centro_y - 100))
        pantalla.blit(pausa_texto, pausa_rect)
        # -- sonido de pausa --
        if not self.reproducido_pausa:
            self.pausa_1.play()
            self.reproducido_pausa = True

        # --- Botón "Jugar" ---
        jugar_rect = pygame.Rect(0, 0, 240, 60)
        jugar_rect.center = (self.centro_x, self.centro_y - 20)
        mouse_pos = pygame.mouse.get_pos()
        color_borde_jugar = NES_ORANGE if jugar_rect.collidepoint(mouse_pos) else NES_GREEN

        pygame.draw.rect(pantalla, self.boton_color, jugar_rect, border_radius=10)
        pygame.draw.rect(pantalla, color_borde_jugar, jugar_rect, 4, border_radius=10)
        texto_jugar = self.font.render("Jugar", True, NES_WHITE)
        pantalla.blit(texto_jugar, texto_jugar.get_rect(center=jugar_rect.center))

        # --- Botón "Volver" ---
        self.boton_rect.center = (self.centro_x, self.centro_y + 60)
        color_borde_volver = NES_ORANGE if self.boton_rect.collidepoint(mouse_pos) else NES_GREEN

        pygame.draw.rect(pantalla, self.boton_color, self.boton_rect, border_radius=10)
        pygame.draw.rect(pantalla, color_borde_volver, self.boton_rect, 4, border_radius=10)
        texto_volver = self.font.render("Volver", True, NES_WHITE)
        pantalla.blit(texto_volver, texto_volver.get_rect(center=self.boton_rect.center))

        # Eventos del mouse
        if pygame.mouse.get_pressed()[0]:  # Click izquierdo
            if jugar_rect.collidepoint(mouse_pos):
                self.pausa_2.play()
                self.pausa = False
                self.reproducido_pausa = False
            elif self.boton_rect.collidepoint(mouse_pos):
                from engine.scene_manager import SceneManager
                from scenes.select_level import SelectLevelScene
                pygame.mixer.music.play(-1)
                SceneManager.cambiar_escena(SelectLevelScene(self.nombre))
