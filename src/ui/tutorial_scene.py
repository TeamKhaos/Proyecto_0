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
        self.nave.x = self.centro_x - self.nave.ancho // 2
        self.nave.y = 300
        
        self.paso_actual = 0
        self.timer_texto = 0
        self.mensajes = [
            "¡BIENVENIDO PILOTO! VAMOS A PRACTICAR.",
            "USA 'WASD' PARA MOVER TU NAVE POR LA PANTALLA.",
            "¡MUY BIEN! AHORA INTENTA DISPARAR CON LA TECLA 'J'.",
            "UN ENEMIGO HA APARECIDO. ¡DESTRÚYELO!",
            "ERROR: Pygame.Surface_Lock(ID:0x666) FAILED.",
            "FATAL: RECURSION_LIMIT_EXCEEDED in 'StarRogue.py'",
            "CRITICAL: Memory leak at 0xAA00BB - EXIT NOW.",
            "¡SISTEMA REESTABLECIDO! PULSA 'CONTINUAR'."
        ]
        
        # Nuevos mensajes sospechosos (Color Rojo)
        self.mensajes_creepys = {
            4: "AttributeError: 'Player' is already dead.",
            5: "OSError: [Errno 13] Access to reality denied.",
            6: "RuntimeError: Unable to locate USER_SOUL.DLL"
        }
        
        # Caracteres para el efecto de glitch
        self.glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/0123456789"
        self.timer_decodificacion = 0
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
        
        # --- Variables de Glitch ---
        self.glitch_fuerza = 0
        self.invertir_colores = False

    def configurar_boss(self):
        # En el tutorial no hay boss real a menos que queramos mostrarlo
        self.boss.aparecido = False
        self.boss.vida = 0
        self.boss.derrotado = False

    def actualizar(self):
        if self.pausa or self.victoria or self.game_over: return

        self.parallax.actualizar()
        self.shake.actualizar() 
        
        # --- LÓGICA DE CORRUPCIÓN (Fase 12) ---
        if self.paso_actual >= 4:
            self.glitch_fuerza = (self.paso_actual - 3) * 6
            # Sacudida aleatoria constante
            if random.random() < 0.1:
                self.shake.activar(5, self.glitch_fuerza)
            
            # Inversión de colores ráfaga
            self.invertir_colores = random.random() < 0.05 * (self.paso_actual - 3)

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
        if self.pausa: self.mostrar_menu_pausa(pantalla); return

        self.surface_juego.fill(NES_BLACK)
        self.parallax.dibujar(self.surface_juego)
        
        for e in self.enemy_manager.enemigos: e.dibujar(self.surface_juego)
        for b in self.balas_jugador: b.dibujar(self.surface_juego)
        for b in self.balas_enemigas: b.dibujar(self.surface_juego)
        self.particle_manager.dibujar(self.surface_juego)
        
        # --- CAJA DE TEXTO DEL TUTORIAL ---
        if self.paso_actual < len(self.mensajes):
            txt_box = pygame.Rect(50, 480, 700, 80)
            pygame.draw.rect(self.surface_juego, (0, 0, 50, 200), txt_box, border_radius=10)
            pygame.draw.rect(self.surface_juego, NES_WHITE, txt_box, 2, border_radius=10)
            
            # Lógica de mensajes normales vs creepys
            msg_final = self.mensajes[self.paso_actual]
            color_msg = NES_WHITE
            
            # Determinar si el mensaje es creepy
            es_creepy = self.paso_actual in self.mensajes_creepys
            if es_creepy:
                msg_final = self.mensajes_creepys[self.paso_actual]
                color_msg = NES_RED
            
            # --- EFECTO DE DECODIFICACIÓN (GLITCH TEXT) ---
            if self.paso_actual >= 4:
                char_list = list(msg_final)
                for i in range(len(char_list)):
                    # Probabilidad de glichear un caracter cada frame
                    if random.random() < 0.1:
                        char_list[i] = random.choice(self.glitch_chars)
                msg_final = "".join(char_list)
            
            txt_render = self.font_pquena.render(msg_final, True, color_msg)
            self.surface_juego.blit(txt_render, txt_render.get_rect(center=txt_box.center))

        # Dibujar Nave y UI
        self.nave.dibujar(self.surface_juego)
        self.hb_jugador.dibujar(self.surface_juego)
        
        # --- INDICADORES WASD (Nuevo Feedback Visual) ---
        if self.paso_actual == 1: # Mostrar SOLO en el paso de movimiento
            self.dibujar_controles_wasd(self.surface_juego)

        if self.victoria: self.mostrar_victoria(self.surface_juego)
        if self.game_over: self.mostrar_game_over(self.surface_juego)
        
        # --- EFECTOS DE CORRUPCIÓN (GLITCH) ---
        if self.invertir_colores:
            # Efecto de inversión rápida (Fase 12)
            self.surface_juego.blit(self.surface_juego, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
        
        # Estática aleatoria (Líneas rojas y ruido)
        if self.paso_actual >= 5 and random.random() < 0.15:
            for _ in range(15):
                rx = random.randint(0, 800)
                ry = random.randint(0, 600)
                rw = random.randint(20, 300)
                rh = random.randint(1, 3)
                pygame.draw.rect(self.surface_juego, NES_RED, (rx, ry, rw, rh))

        # Aplicar Shake y Blit final
        offset = self.shake.get_offset()
        pantalla.blit(self.surface_juego, offset)

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
        from scenes.level_1 import NivelUnoScene
        SceneManager.cambiar_escena(NivelUnoScene(self.nombre))

    def dibujar_controles_wasd(self, pantalla):
        """Dibuja indicadores visuales de las teclas WASD que se iluminan al pulsar."""
        base_x, base_y = self.centro_x - 60, 400
        size = 40
        gap = 5
        
        teclas = [
            ("W", (base_x + size + gap, base_y)),
            ("A", (base_x, base_y + size + gap)),
            ("S", (base_x + size + gap, base_y + size + gap)),
            ("D", (base_x + (size + gap) * 2, base_y + size + gap))
        ]
        
        for tecla, pos in teclas:
            rect = pygame.Rect(pos[0], pos[1], size, size)
            esta_pulsada = self.nave.teclas_estado.get(tecla, False)
            
            # Color basado en el estado
            color_fondo = NES_YELLOW if esta_pulsada else (40, 40, 40)
            color_texto = NES_BLACK if esta_pulsada else NES_WHITE
            
            # Dibujar Tecla
            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=5)
            pygame.draw.rect(pantalla, NES_WHITE, rect, 2, border_radius=5)
            
            # Dibujar Letra
            t = self.font_pquena.render(tecla, True, color_texto)
            pantalla.blit(t, t.get_rect(center=rect.center))
