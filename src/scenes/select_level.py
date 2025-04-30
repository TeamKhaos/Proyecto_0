# src/scenes/select_level.py
import pygame

def pantalla_select_level(pantalla):
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render("Pantalla de selección de nivel", True, (255, 255, 255))
    pantalla.fill((100, 0, 100))
    pantalla.blit(texto, (100, 250))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
                pygame.quit()
                return
