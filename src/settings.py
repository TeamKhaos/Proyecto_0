import pygame
WIDTH, HEIGHT = 800, 600
FULLSCREEN = False

def crear_pantalla():
    flags = pygame.NOFRAME if FULLSCREEN else 0
    return pygame.display.set_mode((WIDTH, HEIGHT), flags)