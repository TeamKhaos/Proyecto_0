import pygame

class Enemy:
    def __init__(self, x, y, velocidad=2):
        # El método __init__ se llama cuando creas un nuevo objeto (instancia) de la clase Enemy.
        
        # 1. Posición y velocidad iniciales
        # Guarda la posición inicial del enemigo en la pantalla.
        self.x = x
        self.y = y
        # Define la velocidad a la que el enemigo se moverá por cada fotograma.
        self.velocidad = velocidad
        
        # 2. Configuración de la animación
        # 'frames' es una lista que guardará cada imagen de la animación.
        self.frames = []
        # El bucle recorre de 0 a 3 para cargar las 4 imágenes de la animación.
        for i in range(4):
            # Carga la imagen de un archivo. La ruta es relativa al directorio de trabajo.
            # .convert_alpha() optimiza la imagen para Pygame, manteniendo la transparencia.
            frame = pygame.image.load(f"assets/images/enemies/Enemy{i}.png").convert_alpha()
            # Escala la imagen a un tamaño específico (en este caso, 64x64 píxeles).
            frame = pygame.transform.scale(frame, (64, 64))
            # Agrega la imagen procesada a la lista de frames.
            self.frames.append(frame)

        # 3. Variables de control de la animación
        # 'frame_actual' es el índice de la imagen que se está mostrando en este momento.
        self.frame_actual = 0
        # 'tiempo_entre_frames' controla la velocidad de la animación.
        # Por ejemplo, un valor de 5 significa que la imagen cambia cada 5 fotogramas del juego.
        self.tiempo_entre_frames = 5
        # 'contador_animacion' lleva la cuenta de los fotogramas transcurridos para saber cuándo cambiar de imagen.
        self.contador_animacion = 0

    def mover(self):
        # El método 'mover' actualiza la posición del enemigo.
        # Aumenta el valor 'y' para mover al enemigo hacia abajo en la pantalla.
        self.y += self.velocidad

    def actualizar_animacion(self):
        # Este método gestiona la lógica para cambiar al siguiente fotograma de la animación.
        # Incrementa el contador en cada llamada.
        self.contador_animacion += 1
        # Comprueba si el tiempo necesario para el cambio ha pasado.
        if self.contador_animacion >= self.tiempo_entre_frames:
            # Pasa al siguiente fotograma. El operador `%` (módulo) se asegura de que el índice
            # vuelva a 0 cuando llega al final de la lista, creando un bucle infinito de la animación.
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            # Reinicia el contador para comenzar a contar para el siguiente cambio de fotograma.
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        # El método 'dibujar' se encarga de mostrar al enemigo en la pantalla.
        # Primero, actualiza el estado de la animación (cambia de imagen si es necesario).
        self.actualizar_animacion()
        # Obtiene la imagen del fotograma actual de la lista.
        imagen = self.frames[self.frame_actual]
        # Dibuja la imagen en la pantalla, en la posición (x, y) del enemigo.
        pantalla.blit(imagen, (self.x, self.y))

    def obtener_rect(self):
        # Devuelve el rectángulo de colisión del enemigo.
        return self.frames[self.frame_actual].get_rect(x=self.x, y=self.y)