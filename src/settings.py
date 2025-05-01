import pygame
WIDTH, HEIGHT = 800, 600
FULLSCREEN = False

def conf_ventana():
    pygame.display.set_caption("Star Rogue")  # Título de la ventana
    
    # Cargar y establecer el ícono
    try:
        icono = pygame.image.load("assets/images/icono.png")  # Ruta relativa al ícono
        pygame.display.set_icon(icono)
    except FileNotFoundError:
        print("¡Advertencia: No se encontró el archivo del ícono!")

def crear_pantalla():
    flags = pygame.NOFRAME if FULLSCREEN else 0
    return pygame.display.set_mode((WIDTH, HEIGHT), flags)