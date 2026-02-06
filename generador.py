import pandas as pd
import random

# --- CONFIGURACIÓN ---
NUM_MUESTRAS = 200 
opciones = ['a', 'b', 'c', 'd', 'e']

# AQUI ESTÁ LA CLAVE 1: Perfiles diferenciados (Primaria + Secundaria)
config_carreras = {
    "Ingeniería de Software":        {'prim': 'a', 'sec': 'd'}, 
    "Ingeniería Mecatrónica":        {'prim': 'b', 'sec': 'a'}, 
    "Ingeniería Mecánica Eléctrica": {'prim': 'b', 'sec': 'c'}, 
    "Ingeniería Civil":              {'prim': 'c', 'sec': 'e'}, 
    "Administración":                {'prim': 'd', 'sec': 'a'}, 
    "Contaduría":                    {'prim': 'd', 'sec': 'e'}, # Diferente de Admin
    "Gestión y Dirección":           {'prim': 'd', 'sec': 'd'}, # Diferente de Conta
    "Ingeniería Industrial":         {'prim': 'e', 'sec': 'd'}  
}

def obtener_pesos_con_matiz(config):
    """
    AQUI ESTÁ LA CLAVE 2 (Reducción de Ruido):
    - 85% Probabilidad de acertar a su principal (Señal fuerte)
    - 10% Probabilidad de su secundaria (Matiz)
    - 5%  Ruido total (Error humano)
    """
    pesos = []
    for letra in opciones:
        if letra == config['prim']:
            pesos.append(0.85) # <--- SEÑAL MUY ALTA (Antes era 0.60)
        elif letra == config['sec']:
            pesos.append(0.10) # <--- MATIZ CLARO (Antes era 0.25)
        else:
            # El 5% restante se reparte entre las 3 opciones sobrantes
            pesos.append(0.05 / 3) 
    return pesos

datos = []

print("Generando datos con BAJO RUIDO y MATICES...")

for carrera, config in config_carreras.items():
    pesos = obtener_pesos_con_matiz(config)
    
    for _ in range(NUM_MUESTRAS):
        fila = {}
        for i in range(1, 21):
            fila[f"P{i:02d}"] = random.choices(opciones, weights=pesos, k=1)[0]
        
        fila['Carrera_Target'] = carrera
        fila['Satisfaccion'] = random.choices([4, 5], weights=[0.3, 0.7])[0]
        datos.append(fila)

df_nuevo = pd.DataFrame(datos)
df_nuevo.to_csv('datos/DATASET_CORREGIDO_BAJO_RUIDO.csv', index=False)

print(f"¡Listo! Archivo generado. Este dataset es muy 'limpio' y fácil de aprender.")