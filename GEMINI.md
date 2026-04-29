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

---

## 📜 Convenciones y Mantenimiento

1.  **Colores:** Importar siempre desde `assets.colors`.
2.  **Colisiones:** Uso preferente de `pygame.Rect`.
3.  **Botones:** Tamaño estándar de **280x60px** con `font_pquena` para consistencia.
4.  **Audio:** Para nuevos sonidos, colocar en `assets/music/` y llamar vía `AudioManager.play("nombre")`.
5.  **Gráficos:** La paleta debe mantenerse fiel al estilo retro/NES.

---

## 📌 Próximos Pasos
1.  **Optimización:** Refinar el manejo de memoria en la carga de imágenes.
2.  **Nuevas Naves:** Implementar diferentes skins o tipos de naves para el jugador.
3.  **Logros:** Añadir un sistema de medallas por tiempo o daño recibido.

---
*Última actualización: 28 de abril de 2026*