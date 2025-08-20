from enemies.enemy import Enemy
import random

class EnemyManager:
    def __init__(self):
        # El método __init__ se ejecuta cuando se crea una nueva instancia del gestor.
        
        # 'enemigos' es una lista que almacenará todos los objetos de la clase Enemy.
        # Sirve para llevar un registro de todos los enemigos activos en el juego.
        self.enemigos = []
        
        # 'spawn_timer' es un contador que se incrementa en cada fotograma del juego.
        # Su propósito es controlar cuándo debe aparecer un nuevo enemigo.
        self.spawn_timer = 0
        
        # 'spawn_interval' define cuántos fotogramas deben pasar antes de que
        # un nuevo enemigo sea creado. Un valor de 60 equivale a 1 segundo si el
        # juego corre a 60 FPS (fotogramas por segundo).
        self.spawn_interval = 60

    def actualizar(self):
        # Este método se llama en cada fotograma del bucle principal del juego.
        # Es responsable de la lógica del gestor de enemigos.
        
        # 1. Lógica de "spawn" (aparición) de enemigos
        # Incrementa el contador del temporizador en cada fotograma.
        self.spawn_timer += 1
        
        # Comprueba si el contador ha alcanzado el intervalo de aparición.
        if self.spawn_timer >= self.spawn_interval:
            # Si el tiempo ha pasado, reinicia el temporizador para el siguiente ciclo.
            self.spawn_timer = 0
            
            # Crea una nueva instancia de la clase Enemy.
            # La posición 'x' es aleatoria (entre 0 y el ancho de la pantalla - 30).
            # La posición 'y' se establece en -20 para que el enemigo aparezca
            # justo por encima del borde superior de la pantalla.
            nuevo = Enemy(random.randint(0, 800 - 30), -20)
            
            # Agrega el nuevo enemigo a la lista de enemigos activos.
            self.enemigos.append(nuevo)

        # 2. Lógica de movimiento de enemigos
        # Itera sobre cada enemigo en la lista.
        for enemigo in self.enemigos:
            # Llama al método 'mover' de cada enemigo para actualizar su posición.
            enemigo.mover()

    def dibujar(self, pantalla):
        # Este método se encarga de dibujar a todos los enemigos en la pantalla.
        
        # Itera sobre cada enemigo en la lista.
        for enemigo in self.enemigos:
            # Llama al método 'dibujar' de cada enemigo, pasándole el objeto 'pantalla'
            # para que el enemigo se pueda dibujar a sí mismo.
            enemigo.dibujar(pantalla)