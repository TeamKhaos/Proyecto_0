from scenes.base_level import BaseLevelScene
from engine.progreso_manager import completar_nivel_1
from engine.scene_manager import SceneManager
import pygame
import random
from assets.colors import *

class NivelUnoScene(BaseLevelScene):
    def __init__(self, nombre_jugador):
        super().__init__(nombre_jugador, nivel=1, meta_oleadas=3, bg_esquema="default")
        self.timer_glitch = 0
        self.input_delay_timer = 0

        # --- Lógica de Advertencia Forzada ---
        self.mostrar_advertencia_inicial = True
        self.mostrar_error_fake = False
        self.advertencia_rect = pygame.Rect(100, 150, 600, 300)
        self.btn_continuar = pygame.Rect(150, 350, 240, 50)
        self.btn_no_salir = pygame.Rect(410, 350, 240, 50)
        
        self.timer_error_fake = 0

        self.mensajes_sistema = [
            "¿POR QUÉ SIGUES DISPARANDO?",
            "ELLOS NO TE HICIERON NADA.",
            "TE ESTÁS EQUIVOCANDO.",
            "D-E-T-E-N-T-E"
        ]
        self.mensaje_actual = ""
        self.mostrar_mensaje_timer = 0

    def manejar_eventos(self, eventos, pantalla):
        if self.mostrar_advertencia_inicial:
            for event in eventos:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.btn_continuar.collidepoint(event.pos):
                            from engine.audio_manager import AudioManager
                            AudioManager.play_boton()
                            self.mostrar_advertencia_inicial = False
                        elif self.btn_no_salir.collidepoint(event.pos):
                            # Activar ERROR falso
                            self.mostrar_error_fake = True
                            from engine.audio_manager import AudioManager
                            AudioManager.play_boton()
            return

        super().manejar_eventos(eventos, pantalla)

    def actualizar(self):
        if self.mostrar_error_fake:
            self.timer_error_fake += 1
            if self.timer_error_fake > 90: # 1.5 segundos de error antes de forzar inicio
                self.mostrar_advertencia_inicial = False
                self.mostrar_error_fake = False
            return

        if self.mostrar_advertencia_inicial: return

        if self.pausa or self.victoria or self.game_over:
            super().actualizar()
            return

        # --- Efecto de Retraso de Input (Incomodidad) ---
        teclas = pygame.key.get_pressed()
        self.timer_glitch += 1
        
        # Cada cierto tiempo, el control se siente "pesado"
        if (self.timer_glitch // 120) % 2 == 0:
            self.nave.mover(teclas)
        else:
            # Simulamos lag de 5 frames (retraso intencionado)
            if self.timer_glitch % 5 == 0:
                self.nave.mover(teclas)

        # Mensajes aleatorios de incomodidad
        if random.random() < 0.005 and self.mostrar_mensaje_timer <= 0:
            self.mensaje_actual = random.choice(self.mensajes_sistema)
            self.mostrar_mensaje_timer = 120 # 2 segundos

        if self.mostrar_mensaje_timer > 0:
            self.mostrar_mensaje_timer -= 1

        # Lógica Inevitable de Muerte ante el Boss
        if self.boss.aparecido and self.boss.vida < self.boss.max_vida * 0.2:
            # El boss se vuelve invulnerable y el jugador pierde el control
            self.boss.vida = self.boss.max_vida * 0.2
            if not self.game_over:
                self.nave.vida -= 1 # Muerte lenta e inevitable
                self.shake.activar(10, 5)

        super().actualizar()

    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        
        # --- RENDERIZADO DE ADVERTENCIA FORZADA ---
        if self.mostrar_advertencia_inicial:
            # Fondo oscuro detrás
            overlay = pygame.Surface((800, 600))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(200)
            pantalla.blit(overlay, (0, 0))
            
            # Caja de Mensaje
            pygame.draw.rect(pantalla, (20, 0, 0), self.advertencia_rect, border_radius=10)
            pygame.draw.rect(pantalla, NES_RED, self.advertencia_rect, 3, border_radius=10)
            
            # Texto del Título
            t1 = self.titulo_font.render("SISTEMA CORRUPTO", True, NES_RED)
            pantalla.blit(t1, t1.get_rect(center=(400, 200)))
            
            # Texto de advertencia
            msg = "¿EL JUEGO PARECE ESTAR CORRUPTO. DESEAS CONTINUAR?"
            t2 = self.font_pquena.render(msg, True, NES_WHITE)
            pantalla.blit(t2, t2.get_rect(center=(400, 280)))
            
            # Botones
            mouse_pos = pygame.mouse.get_pos()
            
            # Botón Continuar
            color_c = NES_RED if self.btn_continuar.collidepoint(mouse_pos) else (100, 0, 0)
            pygame.draw.rect(pantalla, color_c, self.btn_continuar, border_radius=5)
            pygame.draw.rect(pantalla, NES_WHITE, self.btn_continuar, 2, border_radius=5)
            pantalla.blit(self.font_pquena.render("SÍ, CONTINUAR", True, NES_WHITE), 
                         self.font_pquena.render("SÍ, CONTINUAR", True, NES_WHITE).get_rect(center=self.btn_continuar.center))
            
            # Botón No Salir
            color_ns = NES_RED if self.btn_no_salir.collidepoint(mouse_pos) else (100, 0, 0)
            pygame.draw.rect(pantalla, color_ns, self.btn_no_salir, border_radius=5)
            pygame.draw.rect(pantalla, NES_WHITE, self.btn_no_salir, 2, border_radius=5)
            pantalla.blit(self.font_pquena.render("NO SALIR", True, NES_WHITE), 
                         self.font_pquena.render("NO SALIR", True, NES_WHITE).get_rect(center=self.btn_no_salir.center))
            
            # --- VENTANA DE ERROR FAKE ---
            if self.mostrar_error_fake:
                error_rect = pygame.Rect(200, 200, 400, 200)
                pygame.draw.rect(pantalla, NES_RED, error_rect)
                pygame.draw.rect(pantalla, NES_WHITE, error_rect, 4)
                txt_err = self.font.render("ERROR CRÍTICO", True, NES_WHITE)
                pantalla.blit(txt_err, txt_err.get_rect(center=(400, 260)))
                txt_det = self.font_pquena.render("FORZANDO INICIO...", True, NES_YELLOW)
                pantalla.blit(txt_det, txt_det.get_rect(center=(400, 320)))
                
            return # Detener el dibujo del nivel mientras esté la advertencia

        # Dibujar mensajes de incomodidad (si no hay advertencia)
        if self.mostrar_mensaje_timer > 0:
            txt = self.font.render(self.mensaje_actual, True, NES_RED)
            pantalla.blit(txt, txt.get_rect(center=(400, 300)))

    def reiniciar_nivel(self):
        # Al reintentar, el menú de Game Over debe cambiar (Fase 14)
        SceneManager.cambiar_escena(NivelUnoScene(self.nombre))

    def finalizar_nivel(self):
        # Este nivel no debería poder finalizarse normalmente
        pass

    def configurar_boss(self):
        self.boss.max_vida = 300
        self.boss.vida = 300
        self.boss.tint_color = (150, 0, 0) # Rojo oscuro corrupto
        self.boss.shoot_delay = 30
