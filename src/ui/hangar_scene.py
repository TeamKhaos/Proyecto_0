import pygame
from assets.colors import *
from engine.asset_manager import AssetManager
from engine.progreso_manager import cargar_progreso, seleccionar_nave
from engine.audio_manager import AudioManager
from engine.player import Nave

class HangarScene:
    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador
        self.progreso = cargar_progreso()
        
        self.font = AssetManager.get_font("assets/fonts/upheavtt.ttf", 36)
        self.font_pquena = AssetManager.get_font("assets/fonts/upheavtt.ttf", 20)
        self.titulo_font = AssetManager.get_font("assets/fonts/upheavtt.ttf", 64)

        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        
        self.opciones_naves = ["default", "mejora1", "mejora2", "mejora3"]
        self.indice_actual = self.opciones_naves.index(self.progreso.get("nave_seleccionada", "default"))
        
        # Pre-cargar naves para visualización
        self.naves_visuales = {skin: Nave(x=self.centro_x - 32, y=250, skin=skin) for skin in self.opciones_naves}
        
        # Estrellas de fondo
        from engine.background import ParallaxManager
        self.parallax = ParallaxManager(800, 600)

    def manejar_eventos(self, eventos, pantalla):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pos = event.pos
                    
                    # Botón Izquierda
                    btn_izq = pygame.Rect(self.centro_x - 150, 260, 40, 40)
                    if btn_izq.collidepoint(mouse_pos):
                        AudioManager.play_boton()
                        self.indice_actual = (self.indice_actual - 1) % len(self.opciones_naves)
                    
                    # Botón Derecha
                    btn_der = pygame.Rect(self.centro_x + 110, 260, 40, 40)
                    if btn_der.collidepoint(mouse_pos):
                        AudioManager.play_boton()
                        self.indice_actual = (self.indice_actual + 1) % len(self.opciones_naves)
                        
                    # Botón Seleccionar
                    skin_actual = self.opciones_naves[self.indice_actual]
                    if skin_actual in self.progreso["naves_desbloqueadas"]:
                        btn_sel = pygame.Rect(0, 0, 280, 60)
                        btn_sel.center = (self.centro_x, 400)
                        if btn_sel.collidepoint(mouse_pos):
                            AudioManager.play_boton()
                            seleccionar_nave(skin_actual)
                            self.progreso = cargar_progreso() # Recargar
                    
                    # Botón Volver
                    btn_volver = pygame.Rect(0, 0, 280, 60)
                    btn_volver.center = (self.centro_x, 500)
                    if btn_volver.collidepoint(mouse_pos):
                        AudioManager.play_boton()
                        from engine.scene_manager import SceneManager
                        from ui.pantalla_principal import PantallaPrincipalScene
                        SceneManager.cambiar_escena(PantallaPrincipalScene(self.nombre))

    def actualizar(self):
        self.parallax.actualizar()

    def dibujar(self, pantalla):
        pantalla.fill(NES_BLACK)
        self.parallax.dibujar(pantalla)
        
        txt_titulo = self.titulo_font.render("HANGAR", True, NES_WHITE)
        pantalla.blit(txt_titulo, txt_titulo.get_rect(center=(self.centro_x, 80)))
        
        skin_actual = self.opciones_naves[self.indice_actual]
        desbloqueada = skin_actual in self.progreso["naves_desbloqueadas"]
        seleccionada = self.progreso["nave_seleccionada"] == skin_actual
        
        # Dibujar Nave
        nave_obj = self.naves_visuales[skin_actual]
        if not desbloqueada:
            # Dibujar silueta o con filtro gris
            s = nave_obj.frames[1].copy()
            s.fill((50, 50, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
            pantalla.blit(s, (nave_obj.x, nave_obj.y))
            txt_lock = self.font_pquena.render("BLOQUEADA", True, NES_RED)
            pantalla.blit(txt_lock, txt_lock.get_rect(center=(self.centro_x, 330)))
        else:
            nave_obj.dibujar(pantalla)
            txt_name = self.font_pquena.render(f"NAVE: {skin_actual.upper()}", True, NES_GREEN)
            pantalla.blit(txt_name, txt_name.get_rect(center=(self.centro_x, 330)))

        # Flechas
        pygame.draw.polygon(pantalla, NES_WHITE, [(self.centro_x - 150, 280), (self.centro_x - 110, 260), (self.centro_x - 110, 300)])
        pygame.draw.polygon(pantalla, NES_WHITE, [(self.centro_x + 150, 280), (self.centro_x + 110, 260), (self.centro_x + 110, 300)])
        
        # Botón Seleccionar
        if desbloqueada:
            color = NES_ORANGE if seleccionada else NES_BLUE
            texto = "SELECCIONADA" if seleccionada else "SELECCIONAR"
            self.dibujar_boton(pantalla, texto, 400, color)
        else:
            self.dibujar_boton(pantalla, "COMPLETA NIVELES", 400, NES_GRAY)

        # Botón Volver
        self.dibujar_boton(pantalla, "VOLVER AL MENU", 500, NES_BLUE)

    def dibujar_boton(self, pantalla, texto, y_centro, color_base):
        rect = pygame.Rect(0, 0, 280, 60); rect.center = (self.centro_x, y_centro)
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        color = NES_LIGHT_BLUE if hover else color_base
        pygame.draw.rect(pantalla, color, rect, border_radius=10)
        if hover: pygame.draw.rect(pantalla, NES_WHITE, rect, 3, border_radius=10)
        t = self.font_pquena.render(texto, True, NES_WHITE)
        pantalla.blit(t, t.get_rect(center=rect.center))
