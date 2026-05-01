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
            "nivel_3_desbloqueado": False,
            "nave_seleccionada": "default",
            "naves_desbloqueadas": ["default"],
            "logros": {}
        }
        guardar_progreso(progreso_inicial)
        return progreso_inicial
    
    try:
        with open(DATA_PATH, 'r') as f:
            progreso = json.load(f)
            # Asegurar que existan las nuevas llaves
            if "nave_seleccionada" not in progreso: progreso["nave_seleccionada"] = "default"
            if "naves_desbloqueadas" not in progreso: progreso["naves_desbloqueadas"] = ["default"]
            if "logros" not in progreso: progreso["logros"] = {}
            return progreso
    except:
        return {"nivel_1_completado": False, "nivel_2_desbloqueado": False, "nivel_3_desbloqueado": False, "nave_seleccionada": "default", "naves_desbloqueadas": ["default"], "logros": {}}

def registrar_logro(nivel, tiempo, dano):
    progreso = cargar_progreso()
    medalla = "BRONCE"
    
    # Lógica simple de medallas
    if tiempo < 60 and dano < 50:
        medalla = "ORO"
    elif tiempo < 90 and dano < 100:
        medalla = "PLATA"
        
    logro_id = f"nivel_{nivel}"
    if logro_id not in progreso["logros"] or medalla_superior(medalla, progreso["logros"][logro_id]):
        progreso["logros"][logro_id] = medalla
        guardar_progreso(progreso)
    return medalla

def medalla_superior(m1, m2):
    orden = {"BRONCE": 1, "PLATA": 2, "ORO": 3}
    return orden.get(m1, 0) > orden.get(m2, 0)

def guardar_progreso(progreso):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w') as f:
        json.dump(progreso, f, indent=4)

def seleccionar_nave(skin):
    progreso = cargar_progreso()
    progreso["nave_seleccionada"] = skin
    guardar_progreso(progreso)

def desbloquear_nave(skin):
    progreso = cargar_progreso()
    if skin not in progreso["naves_desbloqueadas"]:
        progreso["naves_desbloqueadas"].append(skin)
        guardar_progreso(progreso)

def completar_nivel_1():
    progreso = cargar_progreso()
    progreso["nivel_1_completado"] = True
    progreso["nivel_2_desbloqueado"] = True
    if "mejora1" not in progreso["naves_desbloqueadas"]:
        progreso["naves_desbloqueadas"].append("mejora1")
    guardar_progreso(progreso)

def completar_nivel_2():
    progreso = cargar_progreso()
    progreso["nivel_2_completado"] = True
    progreso["nivel_3_desbloqueado"] = True
    if "mejora2" not in progreso["naves_desbloqueadas"]:
        progreso["naves_desbloqueadas"].append("mejora2")
    guardar_progreso(progreso)

def completar_nivel_3():
    progreso = cargar_progreso()
    progreso["nivel_3_completado"] = True
    if "mejora3" not in progreso["naves_desbloqueadas"]:
        progreso["naves_desbloqueadas"].append("mejora3")
    guardar_progreso(progreso)
