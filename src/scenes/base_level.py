import pygame
import random
import math
from assets.colors import *
from engine.player import Nave
from engine.background import ParallaxManager
from engine.particle_system import ParticleManager
from engine.audio_manager import AudioManager
from engine.asset_manager import AssetManager
from engine.powerup import PowerUp
from engine.visual_effects import ScreenShake, HealthBar
from enemies.bala import Bala, BalaGranada
from enemies.enemy_manager import EnemyManager
from enemies.boss import Boss

class BaseLevelScene:
    def __init__(self, nombre_jugador, nivel, meta_oleadas, bg_esquema="default"):
        self.nombre = nombre_jugador
        self.nivel = nivel
        self.meta_oleadas = meta_oleadas
        
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        self.centro_y = self.alto_pantalla // 2

        # Efectos Visuales
        self.shake = ScreenShake()
        self.hb_jugador = HealthBar(20, 45, 200, 15, NES_RED)
        self.hb_boss = HealthBar(self.centro_x - 150, 45, 300, 20, NES_ORANGE)

        # Fuentes (Optimizado con AssetManager)
        self.font = AssetManager.get_font("assets/fonts/upheavtt.ttf", 36)
        self.font_pquena = AssetManager.get_font("assets/fonts/upheavtt.ttf", 20)
        self.font_mini = AssetManager.get_font("assets/fonts/upheavtt.ttf", 16)
        self.titulo_font = AssetManager.get_font("assets/fonts/upheavtt.ttf", 64)

        # Cargar skin seleccionada desde el progreso
        from engine.progreso_manager import cargar_progreso
        progreso = cargar_progreso()
        self.nave = Nave(skin=progreso.get("nave_seleccionada", "default"))
        
        self.pausa = False
        self.victoria = False
        self.game_over = False
        
        self.balas_jugador = []
        self.balas_enemigas = []
        self.powerups = []

        self.enemy_manager = EnemyManager(nivel=self.nivel, target=self.nave)
        self.boss = Boss(target=self.nave)
        self.configurar_boss()

        self.parallax = ParallaxManager(self.ancho_pantalla, self.alto_pantalla, bg_esquema)
        self.particle_manager = ParticleManager()
        
        # Estadísticas para Logros
        self.tiempo_inicio = pygame.time.get_ticks()
        self.dano_recibido_total = 0
        self.enemigos_derrotados = 0

        AudioManager.play_music("audio.mp3")

    def configurar_boss(self):
        if self.nivel == 1:
            self.boss.vida = 100
            self.boss.max_vida = 100
        elif self.nivel == 2:
            self.boss.vida = 200
            self.boss.max_vida = 200
            self.boss.shoot_delay = 40
        elif self.nivel == 3:
            self.boss.vida = 350
            self.boss.max_vida = 350
            self.boss.shoot_delay = 30

    def manejar_eventos(self, eventos, pantalla):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pausa = not self.pausa
                elif event.key == pygame.K_j and not self.pausa and not self.victoria and not self.game_over:
                    self.disparar()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pos = event.pos
                    if self.pausa: self.manejar_pausa_clic(mouse_pos)
                    elif self.game_over: self.manejar_game_over_clic(mouse_pos)
                    elif self.victoria: self.manejar_victoria_clic(mouse_pos)

    def manejar_pausa_clic(self, pos):
        jugar_rect = pygame.Rect(0, 0, 280, 60); jugar_rect.center = (self.centro_x, self.centro_y - 20)
        volver_rect = pygame.Rect(0, 0, 280, 60); volver_rect.center = (self.centro_x, self.centro_y + 60)
        if jugar_rect.collidepoint(pos):
            AudioManager.play_boton(); self.pausa = False
        elif volver_rect.collidepoint(pos):
            AudioManager.play_boton()
            self.volver_al_menu()

    def manejar_game_over_clic(self, pos):
        reintentar_rect = pygame.Rect(0, 0, 280, 60); reintentar_rect.center = (self.centro_x, self.centro_y)
        menu_rect = pygame.Rect(0, 0, 280, 60); menu_rect.center = (self.centro_x, self.centro_y + 80)
        if reintentar_rect.collidepoint(pos):
            AudioManager.play_boton(); self.reiniciar_nivel()
        elif menu_rect.collidepoint(pos):
            AudioManager.play_boton(); self.volver_al_menu()

    def manejar_victoria_clic(self, pos):
        btn_menu = pygame.Rect(0, 0, 280, 60); btn_menu.center = (self.centro_x, self.centro_y + 80)
        if btn_menu.collidepoint(pos):
            AudioManager.play_boton()
            self.finalizar_nivel()

    def disparar(self):
        cx = self.nave.x + self.nave.ancho // 2
        cy = self.nave.y
        if self.nave.powerup_escopeta:
            self.balas_jugador.append(Bala(cx, cy, vx=0, vy=-8, color=NES_GREEN))
            self.balas_jugador.append(Bala(cx, cy, vx=-2, vy=-7, color=NES_GREEN))
            self.balas_jugador.append(Bala(cx, cy, vx=2, vy=-7, color=NES_GREEN))
        else:
            self.balas_jugador.append(Bala(cx, cy, direccion=-1, color=NES_YELLOW))
        AudioManager.play_disparo()

    def actualizar(self):
        if self.pausa or self.victoria or self.game_over: return

        self.parallax.actualizar()
        self.shake.actualizar()

        if self.boss.derrotado:
            self.completar_nivel_logica()
            self.victoria = True
            self.shake.activar(30, 8)
            return
        
        if self.nave.vida <= 0:
            self.game_over = True
            self.shake.activar(20, 5)
            return

        self.nave.mover(pygame.key.get_pressed())
        
        status, nuevas_balas = self.enemy_manager.actualizar()
        self.balas_enemigas.extend(nuevas_balas)

        if status == "BOSS_TIME" and not self.boss.aparecido:
            self.boss.aparecer()
            self.shake.activar(15, 3)

        if self.boss.aparecido:
            self.boss.mover()
            self.hb_boss.actualizar(self.boss.vida, self.boss.max_vida)
            tipo_disparo = self.boss.puede_disparar()
            if tipo_disparo:
                self.balas_enemigas.extend(self.boss.disparar(tipo_disparo))

        self.hb_jugador.actualizar(self.nave.vida, self.nave.max_vida)

        # Mover balas y manejar granadas
        balas_a_fragmentar = []
        for b in self.balas_enemigas:
            if isinstance(b, BalaGranada):
                if b.mover(): # Retorna True si explota
                    balas_a_fragmentar.append(b)
            else:
                b.mover()
        
        # Procesar explosiones de granadas
        for bg in balas_a_fragmentar:
            self.particle_manager.crear_explosion(bg.x, bg.y, color=NES_ORANGE, cantidad=50)
            self.shake.activar(15, 6)
            # Generar fragmentos en todas las direcciones (Círculo completo)
            for angulo in range(0, 360, 20):
                rad = math.radians(angulo)
                self.balas_enemigas.append(Bala(bg.x, bg.y, vx=math.cos(rad)*5, vy=math.sin(rad)*5, color=NES_YELLOW))
            if bg in self.balas_enemigas: self.balas_enemigas.remove(bg)

        for b in self.balas_jugador: b.mover()
        for p in self.powerups: p.mover()

        self.particle_manager.actualizar()
        self.resolver_colisiones()

    def resolver_colisiones(self):
        balas_j_eliminar = []
        for b in self.balas_jugador:
            if self.boss.aparecido and b.obtener_rect().colliderect(self.boss.obtener_rect()):
                self.boss.recibir_dano(2)
                self.particle_manager.crear_explosion(b.x, b.y, cantidad=5)
                AudioManager.play_explosion()
                balas_j_eliminar.append(b)
                continue
            for e in self.enemy_manager.enemigos:
                if b.obtener_rect().colliderect(e.obtener_rect()):
                    self.particle_manager.crear_explosion(e.x + e.ancho//2, e.y + e.alto//2, cantidad=20)
                    AudioManager.play_explosion()
                    if self.nivel == 3 and random.random() < 0.10:
                        self.powerups.append(PowerUp(e.x, e.y))
                    self.enemy_manager.enemigos.remove(e)
                    self.enemigos_derrotados += 1
                    balas_j_eliminar.append(b)
                    break
        self.balas_jugador = [b for b in self.balas_jugador if b not in balas_j_eliminar and -10 < b.y < 610]

        balas_e_eliminar = []
        nave_rect = self.nave.obtener_rect()
        dano_bala = 5 if self.nivel == 1 else (8 if self.nivel == 2 else 10)
        for b in self.balas_enemigas:
            if b.obtener_rect().colliderect(nave_rect):
                self.nave.recibir_dano(dano_bala)
                self.dano_recibido_total += dano_bala
                self.shake.activar(10, 4)
                self.particle_manager.crear_explosion(b.x, b.y, color=NES_LIGHT_BLUE, cantidad=10)
                AudioManager.play_explosion()
                balas_e_eliminar.append(b)
        self.balas_enemigas = [b for b in self.balas_enemigas if b not in balas_e_eliminar and -50 < b.y < 650 and -50 < b.x < 850]

        dano_choque = 20 if self.nivel == 1 else 25
        for e in self.enemy_manager.enemigos[:]:
            if nave_rect.colliderect(e.obtener_rect()):
                self.nave.recibir_dano(dano_choque)
                self.dano_recibido_total += dano_choque
                self.shake.activar(15, 6)
                self.particle_manager.crear_explosion(e.x + e.ancho//2, e.y + e.alto//2, cantidad=30)
                AudioManager.play_explosion()
                self.enemy_manager.enemigos.remove(e)
                self.enemigos_derrotados += 1

        for p in self.powerups[:]:
            if nave_rect.colliderect(p.obtener_rect()):
                self.nave.powerup_escopeta = True
                self.nave.timer_powerup = 600
                self.powerups.remove(p)
                AudioManager.play_boton()

    def dibujar(self, pantalla):
        if self.pausa: self.mostrar_menu_pausa(pantalla); return

        temp_surf = pygame.Surface((self.ancho_pantalla, self.alto_pantalla))
        temp_surf.fill(NES_BLACK)
        
        self.parallax.dibujar(temp_surf)
        self.dibujar_ui(temp_surf)
        self.nave.dibujar(temp_surf)
        self.enemy_manager.dibujar(temp_surf)
        self.boss.dibujar(temp_surf)

        for b in self.balas_jugador: b.dibujar(temp_surf)
        for b in self.balas_enemigas: b.dibujar(temp_surf)
        for p in self.powerups: p.dibujar(temp_surf)

        self.particle_manager.dibujar(temp_surf)

        if self.victoria: self.mostrar_victoria(temp_surf)
        if self.game_over: self.mostrar_game_over(temp_surf)
        
        self.shake.aplicar(temp_surf)
        pantalla.blit(temp_surf, (0, 0))

    def dibujar_ui(self, pantalla):
        pantalla.blit(self.font_pquena.render(f"HP: {self.nave.vida}", True, NES_WHITE), (20, 20))
        self.hb_jugador.dibujar(pantalla)
        
        pantalla.blit(self.font_pquena.render(f"OLEADA: {self.enemy_manager.oleada_actual}/{self.meta_oleadas}", True, NES_WHITE), (620, 20))
        
        if self.nave.powerup_escopeta:
            txt = self.font_mini.render(f"ESCOPETA: {self.nave.timer_powerup // 60}s", True, NES_GREEN)
            pantalla.blit(txt, (20, 70))

        if self.boss.aparecido:
            texto_boss = "JEFE MAESTRO" if self.nivel == 1 else (f"SUPER JEFE NIVEL {self.nivel}")
            pantalla.blit(self.font_pquena.render(texto_boss, True, NES_RED), (self.centro_x - 100, 20))
            self.hb_boss.dibujar(pantalla)

    def mostrar_menu_pausa(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)); pantalla.blit(overlay, (0, 0))
        pausa_texto = self.font.render(f"PAUSA - NIVEL {self.nivel}", True, NES_RED)
        pantalla.blit(pausa_texto, pausa_texto.get_rect(center=(self.centro_x, self.centro_y - 100)))
        self.dibujar_boton(pantalla, "JUGAR", self.centro_y - 20)
        self.dibujar_boton(pantalla, "VOLVER AL MENU", self.centro_y + 60)

    def dibujar_boton(self, pantalla, texto, y_centro):
        rect = pygame.Rect(0, 0, 280, 60); rect.center = (self.centro_x, y_centro)
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        pygame.draw.rect(pantalla, NES_LIGHT_BLUE if hover else NES_BLUE, rect, border_radius=10)
        if hover: pygame.draw.rect(pantalla, NES_WHITE, rect, 3, border_radius=10)
        t = self.font_pquena.render(texto, True, NES_WHITE)
        pantalla.blit(t, t.get_rect(center=rect.center))

    def mostrar_game_over(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200)); pantalla.blit(overlay, (0, 0))
        t = self.titulo_font.render("GAME OVER", True, NES_RED)
        pantalla.blit(t, t.get_rect(center=(self.centro_x, self.centro_y - 100)))
        self.dibujar_boton(pantalla, "REINTENTAR", self.centro_y)
        self.dibujar_boton(pantalla, "VOLVER AL MENU", self.centro_y + 80)

    def mostrar_victoria(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)); pantalla.blit(overlay, (0, 0))
        txt_victoria = "¡VICTORIA!" if self.nivel == 1 else f"¡NIVEL {self.nivel} COMPLETADO!"
        t = self.titulo_font.render(txt_victoria, True, NES_GREEN)
        pantalla.blit(t, t.get_rect(center=(self.centro_x, self.centro_y - 120)))
        
        tiempo_total = (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
        from engine.progreso_manager import registrar_logro
        medalla = registrar_logro(self.nivel, tiempo_total, self.dano_recibido_total)
        
        color_medalla = NES_YELLOW if medalla == "ORO" else (NES_WHITE if medalla == "PLATA" else NES_ORANGE)
        txt_medalla = self.font.render(f"MEDALLA DE {medalla}", True, color_medalla)
        pantalla.blit(txt_medalla, txt_medalla.get_rect(center=(self.centro_x, self.centro_y - 60)))

        stats = f"Tiempo: {tiempo_total}s | Daño: {self.dano_recibido_total} | Enemigos: {self.enemigos_derrotados}"
        m = self.font_pquena.render(stats, True, NES_WHITE)
        pantalla.blit(m, m.get_rect(center=(self.centro_x, self.centro_y)))
        
        self.dibujar_boton(pantalla, "CONTINUAR", self.centro_y + 100)

    def volver_al_menu(self):
        from engine.scene_manager import SceneManager; from scenes.select_level import SelectLevelScene
        SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

    def reiniciar_nivel(self):
        pass

    def finalizar_nivel(self):
        pass

    def completar_nivel_logica(self):
        pass
