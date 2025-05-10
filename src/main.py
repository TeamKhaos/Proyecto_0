import sys, os, pygame

# Asegura que el proyecto esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.scene_manager import SceneManager
from ui.splash_scene import SplashScene
from settings import crear_pantalla, conf_ventana

pygame.init()
pygame.mixer.init()  # Inicializa el audio

# Reproduce el sonido de inicio solo una vez
sonido_inicio = pygame.mixer.Sound("assets/sounds/coin_inicio.wav")
sonido_inicio.play()

conf_ventana() 
pantalla = crear_pantalla()
clock = pygame.time.Clock()

SceneManager.cambiar_escena(SplashScene())

while True:
    eventos = pygame.event.get()
    SceneManager.manejar_eventos(eventos, pantalla)
    SceneManager.actualizar()
    SceneManager.dibujar(pantalla)
    pygame.display.flip()
    clock.tick(60)
