import pygame

# Dimensiones virtuales (internas del juego)
V_WIDTH, V_HEIGHT = 800, 600

# Dimensiones reales de la ventana (pueden cambiar)
WIDTH, HEIGHT = 800, 600
FULLSCREEN = False

def conf_ventana():
    pygame.display.set_caption("Star Rogue")
    try:
        icono = pygame.image.load("assets/images/icono.png")
        pygame.display.set_icon(icono)
    except FileNotFoundError:
        print("¡Advertencia: No se encontró el archivo del ícono!")

def crear_pantalla():
    if FULLSCREEN:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    else:
        return pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)

def toggle_fullscreen():
    global FULLSCREEN
    FULLSCREEN = not FULLSCREEN
    return crear_pantalla()

def calcular_redimension(ventana_ancho, ventana_alto):
    """Calcula el tamaño y posición para mantener el aspect ratio 4:3"""
    escala = min(ventana_ancho / V_WIDTH, ventana_alto / V_HEIGHT)
    nuevo_ancho = int(V_WIDTH * escala)
    nuevo_alto = int(V_HEIGHT * escala)
    
    # Centrado
    x = (ventana_ancho - nuevo_ancho) // 2
    y = (ventana_alto - nuevo_alto) // 2
    
    return (nuevo_ancho, nuevo_alto), (x, y)

def transformar_mouse(pos_real, rect_destino, pos_destino):
    """Transforma las coordenadas del mouse reales a virtuales"""
    rx, ry = pos_real
    dx, dy = pos_destino
    nw, nh = rect_destino
    
    # Restar el offset del centrado y escalar
    vx = (rx - dx) * (V_WIDTH / nw)
    vy = (ry - dy) * (V_HEIGHT / nh)
    
    return int(vx), int(vy)
