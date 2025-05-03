# src/scenes/select_level.py
import pygame
import random
from assets.colors import *
from scenes.level_1 import NivelUnoScene
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

class Boton:
    def __init__(self, texto, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = NES_BLUE
        self.color_hover = NES_LIGHT_BLUE
        self.color_texto = NES_WHITE
        self.borde_color = NES_BLUE
        self.borde_ancho = 4

    def dibujar(self, pantalla, fuente, mouse_pos):
        hover = self.rect.collidepoint(mouse_pos)
        color_borde = self.color_hover if hover else self.borde_color

        pygame.draw.rect(pantalla, self.color_normal, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, color_borde, self.rect, self.borde_ancho, border_radius=10)

        texto_render = fuente.render(self.texto, True, self.color_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def esta_presionado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)

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

class Nave:
    def __init__(self, x=None, y=None):
        self.direccion = random.choice(["izquierda", "derecha"])
        self.y = y if y else random.randint(50, ALTO_PANTALLA - 100)
        if self.direccion == "izquierda":
            self.x = x if x is not None else ANCHO_PANTALLA
            self.velocidad = -2
        else:
            self.x = x if x is not None else -40
            self.velocidad = 2

    def mover(self):
        self.x += self.velocidad

    def esta_fuera_de_pantalla(self):
        return self.x < -50 or self.x > ANCHO_PANTALLA + 50

    def dibujar(self, pantalla):
        puntos = [(self.x, self.y), (self.x + 20, self.y + 10), (self.x, self.y + 20)]
        pygame.draw.polygon(pantalla, NES_RED, puntos)

class Disparo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = -5
        self.activo = True

    def mover(self):
        self.y += self.velocidad
        if self.y < 0:
            self.activo = False

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, NES_YELLOW, (int(self.x), int(self.y)), 4)

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.explotando = False
        self.contador_explosion = 0

    def dibujar(self, pantalla):
        if self.explotando:
            if self.contador_explosion < 45:
                pygame.draw.circle(pantalla, NES_RED, (int(self.x), int(self.y)), 15)
            elif self.contador_explosion < 90:
                pygame.draw.circle(pantalla, NES_YELLOW, (int(self.x), int(self.y)), 20)
            else:
                return False
            self.contador_explosion += 1
        else:
            pygame.draw.rect(pantalla, NES_GRAY, (self.x - 10, self.y - 10, 20, 20))
        return True

    def impactado_por(self, disparo):
        distancia = ((self.x - disparo.x) ** 2 + (self.y - disparo.y) ** 2) ** 0.5
        return distancia < 20

class SelectLevelScene:
    def __init__(self, nombre):
        self.nombre_jugador = nombre
        self.fuente = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)

        self.botones = [
            Boton("Tutorial", 300, 200, 200, 50),
            Boton("Nivel 1", 300, 270, 200, 50),
            Boton("Nivel 2", 300, 340, 200, 50),
            Boton("Volver", 300, 410, 200, 50)
        ]

        self.estrellas = [Estrella() for _ in range(50)]
        self.naves = []
        self.disparo = None
        self.enemigo = None
        self.nave_atacante = None
        self.tiempo_disparo = pygame.time.get_ticks()
        self.intervalo_disparo = random.randint(5000, 10000)

    def manejar_eventos(self, eventos, pantalla):
        from engine.scene_manager import SceneManager
        from ui.pantalla_principal import PantallaPrincipalScene

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            for boton in self.botones:
                if boton.esta_presionado(evento):
                    if boton.texto == "Volver":
                        SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre_jugador))
                    elif boton.texto == "Nivel 1":
                        SceneManager.cambiar_escena(NivelUnoScene(self.nombre_jugador))
                    else:
                        print(f"Ir a {boton.texto} (implementación pendiente)")

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()

        for estrella in self.estrellas:
            estrella.mover()

        if self.disparo is None and tiempo_actual - self.tiempo_disparo > self.intervalo_disparo:
            base_x, base_y = 100, ALTO_PANTALLA - 150
            self.nave_atacante = Nave(x=base_x, y=base_y)
            self.disparo = Disparo(base_x + 10, base_y + 10)
            self.enemigo = Enemigo(base_x + 10, base_y - 100)
            self.tiempo_disparo = tiempo_actual
            self.intervalo_disparo = random.randint(5000, 10000)

        if self.disparo:
            self.disparo.mover()
            if self.enemigo and not self.enemigo.explotando and self.enemigo.impactado_por(self.disparo):
                self.enemigo.explotando = True
                self.disparo.activo = False

            if not self.disparo.activo:
                self.disparo = None
                self.nave_atacante = None
                self.enemigo = None

        if random.randint(0, 100) < 2:
            self.naves.append(Nave())
        for nave in self.naves[:]:
            nave.mover()
            if nave.esta_fuera_de_pantalla():
                self.naves.remove(nave)

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)
        mouse_pos = pygame.mouse.get_pos()

        for estrella in self.estrellas:
            estrella.dibujar(pantalla)

        if self.nave_atacante:
            self.nave_atacante.dibujar(pantalla)

        if self.disparo:
            self.disparo.dibujar(pantalla)

        if self.enemigo:
            if not self.enemigo.dibujar(pantalla):
                self.enemigo = None

        for nave in self.naves:
            nave.dibujar(pantalla)

        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente, mouse_pos)
