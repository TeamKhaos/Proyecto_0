from scenes.base_level import BaseLevelScene
from engine.progreso_manager import completar_nivel_2
from engine.scene_manager import SceneManager

class NivelDosScene(BaseLevelScene):
    def __init__(self, nombre_jugador):
        super().__init__(nombre_jugador, nivel=2, meta_oleadas=5, bg_esquema="nivel_2")

    def reiniciar_nivel(self):
        SceneManager.cambiar_escena(NivelDosScene(self.nombre))

    def finalizar_nivel(self):
        from scenes.select_level import SelectLevelScene
        SceneManager.cambiar_escena(SelectLevelScene(self.nombre))

    def configurar_boss(self):
        self.boss.max_vida = 250
        self.boss.vida = 250
        self.boss.tint_color = (100, 255, 100) # Verde para el segundo jefe
        self.boss.__init__(target=self.nave, tint_color=self.boss.tint_color, nivel=2)
        self.boss.max_vida = 250
        self.boss.vida = 250
        self.boss.shoot_delay = 45

    def completar_nivel_logica(self):
        completar_nivel_2()
