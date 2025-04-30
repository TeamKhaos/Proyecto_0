import pygame
import sys
from scenes.select_level import pantalla_select_level
# Como hacer que corra el juego pip install pygame

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pantalla Negra")

# Colores para el boton
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

# Fuente para el boton
fuente = pygame.font.SysFont(None, 40)

# Función para crear un boton
def dibujar_boton(texto, x, y, ancho, alto):
    boton_rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, AZUL, boton_rect)
    texto_superficie = fuente.render(texto, True, BLANCO)
    texto_rect = texto_superficie.get_rect(center=boton_rect.center)
    pantalla.blit(texto_superficie, texto_rect)
    return boton_rect

# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton.collidepoint(evento.pos):
                pantalla_select_level(pantalla)

    pantalla.fill(NEGRO)
    boton = dibujar_boton("Ir a selección de nivel", 250, 250, 300, 60)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
