import pygame
import random
import math
from enemies.bala import Bala
from assets.colors import * 
from enemies.enemy_manager import EnemyManager
from enemies.boss import Boss
from engine.progreso_manager import completar_nivel_3
from engine.particle_system import ParticleManager
from engine.audio_manager import AudioManager
from engine.powerup import PowerUp

class Estrella:
    def __init__(self, x, y, velocidad, tamano, color):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.tamano = tamano
        self.color = color

    def mover(self, alto_pantalla):
        self.y += self.velocidad
        if self.y > alto_pantalla:
            self.y = 0
            self.x = random.randint(0, 800)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.tamano)

class ParallaxManager:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.capas = []
        # Rojo/Fuego para Nivel 3
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(0.1, 0.5), 1, NES_GRAY) for _ in range(120)])
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(0.6, 1.2), 2, NES_ORANGE) for _ in range(60)])
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(1.5, 2.5), 3, NES_RED) for _ in range(25)])

    def actualizar(self):
        for capa in self.capas:
            for estrella in capa:
                estrella.mover(self.alto)

    def dibujar(self, pantalla):
        for capa in self.capas:
            for estrella in capa:
                estrella.dibujar(pantalla)

class Nave:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else 368 
        self.y = y if y is not None else 500
        self.velocidad = 7
        self.ancho = 64
        self.alto = 64
        self.vida = 100
        self.max_vida = 100
        self.powerup_escopeta = False
        self.timer_powerup = 0
        self.tiempo_creacion = pygame.time.get_ticks()

        self.frames = []
        try:
            for i in range(1, 4):
                img = pygame.image.load(f"assets/images/player/nave_default{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (self.ancho, self.alto))
                self.frames.append(img)
        except pygame.error:
            self.frames = [None]

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0: self.vida = 0

    def mover(self, teclas):
        if teclas[pygame.K_w] and self.y > 0: self.y -= self.velocidad
        if teclas[pygame.K_s] and self.y < 600 - self.alto: self.y += self.velocidad
        if teclas[pygame.K_a] and self.x > 0: self.x -= self.velocidad
        if teclas[pygame.K_d] and self.x < 800 - self.ancho: self.x += self.velocidad
        
        if self.powerup_escopeta:
            self.timer_powerup -= 1
            if self.timer_powerup <= 0:
                self.powerup_escopeta = False

    def dibujar(self, pantalla):
        if self.frames[0]:
            tiempo_actual = pygame.time.get_ticks()
            frame_actual = 0 if tiempo_actual - self.tiempo_creacion < 1500 else (2 if any(pygame.key.get_pressed()) else 1)
            
            # Efecto visual si tiene powerup
            if self.powerup_escopeta and (pygame.time.get_ticks() // 100) % 2 == 0:
                s = self.frames[frame_actual].copy()
                s.fill((0, 255, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
                pantalla.blit(s, (self.x, self.y))
            else:
                pantalla.blit(self.frames[frame_actual], (self.x, self.y))
        else:
            pygame.draw.rect(pantalla, NES_GREEN if not self.powerup_escopeta else NES_WHITE, (self.x, self.y, self.ancho, self.alto))

    def obtener_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, self.ancho - 20, self.alto - 20)

class NivelTresScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
        self.font_pquena = pygame.font.Font("assets/fonts/upheavtt.ttf", 20)
        self.font_mini = pygame.font.Font("assets/fonts/upheavtt.ttf", 16)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 64)
        
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        self.centro_y = self.alto_pantalla // 2

        self.nave = Nave()
        self.pausa = False
        self.balas_jugador = []  
        self.balas_enemigas = []
        self.powerups = []

        self.enemy_manager = EnemyManager(nivel=3, target=self.nave)
        self.boss = Boss(target=self.nave)
        self.boss.vida = 350
        self.boss.max_vida = 350
        self.boss.shoot_delay = 30 
        
        self.parallax = ParallaxManager(self.ancho_pantalla, self.alto_pantalla)
        self.particle_manager = ParticleManager()
        self.victoria = False
        self.game_over = False
        
        AudioManager.play_music("audio.mp3")

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
            from engine.scene_manager import SceneManager; from scenes.select_level import SelectLevelScene
            SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

    def manejar_game_over_clic(self, pos):
        reintentar_rect = pygame.Rect(0, 0, 280, 60); reintentar_rect.center = (self.centro_x, self.centro_y)
        menu_rect = pygame.Rect(0, 0, 280, 60); menu_rect.center = (self.centro_x, self.centro_y + 80)
        from engine.scene_manager import SceneManager
        if reintentar_rect.collidepoint(pos):
            AudioManager.play_boton(); SceneManager.cambiar_escena(NivelTresScene(self.nombre))
        elif menu_rect.collidepoint(pos):
            AudioManager.play_boton(); from scenes.select_level import SelectLevelScene
            SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

    def manejar_victoria_clic(self, pos):
        btn_menu = pygame.Rect(0, 0, 280, 60); btn_menu.center = (self.centro_x, self.centro_y + 80)
        if btn_menu.collidepoint(pos):
            AudioManager.play_boton()
            from engine.scene_manager import SceneManager; from scenes.select_level import SelectLevelScene
            SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

    def disparar(self):
        cx = self.nave.x + self.nave.ancho // 2
        cy = self.nave.y
        if self.nave.powerup_escopeta:
            # Disparo triple
            self.balas_jugador.append(Bala(cx, cy, vx=0, vy=-8, color=NES_GREEN))
            self.balas_jugador.append(Bala(cx, cy, vx=-2, vy=-7, color=NES_GREEN))
            self.balas_jugador.append(Bala(cx, cy, vx=2, vy=-7, color=NES_GREEN))
        else:
            self.balas_jugador.append(Bala(cx, cy, direccion=-1, color=NES_YELLOW))
        AudioManager.play_disparo()

    def dibujar_barra_vida(self, pantalla, x, y, ancho, alto, vida, max_vida, color_barra):
        pygame.draw.rect(pantalla, NES_WHITE, (x - 2, y - 2, ancho + 4, alto + 4), 2)
        ancho_actual = (vida / max_vida) * ancho if max_vida > 0 else 0
        pygame.draw.rect(pantalla, color_barra, (x, y, ancho_actual, alto))

    def actualizar(self):
        if self.pausa or self.victoria or self.game_over: return

        self.parallax.actualizar()

        if self.boss.derrotado:
            completar_nivel_3()
            self.victoria = True
            return
        
        if self.nave.vida <= 0:
            self.game_over = True
            return

        self.nave.mover(pygame.key.get_pressed())
        
        status, nuevas_balas = self.enemy_manager.actualizar()
        self.balas_enemigas.extend(nuevas_balas)

        if status == "BOSS_TIME" and not self.boss.aparecido:
            self.boss.aparecer()

        if self.boss.aparecido:
            self.boss.mover()
            if self.boss.puede_disparar():
                self.balas_enemigas.extend(self.boss.disparar())

        for b in self.balas_jugador: b.mover()
        for b in self.balas_enemigas: b.mover()
        for p in self.powerups: p.mover()

        self.particle_manager.actualizar()

        # --- Colisiones Balas ---
        balas_j_eliminar = []
        for b in self.balas_jugador:
            if self.boss.aparecido and b.obtener_rect().colliderect(self.boss.obtener_rect()):
                self.boss.recibir_dano(2)
                self.particle_manager.crear_explosion(b.x, b.y, cantidad=5)
                AudioManager.play_explosion(); balas_j_eliminar.append(b)
                continue
            for e in self.enemy_manager.enemigos:
                if b.obtener_rect().colliderect(e.obtener_rect()):
                    self.particle_manager.crear_explosion(e.x + e.ancho//2, e.y + e.alto//2, cantidad=20)
                    AudioManager.play_explosion()
                    # Drop raro de Power-up (10%)
                    if random.random() < 0.10:
                        self.powerups.append(PowerUp(e.x, e.y))
                    self.enemy_manager.enemigos.remove(e)
                    balas_j_eliminar.append(b); break
        
        self.balas_jugador = [b for b in self.balas_jugador if b not in balas_j_eliminar and -10 < b.y < 610]
        
        # Colisiones Nave vs Powerups
        for p in self.powerups[:]:
            if self.nave.obtener_rect().colliderect(p.obtener_rect()):
                self.nave.powerup_escopeta = True
                self.nave.timer_powerup = 600 # 10 segundos a 60 fps
                self.powerups.remove(p)
                AudioManager.play_boton() # Sonido feedback

        balas_e_eliminar = []
        nave_rect = self.nave.obtener_rect()
        for b in self.balas_enemigas:
            if b.obtener_rect().colliderect(nave_rect):
                self.nave.recibir_dano(10) 
                self.particle_manager.crear_explosion(b.x, b.y, color=NES_LIGHT_BLUE, cantidad=10)
                AudioManager.play_explosion(); balas_e_eliminar.append(b)
        
        self.balas_enemigas = [b for b in self.balas_enemigas if b not in balas_e_eliminar and -50 < b.y < 650 and -50 < b.x < 850]

    def dibujar(self, pantalla):
        if self.pausa: self.mostrar_menu_pausa(pantalla); return

        pantalla.fill(NES_BLACK)
        self.parallax.dibujar(pantalla)
        
        self.dibujar_ui(pantalla)
        self.nave.dibujar(pantalla)
        self.enemy_manager.dibujar(pantalla)
        self.boss.dibujar(pantalla)

        for b in self.balas_jugador: b.dibujar(pantalla)
        for b in self.balas_enemigas: b.dibujar(pantalla)
        for p in self.powerups: p.dibujar(pantalla)

        self.particle_manager.dibujar(pantalla)

        if self.victoria: self.mostrar_victoria(pantalla)
        if self.game_over: self.mostrar_game_over(pantalla)

    def dibujar_ui(self, pantalla):
        pantalla.blit(self.font_pquena.render(f"HP: {self.nave.vida}", True, NES_WHITE), (20, 20))
        self.dibujar_barra_vida(pantalla, 20, 45, 200, 15, self.nave.vida, self.nave.max_vida, NES_RED)
        pantalla.blit(self.font_pquena.render(f"OLEADA: {self.enemy_manager.oleada_actual}/5", True, NES_WHITE), (620, 20))
        
        if self.nave.powerup_escopeta:
            txt = self.font_mini.render(f"ESCOPETA: {self.nave.timer_powerup // 60}s", True, NES_GREEN)
            pantalla.blit(txt, (20, 70))

        if self.boss.aparecido:
            pantalla.blit(self.font_pquena.render("SÚPER JEFE NIVEL 3", True, NES_RED), (self.centro_x - 100, 20))
            self.dibujar_barra_vida(pantalla, self.centro_x - 150, 45, 300, 20, self.boss.vida, self.boss.max_vida, NES_ORANGE)

    def mostrar_menu_pausa(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)); pantalla.blit(overlay, (0, 0))
        pausa_texto = self.font.render("PAUSA - NIVEL 3", True, NES_RED)
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
        t = self.titulo_font.render("¡NIVEL 3 COMPLETADO!", True, NES_GREEN)
        pantalla.blit(t, t.get_rect(center=(self.centro_x, self.centro_y - 100)))
        m = self.font_pquena.render("¡Has salvado la galaxia, legendario!", True, NES_WHITE)
        pantalla.blit(m, m.get_rect(center=(self.centro_x, self.centro_y - 30)))
        self.dibujar_boton(pantalla, "VOLVER AL MENU", self.centro_y + 80)
