import pygame
import random
from enemies.bala import Bala
from assets.colors import * 
from enemies.enemy_manager import EnemyManager
from enemies.boss import Boss
from engine.progreso_manager import completar_nivel_1
from engine.particle_system import ParticleManager
from engine.audio_manager import AudioManager

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
        # Capa lejana (pequeña y lenta)
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(0.1, 0.5), 1, NES_GRAY) for _ in range(80)])
        # Capa media
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(0.6, 1.2), 2, NES_WHITE) for _ in range(40)])
        # Capa cercana (más grande y rápida)
        self.capas.append([Estrella(random.randint(0, ancho), random.randint(0, alto), 
                                   random.uniform(1.5, 2.5), 3, NES_LIGHT_BLUE) for _ in range(15)])

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
        self.x = x if x is not None else 368 # Ajustado para centro con 64px
        self.y = y if y is not None else 500
        self.velocidad = 6
        self.ancho = 64
        self.alto = 64
        self.vida = 100
        self.max_vida = 100
        self.tiempo_creacion = pygame.time.get_ticks()

        # Cargar frames de animación
        self.frames = []
        try:
            for i in range(1, 4):
                img = pygame.image.load(f"assets/images/player/nave_default{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (self.ancho, self.alto))
                self.frames.append(img)
        except pygame.error:
            # Fallback si no se encuentran las imágenes
            print("Error cargando assets de la nave, usando fallback visual.")
            self.frames = [None]

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0: self.vida = 0

    def mover(self, teclas):
        if teclas[pygame.K_w] and self.y > 0: self.y -= self.velocidad
        if teclas[pygame.K_s] and self.y < 600 - self.alto: self.y += self.velocidad
        if teclas[pygame.K_a] and self.x > 0: self.x -= self.velocidad
        if teclas[pygame.K_d] and self.x < 800 - self.ancho: self.x += self.velocidad

    def dibujar(self, pantalla):
        if self.frames[0]:
            tiempo_actual = pygame.time.get_ticks()
            
            # 1. Durante el primer 1.5 segundo mostramos nave_default1 (Aparición)
            if tiempo_actual - self.tiempo_creacion < 1500:
                frame_actual = 0
            else:
                # 2. Verificar si hay alguna tecla de movimiento presionada
                teclas = pygame.key.get_pressed()
                moviendose = teclas[pygame.K_w] or teclas[pygame.K_s] or teclas[pygame.K_a] or teclas[pygame.K_d]
                
                if moviendose:
                    frame_actual = 2 # nave_default3 (Movimiento)
                else:
                    frame_actual = 1 # nave_default2 (Quieta)
            
            pantalla.blit(self.frames[frame_actual], (self.x, self.y))
        else:
            pygame.draw.rect(pantalla, NES_GREEN, (self.x, self.y, self.ancho, self.alto))

    def obtener_rect(self):
        # Reducimos un poco el hitbox para que sea más justo con el sprite circular/triangular
        return pygame.Rect(self.x + 10, self.y + 10, self.ancho - 20, self.alto - 20)

class NivelUnoScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
        self.font_pquena = pygame.font.Font("assets/fonts/upheavtt.ttf", 20)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 64)
        
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        self.centro_y = self.alto_pantalla // 2

        self.nave = Nave()
        self.pausa = False
        self.balas_jugador = []  
        self.balas_enemigas = []

        self.enemy_manager = EnemyManager()
        self.boss = Boss()
        self.parallax = ParallaxManager(self.ancho_pantalla, self.alto_pantalla)
        self.particle_manager = ParticleManager()
        self.victoria = False
        self.game_over = False
        
        self.boton_rect = pygame.Rect(0, 0, 240, 60)
        self.boton_color = NES_BLUE

        # Iniciar música de fondo
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
            
            # Lógica de botones en PAUSA, GAME OVER y VICTORIA
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pos = event.pos
                    
                    if self.pausa:
                        jugar_rect = pygame.Rect(0, 0, 240, 60)
                        jugar_rect.center = (self.centro_x, self.centro_y - 20)
                        volver_rect = pygame.Rect(0, 0, 240, 60)
                        volver_rect.center = (self.centro_x, self.centro_y + 60)

                        if jugar_rect.collidepoint(mouse_pos):
                            AudioManager.play_boton()
                            self.pausa = False
                        elif volver_rect.collidepoint(mouse_pos):
                            AudioManager.play_boton()
                            from engine.scene_manager import SceneManager
                            from scenes.select_level import SelectLevelScene
                            SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

                    elif self.game_over:
                        reintentar_rect = pygame.Rect(0, 0, 240, 60)
                        reintentar_rect.center = (self.centro_x, self.centro_y)
                        menu_rect = pygame.Rect(0, 0, 240, 60)
                        menu_rect.center = (self.centro_x, self.centro_y + 80)

                        if reintentar_rect.collidepoint(mouse_pos):
                            AudioManager.play_boton()
                            from engine.scene_manager import SceneManager
                            SceneManager.cambiar_escena(NivelUnoScene(self.nombre))
                        elif menu_rect.collidepoint(mouse_pos):
                            AudioManager.play_boton()
                            from engine.scene_manager import SceneManager
                            from scenes.select_level import SelectLevelScene
                            SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

                    elif self.victoria:
                        btn_menu = pygame.Rect(0, 0, 240, 60)
                        btn_menu.center = (self.centro_x, self.centro_y + 80)
                        if btn_menu.collidepoint(mouse_pos):
                            AudioManager.play_boton()
                            from engine.scene_manager import SceneManager
                            from scenes.select_level import SelectLevelScene
                            SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

    def disparar(self):
        nueva_bala = Bala(self.nave.x + self.nave.ancho // 2, self.nave.y, direccion=-1, color=NES_YELLOW)
        self.balas_jugador.append(nueva_bala)
        AudioManager.play_disparo()

    def dibujar_barra_vida(self, pantalla, x, y, ancho, alto, vida, max_vida, color_barra):
        pygame.draw.rect(pantalla, NES_WHITE, (x - 2, y - 2, ancho + 4, alto + 4), 2)
        ancho_actual = (vida / max_vida) * ancho if max_vida > 0 else 0
        pygame.draw.rect(pantalla, color_barra, (x, y, ancho_actual, alto))

    def mostrar_game_over(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200)) 
        pantalla.blit(overlay, (0, 0))

        texto = self.titulo_font.render("GAME OVER", True, NES_RED)
        pantalla.blit(texto, texto.get_rect(center=(self.centro_x, self.centro_y - 100)))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Botón REINTENTAR
        reintentar_rect = pygame.Rect(0, 0, 240, 60)
        reintentar_rect.center = (self.centro_x, self.centro_y)
        hover_r = reintentar_rect.collidepoint(mouse_pos)
        color_r = NES_LIGHT_BLUE if hover_r else NES_BLUE
        pygame.draw.rect(pantalla, color_r, reintentar_rect, border_radius=10)
        if hover_r: pygame.draw.rect(pantalla, NES_WHITE, reintentar_rect, 3, border_radius=10)
        pantalla.blit(self.font_pquena.render("REINTENTAR", True, NES_WHITE), 
                      self.font_pquena.render("REINTENTAR", True, NES_WHITE).get_rect(center=reintentar_rect.center))

        # Botón MENU
        menu_rect = pygame.Rect(0, 0, 240, 60)
        menu_rect.center = (self.centro_x, self.centro_y + 80)
        hover_m = menu_rect.collidepoint(mouse_pos)
        color_m = NES_LIGHT_BLUE if hover_m else NES_BLUE
        pygame.draw.rect(pantalla, color_m, menu_rect, border_radius=10)
        if hover_m: pygame.draw.rect(pantalla, NES_WHITE, menu_rect, 3, border_radius=10)
        pantalla.blit(self.font_pquena.render("VOLVER AL MENU", True, NES_WHITE), 
                      self.font_pquena.render("VOLVER AL MENU", True, NES_WHITE).get_rect(center=menu_rect.center))

    def mostrar_victoria(self, pantalla):
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        pantalla.blit(overlay, (0, 0))

        texto = self.titulo_font.render("¡VICTORIA!", True, NES_GREEN)
        pantalla.blit(texto, texto.get_rect(center=(self.centro_x, self.centro_y - 100)))
        
        mensaje = self.font_pquena.render("Felicidades haz pasado el nivel 1", True, NES_WHITE)
        pantalla.blit(mensaje, mensaje.get_rect(center=(self.centro_x, self.centro_y - 30)))

        # Botón Volver
        btn_menu = pygame.Rect(0, 0, 240, 60)
        btn_menu.center = (self.centro_x, self.centro_y + 80)
        mouse_pos = pygame.mouse.get_pos()
        hover = btn_menu.collidepoint(mouse_pos)
        color = NES_LIGHT_BLUE if hover else NES_BLUE
        pygame.draw.rect(pantalla, color, btn_menu, border_radius=10)
        if hover: pygame.draw.rect(pantalla, NES_WHITE, btn_menu, 3, border_radius=10)
        
        texto_volver = self.font_pquena.render("VOLVER AL MENU", True, NES_WHITE)
        pantalla.blit(texto_volver, texto_volver.get_rect(center=btn_menu.center))

    def actualizar(self):
        if self.pausa or self.victoria or self.game_over: return

        self.parallax.actualizar()

        if self.boss.derrotado:
            completar_nivel_1()
            self.victoria = True
            return
        
        if self.nave.vida <= 0:
            self.game_over = True
            return

        teclas = pygame.key.get_pressed()
        self.nave.mover(teclas)
        
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

        self.particle_manager.actualizar()

        # Colisiones: Balas Jugador -> Enemigos/Jefe
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
                    self.enemy_manager.enemigos.remove(e)
                    balas_j_eliminar.append(b)
                    break
        
        self.balas_jugador = [b for b in self.balas_jugador if b not in balas_j_eliminar and b.y > -10]

        # Colisiones: Balas Enemigas -> Nave
        balas_e_eliminar = []
        nave_rect = self.nave.obtener_rect()
        for b in self.balas_enemigas:
            if b.obtener_rect().colliderect(nave_rect):
                self.nave.recibir_dano(5)
                self.particle_manager.crear_explosion(b.x, b.y, color=NES_LIGHT_BLUE, cantidad=10)
                AudioManager.play_explosion()
                balas_e_eliminar.append(b)
        
        self.balas_enemigas = [b for b in self.balas_enemigas if b not in balas_e_eliminar and b.y < 610]

        # Colisiones: Nave -> Enemigos
        enemigos_eliminar = []
        for e in self.enemy_manager.enemigos:
            if nave_rect.colliderect(e.obtener_rect()):
                self.nave.recibir_dano(20)
                self.particle_manager.crear_explosion(e.x + e.ancho//2, e.y + e.alto//2, cantidad=30)
                AudioManager.play_explosion() # Sonido al chocar con naves
                enemigos_eliminar.append(e)
        
        for e in enemigos_eliminar:
            if e in self.enemy_manager.enemigos: self.enemy_manager.enemigos.remove(e)

    def dibujar(self, pantalla):
        if self.pausa:
            self.mostrar_menu_pausa(pantalla)
            return

        pantalla.fill(NES_BLACK)
        self.parallax.dibujar(pantalla)
        
        # --- UI ---
        texto_vida = self.font_pquena.render(f"HP: {self.nave.vida}", True, NES_WHITE)
        pantalla.blit(texto_vida, (20, 20))
        self.dibujar_barra_vida(pantalla, 20, 45, 200, 15, self.nave.vida, self.nave.max_vida, NES_RED)

        texto_wave = self.font_pquena.render(f"OLEADA: {self.enemy_manager.oleada_actual}", True, NES_WHITE)
        pantalla.blit(texto_wave, (650, 20))

        if self.boss.aparecido:
            texto_boss = self.font_pquena.render("JEFE MAESTRO", True, NES_RED)
            pantalla.blit(texto_boss, (self.centro_x - 60, 20))
            self.dibujar_barra_vida(pantalla, self.centro_x - 150, 45, 300, 20, self.boss.vida, self.boss.max_vida, NES_ORANGE)

        # --- Entidades ---
        self.nave.dibujar(pantalla)
        self.enemy_manager.dibujar(pantalla)
        self.boss.dibujar(pantalla)

        for b in self.balas_jugador: b.dibujar(pantalla)
        for b in self.balas_enemigas: b.dibujar(pantalla)

        self.particle_manager.dibujar(pantalla)

        if self.victoria: self.mostrar_victoria(pantalla)
        if self.game_over: self.mostrar_game_over(pantalla)

    def dibujar_fondo_congelado(self, pantalla):
        pantalla.fill(NES_BLACK)
        self.parallax.dibujar(pantalla)
        self.nave.dibujar(pantalla)
        self.enemy_manager.dibujar(pantalla)
        self.boss.dibujar(pantalla)

    def mostrar_menu_pausa(self, pantalla):
        self.dibujar_fondo_congelado(pantalla)
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0, 0))
        
        pausa_texto = self.font.render("PAUSA", True, NES_RED)
        pantalla.blit(pausa_texto, pausa_texto.get_rect(center=(self.centro_x, self.centro_y - 100)))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Botón Jugar
        jugar_rect = pygame.Rect(0, 0, 240, 60)
        jugar_rect.center = (self.centro_x, self.centro_y - 20)
        hover_j = jugar_rect.collidepoint(mouse_pos)
        color_j = NES_LIGHT_BLUE if hover_j else NES_BLUE
        pygame.draw.rect(pantalla, color_j, jugar_rect, border_radius=10)
        if hover_j: pygame.draw.rect(pantalla, NES_WHITE, jugar_rect, 3, border_radius=10)
        texto_jugar = self.font.render("Jugar", True, NES_WHITE)
        pantalla.blit(texto_jugar, texto_jugar.get_rect(center=jugar_rect.center))
        
        # Botón Volver
        volver_rect = pygame.Rect(0, 0, 240, 60)
        volver_rect.center = (self.centro_x, self.centro_y + 60)
        hover_v = volver_rect.collidepoint(mouse_pos)
        color_v = NES_LIGHT_BLUE if hover_v else NES_BLUE
        pygame.draw.rect(pantalla, color_v, volver_rect, border_radius=10)
        if hover_v: pygame.draw.rect(pantalla, NES_WHITE, volver_rect, 3, border_radius=10)
        texto_volver = self.font.render("Volver", True, NES_WHITE)
        pantalla.blit(texto_volver, texto_volver.get_rect(center=volver_rect.center))
