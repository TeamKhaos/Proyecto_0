import pygame
import os

class AudioManager:
    """
    Gestor de audio centralizado para manejar efectos de sonido de forma eficiente.
    Utiliza el patrón Singleton para garantizar una única carga de recursos.
    """
    _instance = None
    _sounds = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._init_mixer()
        return cls._instance

    def _init_mixer(self):
        """Inicializa el sistema de sonido y carga los archivos .wav"""
        try:
            # Inicialización optimizada para evitar lag (frecuencia, tamaño de bits, canales, buffer)
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.mixer.init()
            
            base_path = os.path.join("assets", "music")
            sound_files = {
                "boton": "sonido botones.wav",
                "disparo": "sonido disparo.wav",
                "explosion": "explosion contra nave.wav"
            }

            for key, filename in sound_files.items():
                path = os.path.join(base_path, filename)
                if os.path.exists(path):
                    self._sounds[key] = pygame.mixer.Sound(path)
                    print(f"[Audio] Cargado: {filename}")
                else:
                    print(f"[Audio] Error: No se encontró {path}")
        except Exception as e:
            print(f"[Audio] Error crítico en inicialización: {e}")

    def play(self, key):
        """Reproduce el sonido asociado a la clave."""
        sound = self._sounds.get(key)
        if sound:
            # .play() busca automáticamente un canal libre para reproducir
            sound.play()

    @staticmethod
    def play_boton():
        AudioManager().play("boton")

    @staticmethod
    def play_disparo():
        AudioManager().play("disparo")

    @staticmethod
    def play_explosion():
        AudioManager().play("explosion")
