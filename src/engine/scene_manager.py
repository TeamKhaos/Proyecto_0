import pygame

class SceneManager:
    escena_actual = None

    @classmethod
    def cambiar_escena(cls, nueva_escena):
        cls.escena_actual = nueva_escena

    @classmethod
    def manejar_eventos(cls, eventos):
        if cls.escena_actual:
            cls.escena_actual.manejar_eventos(eventos)

    @classmethod
    def actualizar(cls):
        if cls.escena_actual:
            cls.escena_actual.actualizar()

    @classmethod
    def dibujar(cls, pantalla):
        if cls.escena_actual:
            cls.escena_actual.dibujar(pantalla)
