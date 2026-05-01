from scenes.base_level import BaseLevelScene
from engine.progreso_manager import completar_nivel_3
from engine.scene_manager import SceneManager

class NivelTresScene(BaseLevelScene):
    def __init__(self, nombre_jugador):
        super().__init__(nombre_jugador, nivel=3, meta_oleadas=5, bg_esquema="nivel_3")

    def reiniciar_nivel(self):
        SceneManager.cambiar_escena(NivelTresScene(self.nombre))

    def finalizar_nivel(self):
        from scenes.credits_scene import CreditsScene
        SceneManager.cambiar_escena(CreditsScene(self.nombre))

    def completar_nivel_logica(self):
        completar_nivel_3()
