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

# Inicializar Audio DESPUÉS de crear la pantalla
from engine.audio_manager import AudioManager
AudioManager.play_boton() # Intento de carga inicial silenciosa

pantalla_virtual = pygame.Surface((V_WIDTH, V_HEIGHT))
clock = pygame.time.Clock()

SceneManager.cambiar_escena(SplashScene())

# Sobrescribir pygame.mouse.get_pos una sola vez (Optimización)
original_get_pos = pygame.mouse.get_pos
rect_destino, pos_destino = calcular_redimension(pantalla_real.get_width(), pantalla_real.get_height())

def get_virtual_mouse_pos():
    return transformar_mouse(original_get_pos(), rect_destino, pos_destino)
pygame.mouse.get_pos = get_virtual_mouse_pos

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

    # 1. Manejar eventos y actualizar lógica
    SceneManager.manejar_eventos(eventos, pantalla_virtual)
    SceneManager.actualizar()
    
    # 2. Dibujar en la pantalla VIRTUAL
    pantalla_virtual.fill((0, 0, 0))
    SceneManager.dibujar(pantalla_virtual)
    
    # Restaurar get_pos temporalmente si fuera necesario (aquí no hace falta si se mantiene consistente)

    # 3. Proyectar en la pantalla REAL con Letterboxing
    pantalla_real.fill((0, 0, 0)) # Barras negras
    # Usar scale en lugar de smoothscale para mayor rendimiento (y look pixel-art más nítido)
    pantalla_escalada = pygame.transform.scale(pantalla_virtual, rect_destino)
    pantalla_real.blit(pantalla_escalada, pos_destino)
    
    pygame.display.flip()
    clock.tick(60)
