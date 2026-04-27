import sys, os, pygame

# Cambiar el directorio de trabajo a la carpeta donde está este archivo (src)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

from engine.scene_manager import SceneManager
from ui.splash_scene import SplashScene
from settings import crear_pantalla, conf_ventana, V_WIDTH, V_HEIGHT, calcular_redimension, transformar_mouse

pygame.init()
conf_ventana() 

# Crear la ventana inicial
pantalla_real = crear_pantalla()
pantalla_virtual = pygame.Surface((V_WIDTH, V_HEIGHT))
clock = pygame.time.Clock()

SceneManager.cambiar_escena(SplashScene())

while True:
    # Obtener la superficie de pantalla actual (por si cambió)
    pantalla_real = pygame.display.get_surface()
    if pantalla_real is None:
        # Si por alguna razón la pantalla se cerró momentáneamente durante un cambio de modo
        pantalla_real = crear_pantalla()

    eventos = pygame.event.get()
    
    # Recalcular dimensiones de escalado ANTES de transformar el mouse
    rect_destino, pos_destino = calcular_redimension(pantalla_real.get_width(), pantalla_real.get_height())

    # Transformar coordenadas del mouse en los eventos
    for event in eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if hasattr(event, "pos"):
            event.pos = transformar_mouse(event.pos, rect_destino, pos_destino)

    # Sobrescribir pygame.mouse.get_pos para que las escenas lo usen correctamente
    original_get_pos = pygame.mouse.get_pos
    pygame.mouse.get_pos = lambda: transformar_mouse(original_get_pos(), rect_destino, pos_destino)

    # 1. Manejar eventos y actualizar lógica
    SceneManager.manejar_eventos(eventos, pantalla_virtual)
    SceneManager.actualizar()
    
    # Obtener la superficie de pantalla actual después de manejar eventos (por si cambió el modo)
    pantalla_real = pygame.display.get_surface()
    if pantalla_real is None:
        pantalla_real = crear_pantalla()

    # Recalcular dimensiones de escalado (importante si cambió el modo de pantalla)
    rect_destino, pos_destino = calcular_redimension(pantalla_real.get_width(), pantalla_real.get_height())

    # 2. Dibujar en la pantalla VIRTUAL
    pantalla_virtual.fill((0, 0, 0))
    SceneManager.dibujar(pantalla_virtual)
    
    # Restaurar get_pos al final de todo el procesamiento de frame
    pygame.mouse.get_pos = original_get_pos

    # 3. Proyectar en la pantalla REAL con Letterboxing
    pantalla_real.fill((0, 0, 0)) # Barras negras
    pantalla_escalada = pygame.transform.smoothscale(pantalla_virtual, rect_destino)
    pantalla_real.blit(pantalla_escalada, pos_destino)
    
    pygame.display.flip()
    clock.tick(60)
