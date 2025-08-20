import pygame
# Importar módulos necesarios
from assets.colors import * # Asegúrate de tener los colores definidos en este archivo
from enemies.enemy_manager import EnemyManager
from enemies.boss import Boss

# --- Clase de la Nave ---
class Nave:
    def __init__(self, x=None, y=None):
        # Inicializa las propiedades de la nave
        # Si no se dan coordenadas, usa valores predeterminados
        self.x = x if x is not None else 400
        self.y = y if y is not None else 500
        self.velocidad = 5
        self.ancho = 40
        self.alto = 30

    def mover(self, teclas):
        # Mueve la nave basándose en las teclas presionadas
        if teclas[pygame.K_w]:  # Tecla 'W'
            self.y -= self.velocidad
        if teclas[pygame.K_s]:  # Tecla 'S'
            self.y += self.velocidad
        if teclas[pygame.K_a]:  # Tecla 'A'
            self.x -= self.velocidad
        if teclas[pygame.K_d]:  # Tecla 'D'
            self.x += self.velocidad

    def dibujar(self, pantalla):
        # Dibuja la nave como un rectángulo en la pantalla
        pygame.draw.rect(pantalla, NES_GREEN, (self.x, self.y, self.ancho, self.alto))

    # Obtiene el rectángulo de colisión de la nave. Esto es útil para detectar colisiones con otros objetos.
    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

