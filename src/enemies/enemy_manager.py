from enemies.enemy import Enemy
import random

class EnemyManager:
    def __init__(self, nivel=1, target=None):
        self.enemigos = []
        self.spawn_timer = 0
        self.nivel = nivel
        self.target = target
        
        # --- Configuración de Oleadas ---
        self.oleada_actual = 1
        self.max_oleadas = 3 if nivel == 1 else 5 # Más oleadas en nivel 2
        self.enemigos_restantes_oleada = 0
        self.total_enemigos_spawnear = 0
        self.esperando_siguiente_oleada = False
        self.timer_entre_oleadas = 0
        
        self.iniciar_oleada(1)

    def iniciar_oleada(self, numero):
        self.oleada_actual = numero
        base_enemigos = 5 if self.nivel == 1 else 8
        self.total_enemigos_spawnear = base_enemigos + (numero * 3) 
        self.enemigos_restantes_oleada = self.total_enemigos_spawnear
        
        base_interval = 60 if self.nivel == 1 else 45
        self.spawn_interval = max(15, base_interval - (numero * 8))
        self.esperando_siguiente_oleada = False

    def actualizar(self):
        nuevas_balas = []
        
        # Si la oleada ha terminado y no hay enemigos en pantalla
        if self.enemigos_restantes_oleada <= 0 and len(self.enemigos) == 0:
            if self.oleada_actual < self.max_oleadas:
                self.esperando_siguiente_oleada = True
                self.timer_entre_oleadas += 1
                if self.timer_entre_oleadas >= 120:
                    self.timer_entre_oleadas = 0
                    self.iniciar_oleada(self.oleada_actual + 1)
                return "NEXT_WAVE", nuevas_balas
            else:
                return "BOSS_TIME", nuevas_balas

        # Lógica de "spawn"
        if self.enemigos_restantes_oleada > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.enemigos_restantes_oleada -= 1
                
                velocidad = (2 if self.nivel == 1 else 3) + (self.oleada_actual * 0.5)
                
                # Elegir IA según el nivel y oleada
                ia_type = "zigzag"
                if self.nivel == 2:
                    rand = random.random()
                    if rand < 0.4: ia_type = "tracker"
                    elif rand < 0.6: ia_type = "kamikaze"
                
                nuevo = Enemy(random.randint(50, 750), -50, velocidad=velocidad, ia_type=ia_type, target=self.target)
                self.enemigos.append(nuevo)

        # Mover enemigos y manejar disparos
        for enemigo in self.enemigos[:]:
            enemigo.mover()
            
            # IA de disparo: solo si está dentro de la pantalla
            if 0 < enemigo.y < 550:
                if enemigo.puede_disparar():
                    nuevas_balas.append(enemigo.disparar())

            if enemigo.y > 600:
                if enemigo in self.enemigos: self.enemigos.remove(enemigo)
        
        status = "WAVE_IN_PROGRESS"
        if self.esperando_siguiente_oleada:
            status = "NEXT_WAVE"
            
        return status, nuevas_balas

    def dibujar(self, pantalla):
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)
