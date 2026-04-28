# Proyecto de Naves - Documentación de Desarrollo

Este archivo sirve como punto de referencia para la IA y los desarrolladores sobre el estado actual y la arquitectura del juego.

## 🚀 Arquitectura del Proyecto

- `src/main.py`: Punto de entrada del juego. Gestión de rutas, escalado de pantalla y transformación de entrada (mouse).
- `src/settings.py`: Configuraciones globales y utilidades de escalado (Letterboxing).
- `src/engine/`: Núcleo del motor de juego.
    - `scene_manager.py`: Gestiona el cambio entre niveles y menús.
    - `progreso_manager.py`: Gestión de guardado en JSON y desbloqueo de niveles.
- `src/scenes/`: Lógica de niveles específicos.
    - `level_1.py`: Escena del primer nivel.
    - `select_level.py`: Pantalla de selección con niveles bloqueados/desbloqueados.
- `src/enemies/`: Gestión de entidades hostiles.
- `src/ui/`: Componentes de interfaz de usuario.
    - `pantalla_principal.py`: Menú principal con botón de redimensión rápida.
    - `config_scene.py`: Ajustes de volumen.
- `src/assets/`: Directorio de recursos.
    - `music/`: Contiene música de fondo (`audio.mp3`) y efectos de sonido (`explosion contra nave.wav`, `sonido botones.wav`, `sonido disparo.wav`).
    - `images/`: Sprites de naves, enemigos, jefes y UI.
    - `fonts/`: Fuentes tipográficas (Ej: `upheavtt.ttf`).

## 🛠 Estado de Implementación (Nivel 1)

### Fase 1: Mejoras de UI y Salud [COMPLETADO]
- [x] Implementar sistema de HP en `Nave`.
- [x] Crear barras de vida visuales.

### Fase 2: IA y Oleadas [COMPLETADO]
- [x] Implementar sistema de 3 oleadas en `EnemyManager`.

### Fase 3: Progresión y Pantalla [COMPLETADO]
- [x] Sistema de bloqueo de niveles.
- [x] Persistencia de progreso en `src/data/data.json`.
- [x] **Sistema de Escalado Dinámico:** Implementado letterboxing para mantener aspect ratio 4:3.
- [x] **Corrección de Mouse en Fullscreen:** Las coordenadas se transforman automáticamente y se sobrescribe `get_pos` para corregir clics y efectos *hover*.
- [x] **Estabilidad de Pantalla:** Corregido bug `display Surface quit` al cambiar modos de pantalla.
- [x] **Mejoras Visuales:** Fondo parallax de estrellas y nueva nave animada (64x64) con estados (reposo/movimiento).

### Fase 4: Corrección de Errores y Pulido [EN PROGRESO]
- [x] **Corrección de Crash:** Añadidos atributos `ancho` y `alto` a las clases `Enemy` y `Boss`.
- [x] **Optimización de Colisiones:** Corregida la eliminación de elementos de una lista durante su iteración en `level_1.py`.
- [x] **Mejora de Partículas:** Implementado sistema de partículas retro (cuadradas) con física de fricción y paleta NES.

## 📜 Convenciones
1. Los colores deben importarse de `assets.colors`.
2. Las colisiones se manejan preferentemente mediante `pygame.Rect`.
3. El progreso se guarda automáticamente al derrotar al Jefe del Nivel 1.
4. **REGLA CRÍTICA:** Este archivo `GEMINI.md` DEBE ser actualizado siempre que se añada una nueva funcionalidad, se corrija un bug importante o se cambie la arquitectura.

## 📌 Próximos Pasos
1. Implementar el Nivel 2 con nuevos tipos de enemigos.
2. Añadir efectos de sonido y música.
3. Mejorar los sprites de la nave del jugador.

## 🔄 Continuará...
- **Última orden:** "analiza la carpeta de audios y lo añadas en consideracion a la carpeta gemini.md" (Analizados audios en `src/assets/music/` y `src/assets/sounds/`, documentación actualizada).
