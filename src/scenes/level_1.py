from scenes.base_level import BaseLevelScene
from engine.progreso_manager import completar_nivel_1
from engine.scene_manager import SceneManager

class NivelUnoScene(BaseLevelScene):
    def __init__(self, nombre_jugador):
        super().__init__(nombre_jugador, nivel=1, meta_oleadas=3, bg_esquema="default")

    def reiniciar_nivel(self):
        SceneManager.cambiar_escena(NivelUnoScene(self.nombre))

    def finalizar_nivel(self):
        from scenes.select_level import SelectLevelScene
        SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

    def completar_nivel_logica(self):
        completar_nivel_1()
