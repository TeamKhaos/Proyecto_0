# Registro de Mejoras - Sistema de Audio

Este documento registra las implementaciones realizadas en el sistema de audio para asegurar una experiencia de usuario fluida y persistente.

## Implementaciones Realizadas

### 1. AudioManager (Gestor Centralizado)
- **Patrón Singleton:** Garantiza que los sonidos se carguen una sola vez.
- **Buffer Optimizado:** Configurado a `2048` para eliminar latencia y fallos en Windows.
- **Persistencia:** Carga y guarda los niveles de volumen en `src/data/data.json`.
- **Soporte de Canales:** Utiliza `pygame.mixer.find_channel(True)` para permitir múltiples sonidos simultáneos (disparos rápidos, múltiples explosiones).

### 2. Integración de Sonidos
- **Botones:** 
    - Sonido: `sonido botones.wav`
    - Activación: Evento `MOUSEBUTTONUP` (al soltar el clic).
    - Ubicación: Implementado en todas las escenas (`MainMenu`, `PantallaPrincipal`, `SelectLevel`, `Tutorial`, `Config`).
- **Disparos:**
    - Sonido: `sonido disparo.wav`
    - Activación: Inmediata al crear el proyectil en `Level 1`.
- **Impactos / Explosiones:**
    - Sonido: `explosion contra nave.wav`
    - Activación: Al detectar colisión entre proyectil-enemigo, proyectil-nave o nave-enemigo.

### 3. Música de Fondo
- **Archivo:** `audio.mp3`
- **Control:** Métodos `play_music` y `stop_music` añadidos al gestor.
- **Persistencia:** El volumen de la música se ajusta globalmente desde el menú de configuración.

## Instrucciones de Mantenimiento
- Para añadir un nuevo sonido: Colocar el archivo `.wav` en `assets/music/` y llamarlo mediante `AudioManager.play("nombre_archivo")`.
- Para ajustar el volumen maestro: Utilizar `AudioManager.set_volume(valor)` donde `valor` es de 0.0 a 1.0.
