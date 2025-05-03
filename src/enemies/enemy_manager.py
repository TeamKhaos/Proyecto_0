from enemies.enemy import Enemy
import random

class EnemyManager:
    def __init__(self):
        self.enemigos = []
        self.spawn_timer = 0
        self.spawn_interval = 60  # frames entre enemigos

    def actualizar(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            nuevo = Enemy(random.randint(0, 800 - 30), -20)
            self.enemigos.append(nuevo)

        for enemigo in self.enemigos:
            enemigo.mover()

    def dibujar(self, pantalla):
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)
