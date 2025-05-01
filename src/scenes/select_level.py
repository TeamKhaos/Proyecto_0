# src/scenes/select_level.py
import pygame
import random

# Colores estilo NES
NEGRO = (0, 0, 0)
GRIS = (192, 192, 192)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

class Boton:
    def __init__(self, texto, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = GRIS
        self.color_hover = ROJO
        self.color_texto = NEGRO

    def dibujar(self, pantalla, fuente, mouse_pos):
        color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_normal
        pygame.draw.rect(pantalla, color, self.rect)
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
        pygame.draw.circle(pantalla, BLANCO, (int(self.x), int(self.y)), self.tamano)

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
        pygame.draw.polygon(pantalla, ROJO, puntos)

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
        pygame.draw.circle(pantalla, AMARILLO, (int(self.x), int(self.y)), 4)

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.explotando = False
        self.contador_explosion = 0

    def dibujar(self, pantalla):
        if self.explotando:
            if self.contador_explosion < 45:
                pygame.draw.circle(pantalla, ROJO, (int(self.x), int(self.y)), 15)
            elif self.contador_explosion < 90:
                pygame.draw.circle(pantalla, AMARILLO, (int(self.x), int(self.y)), 20)
            else:
                return False  # ya terminó la animación
            self.contador_explosion += 1
        else:
            pygame.draw.rect(pantalla, GRIS, (self.x - 10, self.y - 10, 20, 20))
        return True

    def impactado_por(self, disparo):
        distancia = ((self.x - disparo.x) ** 2 + (self.y - disparo.y) ** 2) ** 0.5
        return distancia < 20

def pantalla_select_level(pantalla):
    fuente = pygame.font.SysFont("Courier", 30, bold=True)
    botones = [
        Boton("Tutorial", 300, 200, 200, 50),
        Boton("Nivel 1", 300, 270, 200, 50),
        Boton("Nivel 2", 300, 340, 200, 50)
    ]

    estrellas = [Estrella() for _ in range(50)]
    naves = []
    reloj = pygame.time.Clock()

    # Disparo automático
    evento_disparo = 0
    intervalo_disparo = random.randint(5000, 10000)

    disparo = None
    enemigo = None
    nave_atacante = None

    esperando = True
    while esperando:
        pantalla.fill(NEGRO)
        tiempo_actual = pygame.time.get_ticks()

        for estrella in estrellas:
            estrella.mover()
            estrella.dibujar(pantalla)

        # Evento automático de disparo en esquina inferior
        if disparo is None and tiempo_actual - evento_disparo > intervalo_disparo:
            base_x = 100
            base_y = ALTO_PANTALLA - 150
            nave_atacante = Nave(x=base_x, y=base_y)
            disparo = Disparo(nave_atacante.x + 10, nave_atacante.y + 10)
            enemigo = Enemigo(nave_atacante.x + 10, nave_atacante.y - 100)  # Mayor distancia
            evento_disparo = tiempo_actual
            intervalo_disparo = random.randint(5000, 10000)

        # Animación del disparo
        if disparo:
            nave_atacante.dibujar(pantalla)
            disparo.mover()
            disparo.dibujar(pantalla)

            if enemigo:
                if not enemigo.explotando and enemigo.impactado_por(disparo):
                    enemigo.explotando = True
                    disparo.activo = False
                if not enemigo.dibujar(pantalla):
                    enemigo = None
                    disparo = None
                    nave_atacante = None

            if not disparo.activo:
                disparo = None

        # Dibujar otras naves de fondo
        if random.randint(0, 100) < 2:
            naves.append(Nave())
        for nave in naves[:]:
            nave.mover()
            nave.dibujar(pantalla)
            if nave.esta_fuera_de_pantalla():
                naves.remove(nave)

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for boton in botones:
            boton.dibujar(pantalla, fuente, mouse_pos)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
                pygame.quit()
                return
            for i, boton in enumerate(botones):
                if boton.esta_presionado(evento):
                    esperando = False
                    return i

        pygame.display.flip()
        reloj.tick(60)
