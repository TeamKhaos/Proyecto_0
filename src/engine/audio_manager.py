import pygame
import os
import json

# Inicialización forzada
if not pygame.mixer.get_init():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()

class AudioManager:
    _instance = None
    _sounds = {}
    _volume = 1.0
    _music_volume = 0.5

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self):
        """Carga el volumen desde el archivo data.json"""
        path = os.path.join("data", "data.json")
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    self._volume = data.get("volumen_efectos", 1.0)
                    self._music_volume = data.get("volumen_musica", 0.5)
            except:
                pass

    def _save_settings(self):
        """Guarda el volumen actual en data.json"""
        path = os.path.join("data", "data.json")
        data = {}
        if os.path.exists(path):
            try:
                with open(path, "r") as f: data = json.load(f)
            except: pass
        
        data["volumen_efectos"] = self._volume
        data["volumen_musica"] = self._music_volume
        
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error guardando ajustes: {e}")

    @classmethod
    def set_volume(cls, volume):
        cls()._volume = volume
        for sound in cls._sounds.values():
            sound.set_volume(volume)
        cls()._save_settings()

    @classmethod
    def set_music_volume(cls, volume):
        cls()._music_volume = volume
        pygame.mixer.music.set_volume(volume)
        cls()._save_settings()

    @classmethod
    def get_sound(cls, name):
        if name not in cls._sounds:
            path = os.path.join("assets", "music", f"{name}.wav")
            if not os.path.exists(path): return None
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(cls()._volume)
                cls._sounds[name] = sound
            except: return None
        return cls._sounds.get(name)

    @classmethod
    def play(cls, name):
        sound = cls.get_sound(name)
        if sound:
            channel = pygame.mixer.find_channel(True)
            if channel: channel.play(sound)

    @staticmethod
    def play_boton():
        AudioManager.play("sonido botones")

    @staticmethod
    def play_disparo():
        AudioManager.play("sonido disparo")

    @staticmethod
    def play_explosion():
        AudioManager.play("explosion contra nave")

    @classmethod
    def play_music(cls, filename, volume=0.5):
        """Reproduce música de fondo (formato MP3/WAV) en bucle."""
        path = os.path.join("assets", "music", filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1) # -1 significa bucle infinito
                print(f"[Audio] Música iniciada: {filename}")
            except Exception as e:
                print(f"[Audio Error] No se pudo cargar música {filename}: {e}")
        else:
            print(f"[Audio Error] Archivo de música no encontrado: {path}")

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()
