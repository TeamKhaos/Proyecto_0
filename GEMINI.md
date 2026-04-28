# Registro de Mejoras - Proyecto Star Rogue

Este documento detalla las implementaciones realizadas para optimizar el sistema de audio, la navegación entre escenas y la experiencia visual del usuario.

## 1. Sistema de Audio (AudioManager)
Se ha implementado un gestor centralizado (`src/engine/audio_manager.py`) con las siguientes características:
- **Arquitectura:** Patrón *Singleton* para evitar cargas duplicadas de archivos.
- **Buffer de Seguridad:** Configurado a `2048` para garantizar compatibilidad con drivers de audio en Windows y eliminar latencia.
- **Persistencia:** Los niveles de volumen se sincronizan automáticamente con `src/data/data.json`.
- **Efectos Soportados:**
    - `sonido botones.wav`: Interacciones en menús.
    - `sonido disparo.wav`: Acción de disparo de la nave.
    - `explosion contra nave.wav`: Colisiones (balas-enemigos, balas-jugador y nave-nave).
- **Música de Fondo:** Soporte para archivos `.mp3` con control de bucle infinito.

## 2. Mejoras en la Interfaz de Usuario (UI)
Se han unificado los efectos visuales y sonoros en todas las escenas:
- **Evento de Clic:** Se migró de `MOUSEBUTTONDOWN` a `MOUSEBUTTONUP` en todos los botones para asegurar una respuesta táctil y sonora natural.
- **Efecto Hover:** Implementación de cambio de color (`NES_LIGHT_BLUE`) y borde blanco grueso (`width=3`) al pasar el cursor sobre los botones en:
    - Menú Principal.
    - Selección de Nivel.
    - Menú de Pausa.
    - Pantalla de Game Over.
    - Pantalla de Victoria.
- **Sonidos de Botones:** Integrados en el 100% de la interfaz, incluyendo botones de retroceso, reintento y ajustes de volumen.

## 3. Corrección de Bugs Críticos
- **Navegación Fantasma (Cooldown):** Se implementó un bloqueo de entrada de **1000ms** al entrar en la `PantallaPrincipalScene`. Esto evita que el clic de "Volver" en Configuración active accidentalmente el botón "Salir" del menú principal.
- **Lógica de Pausa:** Se corrigió el menú de pausa moviendo la detección de colisiones al flujo de eventos principal, permitiendo que los botones respondan correctamente y con sonido.
- **Impactos Físicos:** Se activó el sonido de explosión en colisiones directas de la nave contra enemigos.

## 4. Instrucciones para Desarrolladores
- **Añadir Sonido:** `AudioManager.play("nombre_del_archivo")` (sin extensión .wav).
- **Ajustar Música:** `AudioManager.play_music("archivo.mp3")`.
- **Nuevos Botones:** Asegurarse de usar `pygame.MOUSEBUTTONUP` para mantener la consistencia del sistema de audio.
