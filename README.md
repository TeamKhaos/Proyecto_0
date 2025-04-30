# pip install pygame
# Codigo de ejemplo en main
---

    juego_naves/
    │
    ├── assets/
    │   ├── images/              # Sprites: jugador, enemigos, UI, fondo
    │   ├── sounds/              # Efectos: disparos, explosiones
    │   └── music/               # Música de fondo
    │
    ├── src/
    │   ├── main.py              # Punto de entrada - carga PantallaPrincipal
    │   ├── settings.py          # Configuración global (pantalla, FPS, volumen, etc.)
    │
    │   ├── ui/                  # Pantalla y menú principal
    │   │   └── main_menu.py     # [Yuve] UI: nombre jugador, botones, fullscreen, config
    │
    │   ├── scenes/
    │   │   └── level_select.py  # [Kairos] Selección de niveles
    │   │   └── level_1.py       # [Kairos] Nivel 1, carga nave y escenario
    │
    │   ├── gameplay/
    │   │   └── player.py        # [Edu] Lógica del jugador: movimiento, animación
    │   │   └── bullet.py        # [Edu] Disparos, colisiones
    │   │   └── score.py         # [Edu] Sistema de puntaje
    │
    │   ├── audio/
    │   │   └── music_manager.py # [Hanly] Cargar, reproducir y pausar música
    │
    │   ├── enemies/
    │   │   └── enemy.py         # [Wesitos] Enemigos básicos
    │   │   └── enemy_manager.py # [Wesitos] Control de aparición, muerte, disparos
    │
    │   ├── engine/
    │   │   └── game_loop.py     # Lógica del loop principal
    │   │   └── scene_manager.py # Cambio de escenas
    │   │   └── utils.py         # Funciones generales (carga imágenes, textos, etc.)
    │
    ├── data/
    │   └── highscores.json      # Puntajes guardados
    │
    ├── tests/                   # (Opcional) Pruebas unitarias
    ├── requirements.txt         # pygame, etc.
    ├── README.md
    └── .gitignore
