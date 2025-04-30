import pygame
import sys
# Como hacer que corra el juego pip install pygame

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pantalla Negra")

# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    pantalla.fill((0, 0, 0))  # Negro
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
