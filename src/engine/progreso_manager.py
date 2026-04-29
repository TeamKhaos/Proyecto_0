import json
import os

DATA_PATH = "data/data.json"

def cargar_progreso():
    # Asegurarse de que el directorio exista
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    if not os.path.exists(DATA_PATH):
        # Progreso inicial por defecto
        progreso_inicial = {
            "nivel_1_completado": False,
            "nivel_2_desbloqueado": False,
            "nivel_3_desbloqueado": False
        }
        guardar_progreso(progreso_inicial)
        return progreso_inicial
    
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    except:
        return {"nivel_1_completado": False, "nivel_2_desbloqueado": False, "nivel_3_desbloqueado": False}

def guardar_progreso(progreso):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w') as f:
        json.dump(progreso, f, indent=4)

def completar_nivel_1():
    progreso = cargar_progreso()
    progreso["nivel_1_completado"] = True
    progreso["nivel_2_desbloqueado"] = True
    guardar_progreso(progreso)

def completar_nivel_2():
    progreso = cargar_progreso()
    progreso["nivel_2_completado"] = True
    progreso["nivel_3_desbloqueado"] = True
    guardar_progreso(progreso)

def completar_nivel_3():
    progreso = cargar_progreso()
    progreso["nivel_3_completado"] = True
    guardar_progreso(progreso)
