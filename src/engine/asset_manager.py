import pygame
import os

class AssetManager:
    _images = {}
    _fonts = {}
    _sounds = {}

    @classmethod
    def get_image(cls, path, scale=None):
        key = (path, scale)
        if key not in cls._images:
            if path not in cls._images:
                if not os.path.exists(path):
                    print(f"Advertencia: No se encontró la imagen en {path}")
                    return None
                img = pygame.image.load(path).convert_alpha()
                cls._images[path] = img
            
            if scale:
                img = cls._images[path]
                cls._images[key] = pygame.transform.scale(img, scale)
            else:
                cls._images[key] = cls._images[path]
        
        return cls._images[key]

    @classmethod
    def get_font(cls, path, size):
        key = (path, size)
        if key not in cls._fonts:
            if not os.path.exists(path):
                print(f"Advertencia: No se encontró la fuente en {path}")
                return pygame.font.SysFont("Arial", size)
            cls._fonts[key] = pygame.font.Font(path, size)
        return cls._fonts[key]

    @classmethod
    def clear(cls):
        cls._images.clear()
        cls._fonts.clear()
        cls._sounds.clear()
