import pygame
import math
import random
from enemies.bala import Bala, BalaGranada
from assets.colors import NES_RED, NES_ORANGE, NES_YELLOW, NES_WHITE
from engine.asset_manager import AssetManager

class Boss:
    def __init__(self, target=None, tint_color=None, nivel=1):
        self.x = 300
        self.y = -250
        self.velocidad = 1
        self.vida = 100
        self.max_vida = 100
        self.aparecido = False
        self.entrada_completa = False 
        self.derrotado = False
        self.target = target
        self.tint_color = tint_color
        self.nivel = nivel # Identificar el nivel para la IA
        
        # --- Movimiento ---
        self.direccion_x = 1
        self.velocidad_x = 2 if nivel == 1 else 4
        self.timer_movimiento = 0
        
        # --- Disparo ---
        self.shoot_timer = 0
        self.shoot_delay = 60 
        self.ancho = 200
        self.alto = 200
        self.patron_actual = 0 
        self.angulo_espiral = 0
        
        # Especial Nivel 2
        self.timer_granada = 0
        self.delay_granada = 180 # Cada 3 segundos aprox

        self.frames = []
        try:
            for i in range(4):
                img = AssetManager.get_image(f"assets/images/enemies/boss{i}.png", (200, 200))
                if self.tint_color:
                    img_tintada = img.copy()
                    img_tintada.fill((*self.tint_color, 255), special_flags=pygame.BLEND_RGBA_MULT)
                    self.frames.append(img_tintada)
                else:
                    self.frames.append(img)
        except:
            self.frames = [None]

        self.frame_actual = 0
        self.contador_animacion = 0
        self.tiempo_entre_frames = 6

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.vida = 0
            self.morir()
            
    def morir(self):
        if not self.derrotado:
            self.derrotado = True
            self.aparecido = False

    def aparecer(self):
        self.aparecido = True

    def mover(self):
        if not self.aparecido: 
            return

        # Fase de entrada (Solo ocurre una vez)
        if not self.entrada_completa:
            self.y += self.velocidad
            if self.y >= 50:
                self.y = 50
                self.entrada_completa = True
            return

        # Lógica de movimiento principal
        porcentaje_vida = self.vida / self.max_vida
        self.timer_movimiento += 1

        if porcentaje_vida > 0.7:
            # Fase 1: Rebote lateral + Oscilación vertical
            self.x += self.velocidad_x * self.direccion_x
            if self.x >= 800 - self.ancho:
                self.x = 800 - self.ancho
                self.direccion_x = -1
            elif self.x <= 0:
                self.x = 0
                self.direccion_x = 1
            
            # Aquí self.y puede bajar de 50 sin reactivar la entrada
            self.y = 50 + math.sin(self.timer_movimiento * 0.05) * 20
        
        elif porcentaje_vida > 0.3:
            # Fase 2: Infinito (8)
            t = self.timer_movimiento * 0.03
            self.x = 400 - (self.ancho // 2) + math.sin(t) * 250
            self.y = 70 + math.cos(t * 2) * 50
        
        else:
            # Fase 3: Persecución Agresiva
            if self.target:
                centro_boss = self.x + self.ancho // 2
                centro_player = self.target.x + self.target.ancho // 2
                distancia = centro_player - centro_boss
                self.x += distancia * 0.05
            
            self.x = max(0, min(800 - self.ancho, self.x))
            self.y = 60 + math.sin(self.timer_movimiento * 0.1) * 15

    def puede_disparar(self):
        if not self.aparecido or self.y < 50: return False
        self.shoot_timer += 1
        
        porcentaje_vida = self.vida / self.max_vida
        
        # Lógica de Granada (Nivel 2)
        if self.nivel == 2:
            self.timer_granada += 1
            if self.timer_granada >= self.delay_granada:
                self.timer_granada = 0
                return "GRANADA"

        if porcentaje_vida > 0.7: self.patron_actual = 0
        elif porcentaje_vida > 0.4: self.patron_actual = 1
        else: self.patron_actual = 2 if random.random() > 0.3 else 3

        current_delay = self.shoot_delay
        if self.patron_actual == 1: current_delay = 12 
        if self.patron_actual == 3: current_delay = 5 
            
        if self.shoot_timer >= current_delay:
            self.shoot_timer = 0
            return True
        return False

    def disparar(self, tipo=None):
        balas = []
        cx, cy = self.x + 100, self.y + 180
        
        if tipo == "GRANADA":
            balas.append(BalaGranada(cx, cy, velocidad=6, color=NES_ORANGE))
            return balas

        if self.patron_actual == 0: # Fan (Abanico)
            for angulo in range(-45, 46, 15):
                rad = math.radians(angulo + 90)
                balas.append(Bala(cx, cy, vx=math.cos(rad)*4, vy=math.sin(rad)*4, color=NES_RED))
        
        elif self.patron_actual == 1: # Spiral (Espiral)
            rad = math.radians(self.angulo_espiral)
            balas.append(Bala(cx, cy, vx=math.cos(rad)*5, vy=math.sin(rad)*5, color=NES_ORANGE))
            self.angulo_espiral += 25
            
        elif self.patron_actual == 2: # Targeted (Dirigido)
            if self.target:
                tx, ty = self.target.x + 32, self.target.y + 32
                dx, dy = tx - cx, ty - cy
                mag = math.sqrt(dx**2 + dy**2)
                if mag > 0:
                    balas.append(Bala(cx, cy, vx=(dx/mag)*7, vy=(dy/mag)*7, color=NES_YELLOW))
        
        elif self.patron_actual == 3: # Chaos (Lluvia aleatoria)
            vx = random.uniform(-3, 3)
            vy = random.uniform(4, 8)
            balas.append(Bala(cx, cy, vx=vx, vy=vy, color=NES_WHITE))
                
        return balas

    def actualizar_animacion(self):
        if not self.frames[0]: return
        self.contador_animacion += 1
        if self.contador_animacion >= self.tiempo_entre_frames:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        if self.aparecido:
            self.actualizar_animacion()
            if self.frames[0]:
                pantalla.blit(self.frames[self.frame_actual], (self.x, self.y))
            else:
                pygame.draw.rect(pantalla, NES_RED, (self.x + 20, self.y + 20, 160, 160))

    def obtener_rect(self):
        return pygame.Rect(self.x + 20, self.y + 20, 160, 160)
