import sys, os, pygame

# Asegura que el proyecto esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.scene_manager import SceneManager
from ui.splash_scene import SplashScene
from settings import crear_pantalla

pygame.init()
pantalla = crear_pantalla()
clock = pygame.time.Clock()

SceneManager.cambiar_escena(SplashScene())


while True:
    eventos = pygame.event.get()
    SceneManager.manejar_eventos(eventos, pantalla)  # Pasa pantalla aquí
    SceneManager.actualizar()
    SceneManager.dibujar(pantalla)
    pygame.display.flip()
    clock.tick(60)