# --- Clase de la Escena del Nivel Uno ---
class NivelUnoScene:
    def __init__(self, nombre_jugador):
        # Inicializa la escena del nivel
        self.nombre = nombre_jugador
        # Carga las fuentes necesarias.
        self.font = pygame.font.Font("assets/fonts/upheavtt.ttf", 36)
        self.titulo_font = pygame.font.Font("assets/fonts/upheavtt.ttf", 64)
        
        # Define las dimensiones de la pantalla y el centro
        self.ancho_pantalla = 800
        self.alto_pantalla = 600
        self.centro_x = self.ancho_pantalla // 2
        self.centro_y = self.alto_pantalla // 2

        # Crea una instancia de la nave del jugador
        self.nave = Nave()
        self.pausa = False  # Variable para controlar el estado de pausa

        # Define las propiedades del botón de pausa (rectángulo y color)
        self.boton_rect = pygame.Rect(0, 0, 240, 60)
        self.boton_color = NES_BLUE

        # Inicializa el gestor de enemigos y el jefe
        self.enemy_manager = EnemyManager()
        self.boss = Boss()
        self.contador_frames = 0  # Contador para gestionar eventos temporizados (como la aparición del jefe)

    def manejar_eventos(self, eventos, pantalla):
        # Procesa los eventos de entrada del usuario
        for event in eventos:
            if event.type == pygame.QUIT:
                # Si el usuario cierra la ventana, el juego termina
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Si se presiona ESC, se activa/desactiva la pausa
                    self.pausa = not self.pausa  # Cambia el estado de pausa
                # Los siguientes movimientos se gestionan con la lógica de las teclas presionadas
                # y no con eventos, por lo que el siguiente código de movimiento es redundante.
                # Se puede eliminar para evitar conflictos.
                # ⭐ Este bloque se puede simplificar o eliminar si el movimiento se maneja solo en 'actualizar'
                if not self.pausa:
                    if event.key == pygame.K_w:
                        self.nave.y -= 10
                    elif event.key == pygame.K_s:
                        self.nave.y += 10
                    elif event.key == pygame.K_a:
                        self.nave.x -= 10
                    elif event.key == pygame.K_d:
                        self.nave.x += 10

    def actualizar(self):
        # Lógica del juego que se ejecuta en cada fotograma
        if not self.pausa:
            teclas = pygame.key.get_pressed()  # Obtiene un diccionario con el estado de todas las teclas
            self.nave.mover(teclas)  # Llama al método mover de la nave
            self.contador_frames += 1
            self.enemy_manager.actualizar()  # Actualiza la lógica de los enemigos
            
            # Colision de enemigos
            self.nave_rect = self.nave.obtener_rect()
            enemigos_a_eliminar = []

            for enemigo in self.enemy_manager.enemigos:
                enemigo_rect = enemigo.obtener_rect()
                # .colliderect() comprueba si dos rectángulos se superponen
                # si la nave colisiona con el jugador
                if self.nave_rect.colliderect(enemigo_rect):
                    print("¡Colisión detectada! La nave del jugador ha chocado con un enemigo.")
                    # Ocultar la nave del jugador para simular que explotó.
                    # Una forma simple es moverla fuera de la pantalla.
                    self.nave.x = 400
                    self.nave.y = 500

                    enemigos_a_eliminar.append(enemigo)
            # Elimina los enemigos que han colisionado
            for enemigo in enemigos_a_eliminar:
                if enemigo in self.enemy_manager.enemigos:
                    self.enemy_manager.enemigos.remove(enemigo)

            # Colision con el jefe
            if self.boss.aparecido:
                boss_rect = self.boss.obtener_rect()
                if self.nave_rect.colliderect(boss_rect):
                    print("¡Colisión detectada! La nave del jugador ha chocado con el jefe.")
                    self.nave.x = 400
                    self.nave.y = 500

            # Si han pasado 1200 frames (aproximadamente 20 segundos a 60 FPS), el jefe aparece
            if self.contador_frames == 1200:
                self.boss.aparecer()
            
            self.boss.mover()  # Mueve al jefe

    def dibujar(self, pantalla):
        # Dibuja todos los elementos en la pantalla
        if self.pausa:
            # Si el juego está en pausa, muestra el menú de pausa
            self.mostrar_menu_pausa(pantalla)
        else:
            # Si no está en pausa, dibuja el juego normal
            pantalla.fill(NES_BLACK) # Rellena el fondo
            
            # Dibuja el título del nivel
            titulo = self.titulo_font.render("Nivel 1", True, NES_GREEN)
            titulo_rect = titulo.get_rect(center=(self.centro_x, 100))
            pantalla.blit(titulo, titulo_rect)
            
            # Llama a los métodos de dibujo de la nave y los enemigos
            self.nave.dibujar(pantalla)
            self.enemy_manager.dibujar(pantalla)
            self.boss.dibujar(pantalla)

    def dibujar_fondo_congelado(self, pantalla):
        # Dibuja el estado del juego para mostrarlo detrás del menú de pausa
        pantalla.fill(NES_BLACK)
        titulo = self.titulo_font.render("Nivel 1", True, NES_GREEN)
        pantalla.blit(titulo, titulo.get_rect(center=(self.centro_x, 100)))
        self.nave.dibujar(pantalla)

    def mostrar_menu_pausa(self, pantalla):
        # Lógica para dibujar el menú de pausa
        self.dibujar_fondo_congelado(pantalla)
        
        # Dibuja una capa semi-transparente sobre el juego
        overlay = pygame.Surface((self.ancho_pantalla, self.alto_pantalla), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Color negro con 180 de transparencia (de 0 a 255)
        pantalla.blit(overlay, (0, 0))
        
        # Dibuja el texto de "PAUSA"
        pausa_texto = self.font.render("PAUSA", True, NES_RED)
        pausa_rect = pausa_texto.get_rect(center=(self.centro_x, self.centro_y - 100))
        pantalla.blit(pausa_texto, pausa_rect)
        
        # Dibuja y gestiona el botón "Jugar"
        jugar_rect = pygame.Rect(0, 0, 240, 60)
        jugar_rect.center = (self.centro_x, self.centro_y - 20)
        mouse_pos = pygame.mouse.get_pos()
        color_borde_jugar = NES_ORANGE if jugar_rect.collidepoint(mouse_pos) else NES_GREEN
        pygame.draw.rect(pantalla, self.boton_color, jugar_rect, border_radius=10)
        pygame.draw.rect(pantalla, color_borde_jugar, jugar_rect, 4, border_radius=10)
        texto_jugar = self.font.render("Jugar", True, NES_WHITE)
        pantalla.blit(texto_jugar, texto_jugar.get_rect(center=jugar_rect.center))
        
        # Dibuja y gestiona el botón "Volver"
        self.boton_rect.center = (self.centro_x, self.centro_y + 60)
        color_borde_volver = NES_ORANGE if self.boton_rect.collidepoint(mouse_pos) else NES_GREEN
        pygame.draw.rect(pantalla, self.boton_color, self.boton_rect, border_radius=10)
        pygame.draw.rect(pantalla, color_borde_volver, self.boton_rect, 4, border_radius=10)
        texto_volver = self.font.render("Volver", True, NES_WHITE)
        pantalla.blit(texto_volver, texto_volver.get_rect(center=self.boton_rect.center))
        
        # Manejo de los clics del mouse
        if pygame.mouse.get_pressed()[0]:  # Comprueba si el botón izquierdo del ratón está presionado
            if jugar_rect.collidepoint(mouse_pos):
                self.pausa = False  # Reanuda el juego
            elif self.boton_rect.collidepoint(mouse_pos):
                from engine.scene_manager import SceneManager
                from scenes.select_level import SelectLevelScene
                # Vuelve a la pantalla de selección de nivel
                SceneManager.cambiar_escena(SelectLevelScene(self.nombre))