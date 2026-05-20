# 🚀 Star Rogue - Documentación Técnica (GEMINI.MD)

Este documento es el **Índice de Contexto Maestro**. Proporciona una hoja de ruta técnica precisa y define la dirección creativa del proyecto.

---

## 👁️ Lore & Ambientación (El Arcade Maldito)
"Star Rogue" no es un juego moderno; es un mueble de arcade antiguo, polvoriento y deteriorado encontrado en un rincón olvidado. El jugador toma el papel de alguien que decide encender la máquina. Lo que comienza como un shooter simple pronto revela una naturaleza hostil y consciente. El juego intenta comunicarse, advierte al jugador de peligros reales fuera de la pantalla y, finalmente, intenta atraparlo en un bucle de corrupción digital y fallos programados.

---

## 🏗️ Mapa de Símbolos y Arquitectura

### 📂 `src/engine/` (Núcleo del Motor)
- **`asset_manager.py`** (`AssetManager`): Singleton para caché de imágenes y fuentes.
- **`audio_manager.py`** (`AudioManager`): Gestor de canales y persistencia. *Próxima mejora: Efectos de distorsión.*
- **`scene_manager.py`** (`SceneManager`): Máquina de estados para transiciones entre escenas.
- **`visual_effects.py`**: `ScreenShake`, `HealthBar` (con Lerp).
- **`glitch_system.py` (NUEVO)**: Sistema para inyectar fallos de control y eventos visuales aleatorios.

### 📂 `src/scenes/` (Lógica de Juego)
- **`base_level.py`** (`BaseLevelScene`): Clase maestra para niveles. Maneja colisiones y ahora eventos meta-narrativos.
- **`tutorial_scene.py`**: Nivel guiado. Ahora incluye la fase de "Advertencia" con mensajes sospechosos.

---

## 📊 Historial de Hitos (Roadmap Evolutivo)

### 🔹 Fase 1 a 3: Core y Gameplay
* **Sistema de HP y UI:** Barras de vida visuales para la Nave.
* **IA de Enemigos:** Sistema de 3 oleadas gestionado por `EnemyManager`.
* **Escalado Dinámico:** Implementado Letterboxing y corrección de clic del mouse.
* **Visuales:** Fondo parallax de estrellas, nave animada y sistema de partículas estilo NES.

### 🔹 Fase 4: Pulido y Estabilidad
* **Estabilidad de Pantalla:** Corregido el error `display Surface quit`.
* **IA Avanzada:** Tipos `zigzag`, `tracker` y `kamikaze`. Jefes con patrones dinámicos.
* **Audio:** Implementación completa del `AudioManager`.

### 🔹 Fase 5: Expansión de Contenido
* **Niveles 2 y 3:** Nuevos desafíos, estéticas y jefes finales.
* **Power-ups:** Mejora de "Escopeta" (Triple disparo temporal).
* **Persistencia:** Sistema de progresión con guardado JSON y créditos finales.

### 🔹 Fase 6: Refactorización Arquitectónica
* **AssetManager:** Carga centralizada y eficiente de recursos.
* **Herencia Base:** Creación de `BaseLevelScene` para estandarizar niveles.
* **Meta-Progreso:** Hangar de naves, skins desbloqueables y sistema de logros.

### 🔹 Fase 7: User Experience (UX)
* **Tutorial Interactivo:** Nivel guiado por scripts para aprendizaje de mecánicas.
* **Optimización de UI:** Rediseño de menús para mejorar el flujo.

### 🔹 Fase 8: Fidelidad Visual Pro
* **Ghosting RGB:** Estelas cromáticas dinámicas en la nave.
* **Glow & Trail:** Proyectiles con núcleos brillantes y auras de color.
* **Parallax Galáctico:** Planetas y nebulosas procedimentales.

### 🔹 Fase 9: Post-Procesamiento
* **Screen Shake:** Sacudidas de pantalla dinámicas en impactos.
* **HealthBar Lerp:** Barras de HP con interpolación suave y daño fantasma.

### 🔹 Fase 10: Optimización Extrema
* **Asset Cache:** Imágenes reescaladas en caché para carga instantánea.
* **Zero-Copy Shake:** Optimización de CPU mediante offsets de blit.
* **Surface Reuse:** Reutilización de superficies persistentes.

### 🔹 Fase 11: UX & Tutorial Refinado
* **Dynamic Controls:** Indicadores WASD interactivos en el tutorial.
* **Interpolación de Jefes:** Movimiento suave (Lerp) en transiciones de fase.

### 🔹 Fase 12: La Capa Meta-Narrativa (EN PROGRESO)
* **Mensajes Críticos:** Diálogos que rompen la cuarta pared ("SAL DE AQUÍ", "NO DISPARES").
* **UI Arcade:** Estética de pantalla CRT vieja y eliminación de menús tradicionales.

### 🔹 Fase 13: Mecánicas de Incomodidad (PENDIENTE)
* **Input Delay:** Retrasos aleatorios en los controles para generar frustración.
* **Glitches de Audio:** Distorsión de música y sonidos de botones fallidos.

### 🔹 Fase 14: El Bucle de Corrupción (PENDIENTE)
* **Muerte Inevitable:** Scripting de jefe para forzar Game Over y alterar el menú principal.
* **Eventos Aleatorios:** Enemigos fantasmales y fallos visuales críticos.

---

## 📜 Estándares Técnicos y Reglas

### 🛡️ Reglas de Oro de Documentación (¡OBLIGATORIO!)
1. **Persistencia del Historial:** **NUNCA** se deben borrar o sobrescribir las fases anteriores. El historial debe ser exhaustivo.
2. **Actualización Constante:** Cada nuevo hito debe generar una fase nueva.
3. **Mantenimiento:** El Mapa de Símbolos debe reflejar el estado actual del código.

### 🛠️ Estándares de Horror Psicológico
1. **Inconsistencia Intencionada:** Los fallos (glitches) deben ser programados pero parecer errores fortuitos.
2. **Atmósfera de Tensión:** Uso de silencios repentinos o distorsiones ante eventos narrativos.
3. **Feedback Engañoso:** Mensajes de UI en rojo para advertencias reales del "sistema".

---
*Última actualización: 2 de mayo de 2026 - Documentación Restaurada e Integrada*
