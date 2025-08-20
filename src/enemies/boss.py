import pygame

class Boss:
    def __init__(self):
        # El método __init__ se ejecuta al crear un nuevo objeto (instancia) de la clase Boss.
        
        # Posición inicial del jefe.
        # Se coloca fuera de la pantalla (y = -150) para que no sea visible al inicio.
        self.x = 300
        self.y = -150
        self.velocidad = 1
        
        # 'self.aparecido' es una bandera (flag) que controla si el jefe ya debe ser visible y moverse.
        # Se inicia en False, ya que el jefe no aparece al comienzo del nivel.
        self.aparecido = False

        # --- Lógica de la animación ---
        # 'frames' es una lista que guardará cada imagen de la animación del jefe.
        self.frames = []
        
        # El bucle recorre de 0 a 3 (o sea, 4 veces) para cargar las imágenes.
        for i in range(4):
            # Carga la imagen de un archivo. La ruta es relativa al directorio de trabajo.
            # .convert_alpha() optimiza la imagen para Pygame, manteniendo la transparencia.
            # La ruta "assets/images/enemies/boss{i}.png" asume que las imágenes están ahí.
            frame = pygame.image.load(f"assets/images/enemies/boss{i}.png").convert_alpha()
            # Escala la imagen a un tamaño específico (200x200 píxeles).
            frame = pygame.transform.scale(frame, (200, 200))
            # Añade la imagen a la lista de frames.
            self.frames.append(frame)

        # Variables para controlar el estado de la animación
        self.frame_actual = 0  # Índice de la imagen que se muestra actualmente.
        self.contador_animacion = 0  # Contador para controlar el tiempo entre cambios de frame.
        self.tiempo_entre_frames = 6  # Define la velocidad de la animación. A mayor valor, más lenta es la animación.

    def aparecer(self):
        # Este método cambia la bandera 'self.aparecido' a True.
        # Esto hace que el jefe comience a moverse y a dibujarse en la pantalla.
        self.aparecido = True

    def mover(self):
        # El método 'mover' se encarga de la lógica de movimiento del jefe.
        # Se ejecuta solo si el jefe ya ha "aparecido" y su posición 'y' es menor que 100.
        # Esto asegura que el jefe solo se mueva hasta una posición específica en la pantalla (y=100) y se detenga ahí.
        if self.aparecido and self.y < 100:
            self.y += self.velocidad

    def actualizar_animacion(self):
        # Esta función gestiona el cambio de un frame de animación al siguiente.
        self.contador_animacion += 1
        
        # Comprueba si ha pasado el número de frames necesario para cambiar de imagen.
        if self.contador_animacion >= self.tiempo_entre_frames:
            # Actualiza el índice del frame actual al siguiente.
            # El operador % (módulo) asegura que el índice vuelva a 0 al llegar al final de la lista, creando un bucle infinito.
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0  # Reinicia el contador para el próximo ciclo de animación.

    def dibujar(self, pantalla):
        # El método 'dibujar' se encarga de renderizar al jefe en la pantalla.
        # Solo se dibuja si la bandera 'self.aparecido' es True.
        if self.aparecido:
            self.actualizar_animacion() # Llama a la función para actualizar la animación antes de dibujar.
            # Dibuja la imagen del frame actual en la posición (self.x, self.y) del jefe.
            pantalla.blit(self.frames[self.frame_actual], (self.x, self.y))
    def obtener_rect(self):
        # Devuelve un rectángulo que representa la posición y tamaño del jefe.
        return pygame.Rect(self.x, self.y, 200, 200)