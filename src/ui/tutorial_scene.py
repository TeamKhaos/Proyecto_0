import pygame
import random
from scenes.base_level import BaseLevelScene
from enemies.enemy import Enemy
from assets.colors import *
from engine.audio_manager import AudioManager

class InteractiveTutorialScene(BaseLevelScene):
    def __init__(self, nombre_jugador):
        # Inicializamos como un nivel nivel=0 (Tutorial)
        super().__init__(nombre_jugador, nivel=0, meta_oleadas=1, bg_esquema="default")
        
        # Sobrescribir variables específicas del tutorial
        self.paso_actual = 0
        self.timer_texto = 0
        self.mensajes = [
            "¡BIENVENIDO PILOTO! VAMOS A PRACTICAR.",
            "USA 'WASD' PARA MOVER TU NAVE POR LA PANTALLA.",
            "¡MUY BIEN! AHORA INTENTA DISPARAR CON LA TECLA 'J'.",
            "UN ENEMIGO HA APARECIDO. ¡DESTRÚYELO!",
            "¡EXCELENTE! LOS ENEMIGOS TAMBIÉN DISPARAN. ¡ESQUIVA!",
            "EL JEFE APARECERÁ CUANDO COMPLETES LAS OLEADAS.",
            "¡ESTÁS LISTO PARA LA BATALLA! PULSA 'CONTINUAR'."
        ]
        
        # Deshabilitar spawns automáticos de EnemyManager
        self.enemy_manager.oleada_actual = 0
        self.enemy_manager.enemigos = []
        self.meta_oleadas = "TUTORIAL"
        
        # Flags de progreso
        self.teclas_movimiento_probadas = {"W": False, "A": False, "S": False, "D": False}
        self.disparo_probado = False
        self.enemigo_practica_muerto = False
        self.esquiva_probada = False
        
        # Para el paso de esquiva
        self.bala_tutorial = None

    def configurar_boss(self):
        # En el tutorial no hay boss real a menos que queramos mostrarlo
        self.boss.aparecido = False
        self.boss.vida = 0
        self.boss.derrotado = False

    def actualizar(self):
        if self.pausa or self.victoria or self.game_over: return

        self.parallax.actualizar()
        self.shake.actualizar() # Añadir actualización de sacudida
        
        # Bug 1 Fix: Bloqueo de movimiento hasta el paso 1
        if self.paso_actual >= 1:
            self.nave.mover(pygame.key.get_pressed())
            
        self.particle_manager.actualizar()
        
        # Actualizar barra de vida animada
        self.hb_jugador.actualizar(self.nave.vida, self.nave.max_vida)
        
        # Lógica de pasos del tutorial
        self.actualizar_logica_tutorial()
        
        # Actualizar proyectiles y colisiones
        for b in self.balas_jugador: b.mover()
        for b in self.balas_enemigas: b.mover()
        
        # Bug 2 Fix: Hacer que los enemigos en el tutorial disparen y se muevan
        for e in self.enemy_manager.enemigos:
            if self.paso_actual >= 4: # En el paso de esquiva ya pueden disparar
                if e.puede_disparar():
                    self.balas_enemigas.append(e.disparar())
            # Solo se mueven si no es el enemigo de práctica estático del paso 3
            if self.paso_actual > 3:
                e.mover()
        
        self.resolver_colisiones_tutorial()

    def actualizar_logica_tutorial(self):
        teclas = pygame.key.get_pressed()
        
        if self.paso_actual == 0: # Bienvenida
            self.timer_texto += 1
            if self.timer_texto > 180: # 3 segundos
                self.paso_actual = 1
                self.timer_texto = 0
                
        elif self.paso_actual == 1: # Movimiento
            if teclas[pygame.K_w]: self.teclas_movimiento_probadas["W"] = True
            if teclas[pygame.K_a]: self.teclas_movimiento_probadas["A"] = True
            if teclas[pygame.K_s]: self.teclas_movimiento_probadas["S"] = True
            if teclas[pygame.K_d]: self.teclas_movimiento_probadas["D"] = True
            
            if all(self.teclas_movimiento_probadas.values()):
                self.timer_texto += 1
                if self.timer_texto > 60:
                    self.paso_actual = 2
                    self.timer_texto = 0
                    
        elif self.paso_actual == 2: # Disparo
            if self.disparo_probado:
                self.timer_texto += 1
                if self.timer_texto > 60:
                    self.paso_actual = 3
                    self.timer_texto = 0
                    # Spawn enemigo de práctica quieto
                    en = Enemy(self.centro_x - 32, 100, velocidad=0, ia_type="zigzag")
                    en.shoot_delay = 999999 # No dispara todavía
                    self.enemy_manager.enemigos.append(en)

        elif self.paso_actual == 3: # Destruir enemigo
            if len(self.enemy_manager.enemigos) == 0:
                self.paso_actual = 4
                self.timer_texto = 0
                # Spawn enemigo que dispara
                en = Enemy(self.centro_x - 32, 100, velocidad=1)
                en.shoot_delay = 60 # Dispara rápido para practicar esquiva
                self.enemy_manager.enemigos.append(en)

        elif self.paso_actual == 4: # Esquiva
            # Si el jugador sobrevive a cierto tiempo esquivando, avanzamos
            if self.timer_texto > 400: # ~7 segundos esquivando
                self.paso_actual = 5
                self.timer_texto = 0
                self.enemy_manager.enemigos = []
                self.balas_enemigas = [] # Limpiar balas para la transición
            else:
                self.timer_texto += 1
                
        elif self.paso_actual == 5: # Info Boss
            self.timer_texto += 1
            if self.timer_texto > 180:
                self.paso_actual = 6
                self.timer_texto = 0

        elif self.paso_actual == 6: # Final
            self.victoria = True

    def resolver_colisiones_tutorial(self):
        # Similar a BaseLevelScene pero con ajustes para el flujo
        balas_j_eliminar = []
        for b in self.balas_jugador:
            for e in self.enemy_manager.enemigos:
                if b.obtener_rect().colliderect(e.obtener_rect()):
                    self.particle_manager.crear_explosion(e.x + e.ancho//2, e.y + e.alto//2, cantidad=20)
                    AudioManager.play_explosion()
                    self.enemy_manager.enemigos.remove(e)
                    balas_j_eliminar.append(b)
                    break
        self.balas_jugador = [b for b in self.balas_jugador if b not in balas_j_eliminar and b.y > -10]

        balas_e_eliminar = []
        nave_rect = self.nave.obtener_rect()
        for b in self.balas_enemigas:
            if b.obtener_rect().colliderect(nave_rect):
                self.nave.recibir_dano(0) # No recibe daño real en el tutorial para no morir
                self.particle_manager.crear_explosion(b.x, b.y, color=NES_LIGHT_BLUE, cantidad=10)
                AudioManager.play_explosion()
                balas_e_eliminar.append(b)
        self.balas_enemigas = [b for b in self.balas_enemigas if b not in balas_e_eliminar and b.y < 610]

    def disparar(self):
        # Bug 1 Fix: Bloqueo de disparo hasta el paso 2
        if self.paso_actual < 2: return
        
        super().disparar()
        if self.paso_actual == 2:
            self.disparo_probado = True

    def dibujar(self, pantalla):
        # Dibujamos todo lo de la base
        pantalla.fill(NES_BLACK)
        self.parallax.dibujar(pantalla)
        
        for e in self.enemy_manager.enemigos: e.dibujar(pantalla)
        for b in self.balas_jugador: b.dibujar(pantalla)
        for b in self.balas_enemigas: b.dibujar(pantalla)
        self.particle_manager.dibujar(pantalla)
        
        # --- CAJA DE TEXTO DEL TUTORIAL ---
        # Bug 1 Fix: Dibujar la caja ANTES que la nave para que la nave pueda estar "encima"
        if self.paso_actual < len(self.mensajes):
            txt_box = pygame.Rect(50, 480, 700, 80)
            pygame.draw.rect(pantalla, (0, 0, 50, 200), txt_box, border_radius=10)
            pygame.draw.rect(pantalla, NES_WHITE, txt_box, 2, border_radius=10)
            
            msg = self.mensajes[self.paso_actual]
            txt_render = self.font_pquena.render(msg, True, NES_WHITE)
            pantalla.blit(txt_render, txt_render.get_rect(center=txt_box.center))

        # Dibujar Nave al final para que siempre esté sobre todo lo demás
        self.nave.dibujar(pantalla)
        
        # Dibujar UI de Vida (Nueva sistema)
        self.hb_jugador.dibujar(pantalla)

        if self.pausa: self.mostrar_menu_pausa(pantalla)
        if self.victoria: self.mostrar_victoria(pantalla)
        if self.game_over: self.mostrar_game_over(pantalla)

    def mostrar_victoria(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)); pantalla.blit(overlay, (0, 0))
        
        # Bug 3 Fix: Reducir fuente si es necesario para evitar desbordamiento
        t = self.font.render("¡ENTRENAMIENTO COMPLETADO!", True, NES_GREEN)
        pantalla.blit(t, t.get_rect(center=(self.centro_x, self.centro_y - 50)))
        
        m = self.font_pquena.render("Ahora estás listo para la verdadera acción.", True, NES_WHITE)
        pantalla.blit(m, m.get_rect(center=(self.centro_x, self.centro_y + 20)))
        
        self.dibujar_boton(pantalla, "CONTINUAR", self.centro_y + 100)

    def reiniciar_nivel(self):
        from engine.scene_manager import SceneManager
        SceneManager.cambiar_escena(InteractiveTutorialScene(self.nombre))

    def finalizar_nivel(self):
        from engine.scene_manager import SceneManager
        from scenes.select_level import SelectLevelScene
        SceneManager.cambiar_escena(SelectLevelScene(self.nombre))
