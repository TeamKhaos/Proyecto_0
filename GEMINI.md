# 🚀 Proyecto de Naves - Documentación de Desarrollo (GEMINI.MD)

Este archivo es el punto de referencia sobre el estado actual, la arquitectura y el registro de cambios del juego. **Regla Crítica:** Actualizar este archivo tras cada funcionalidad nueva o corrección mayor.

---

## 🛠 Arquitectura del Proyecto

* **`src/main.py`**: Punto de entrada. Gestión de rutas, escalado de pantalla y transformación de coordenadas del mouse.
* **`src/settings.py`**: Configuraciones globales y utilidades de **Letterboxing** (4:3).
* **`src/engine/`**: Núcleo del motor.
    * `scene_manager.py`: Control de transiciones entre niveles y menús.
    * `progreso_manager.py`: Persistencia en `data.json` y desbloqueo de niveles.
    * **`audio_manager.py`**: Gestor centralizado (Singleton).
* **`src/scenes/`**: Lógica de escenas (Nivel 1, Selección de Nivel, Configuración).
* **`src/ui/`**: Componentes de interfaz y menús.

---

## 🔊 Sistema de Audio (Implementado)

Se ha establecido un gestor centralizado para una experiencia fluida:
* **Patrón Singleton:** Los recursos se cargan una sola vez en memoria.
* **Buffer Optimizado:** Configurado a **2048** para eliminar latencia en Windows.
* **Soporte de Canales:** Uso de `pygame.mixer.find_channel(True)` para sonidos simultáneos (disparos y explosiones).
* **Persistencia:** Los niveles de volumen se cargan/guardan en `src/data/data.json`.

### Integración de Sonidos:
* **Interfaz:** `sonido botones.wav` en evento `MOUSEBUTTONUP` (con retardo de 150ms para evitar navegación fantasma).
* **Combate:** `sonido disparo.wav` e `explosion contra nave.wav` para colisiones y proyectiles.
* **Música:** `audio.mp3` con métodos de control global (`play_music`, `stop_music`).

---

## 📊 Estado de Implementación

### Fase 1 a 3: Core y Gameplay [COMPLETADO]
* **Sistema de HP y UI:** Barras de vida visuales para la Nave.
* **IA de Enemigos:** Sistema de 3 oleadas gestionado por `EnemyManager`.
* **Escalado Dinámico:** Implementado Letterboxing y corrección de clic del mouse en pantalla completa/redimensionada.
* **Visuales:** Fondo parallax de estrellas, nave animada (64x64) y sistema de partículas retro (estilo NES).

### Fase 4: Pulido y Estabilidad [COMPLETADO]
* **Estabilidad de Pantalla:** Corregido el error `display Surface quit` al cambiar modos.
* **Optimización de Colisiones:** Se corrigió la eliminación de elementos mientras se itera la lista en `level_1.py`.
* **Audio:** Implementación completa del `AudioManager`.
* **IA Avanzada:** 
    * `Enemy` ahora soporta tipos: `zigzag`, `tracker` (persigue al jugador) y `kamikaze`.
    * `Boss` ahora tiene patrones: `Fan`, `Spiral` y `Targeted`, que cambian según su vida.
    * `Bala` mejorada para soportar movimiento vectorial (vx, vy).

### Fase 5: Expansión de Contenido [COMPLETADO]
* **Nivel 2:** Implementado con 5 oleadas más rápidas y un jefe con 200 HP y ataques acelerados.
* **Nivel 3:** Nivel final con estética de fuego, jefe de 350 HP y sistema de Power-ups.
* **Power-ups:** Drop raro (10%) de mejora de "Escopeta" que otorga triple disparo temporal.
* **Sistema de Progresión:** Desbloqueo automático de niveles y persistencia en JSON.
* **Créditos Finales:** Escena de scroll vertical que se activa al completar el Nivel 3.

### Fase 6: Refactorización y Nuevas Funcionalidades [COMPLETADO]
* **AssetManager:** Centralización de recursos para optimizar memoria (se cargan una sola vez).
* **Arquitectura Base:** Creación de `BaseLevelScene` para eliminar redundancia entre niveles.
* **Hangar:** Nueva escena para seleccionar naves desbloqueadas.
* **Skins:** Implementación de 4 tipos de naves (Default + 3 Mejoras) con visuales únicos.
* **Sistema de Logros:** Registro de medallas (Bronce, Plata, Oro) basado en tiempo y daño recibido.

### Fase 7: Experiencia de Usuario y Pulido [COMPLETADO]
* **Tutorial Interactivo:** Sustitución del tutorial estático por un nivel guiado con scripts de texto, práctica de movimiento y combate real.
* **Optimización de UI:** Rediseño del Menú Principal con espaciado mejorado y layout balanceado para evitar superposiciones.
* **Flujo de Navegación:** Reubicación del Tutorial a la pantalla de Selección de Niveles para un acceso más intuitivo.

### Fase 8: Fidelidad Visual y Efectos Especiales [COMPLETADO]
* **Sistema de Ghosting RGB:** Implementación de estelas cromáticas que siguen a la nave del jugador según su vector de movimiento.
* **Proyectiles Pro (Glow & Trail):** Rediseño de balas con núcleos brillantes, auras de color y estelas de trayectoria para mayor impacto visual.
* **Parallax Galáctico:** Mejora del fondo con "Objetos Espaciales" (planetas y nebulosas procedimentales) que añaden profundidad y variedad a cada nivel.
* **Explosiones Dinámicas:** Refinamiento del sistema de partículas con desvanecimiento alfa, varianza de tamaño y formas circulares.

---

## 📜 Convenciones y Mantenimiento

1.  **Colores:** Importar siempre desde `assets.colors`.
2.  **Colisiones:** Uso preferente de `pygame.Rect`.
3.  **Botones:** Tamaño estándar de **280x60px** con `font_pquena` para consistencia.
4.  **Audio:** Para nuevos sonidos, colocar en `assets/music/` y llamar vía `AudioManager.play("nombre")`.
5.  **Gráficos:** La paleta debe mantenerse fiel al estilo retro/NES.
6.  **Escenas de Nivel:** Heredar siempre de `BaseLevelScene` para mantener consistencia.

---

## 📌 Próximos Pasos
1.  **Tienda:** Implementar un sistema de puntos/monedas para comprar mejoras en lugar de desbloqueo directo.
2.  **Más Enemigos:** Añadir variedad de enemigos con patrones de ataque más complejos.
3.  **Partículas:** Mejorar el sistema de partículas para efectos de propulsión de la nave.

---
*Última actualización: 1 de mayo de 2026*