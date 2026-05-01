# 🚀 Star Rogue - Documentación Técnica (GEMINI.MD)

Este documento sirve como el **Índice de Contexto Maestro** para el desarrollo de Star Rogue. Proporciona una hoja de ruta técnica precisa para minimizar el consumo de tokens y maximizar la coherencia arquitectónica.

---

## 🏗️ Mapa de Símbolos y Arquitectura

### 📂 `src/engine/` (Núcleo del Motor)
- **`asset_manager.py`** (`AssetManager`): Singleton para caché de imágenes y fuentes.
- **`audio_manager.py`** (`AudioManager`): Gestor centralizado de canales y persistencia de volumen.
- **`scene_manager.py`** (`SceneManager`): Máquina de estados para transiciones entre escenas.
- **`progreso_manager.py`**: Gestión de `data.json`, desbloqueos y persistencia de skins/logros.
- **`visual_effects.py`**:
    - `ScreenShake`: Sacudida de pantalla basada en offsets aleatorios.
    - `HealthBar`: Barras con interpolación suave (Lerp) y daño fantasma.
- **`particle_system.py`** (`ParticleManager`): Explosiones y efectos de partículas dinámicas.
- **`player.py`** (`Nave`): Lógica del jugador, animación y efecto **Ghosting RGB**.
- **`background.py`** (`ParallaxManager`): Fondo estelar y **Objetos Espaciales** (planetas procedimentales).

### 📂 `src/scenes/` (Lógica de Juego)
- **`base_level.py`** (`BaseLevelScene`): Clase maestra para niveles. Maneja colisiones, UI dinámica, ScreenShake y flujo de victoria/derrota.
- **`level_1/2/3.py`**: Configuraciones específicas de dificultad y oleadas.
- **`select_level.py`**: Menú de selección con estados de desbloqueo.

### 📂 `src/ui/` (Interfaz de Usuario)
- **`hangar_scene.py`**: Selección y visualización de naves desbloqueadas.
- **`tutorial_scene.py`** (`InteractiveTutorialScene`): Nivel guiado por scripts para aprendizaje de mecánicas.
- **`pantalla_principal.py`**: Menú raíz con layout optimizado.

---

## 📊 Hitos Visuales (Fase 9: Post-Procesamiento)
*   **Screen Shake:** Activado en impactos críticos, daño al jugador y derrotas de jefes.
*   **Interpolación Lerp:** Barras de HP que reflejan el daño de forma fluida.
*   **Corrección de Sincronización:** El Tutorial Interactivo ahora está totalmente integrado con el nuevo sistema de efectos visuales y barras animadas.
*   **Muzzle Flashes:** Efecto de destello (pendiente de refinamiento).
*   **Glow Global:** Simulado mediante estelas y núcleos de color en proyectiles.

---

## 📜 Estándares Técnicos
1.  **Herencia:** Todos los niveles DEBEN heredar de `BaseLevelScene`.
2.  **Activos:** Cargar SIEMPRE vía `AssetManager.get_image` o `get_font`.
3.  **UI:** Botones estándar: `280x60px`. Colores: `assets.colors`.
4.  **Escalado:** Resolución virtual `800x600` con Letterboxing (ver `main.py`).

---
*Última actualización: 1 de mayo de 2026 - Control Creativo Cedido al Agente*
