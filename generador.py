import pandas as pd
import numpy as np
import random

# CONFIGURACIÓN
NUM_MUESTRAS = 300

# Mapeo de preguntas a áreas (Para saber qué preguntas deben tener puntaje alto en cada carrera)
# Q01-Q08: Aptitudes | Q09-Q16: Intereses | Q17-Q24: Futuro | Q25: Materias
# Definimos qué índices de preguntas son CLAVE para cada área
mapa_preguntas = {
    "Software": [2, 9, 10, 17, 24],       # Computadoras, Apps, Robots, Código
    "Mecatronica": [4, 7, 10, 15, 18, 24],# Reparar, Robots, Motores, Armar
    "Civil": [3, 8, 11, 19, 23],          # Planos, 3D, Construcción, Obra
    "Mecanica": [4, 7, 15, 18, 22],       # Reparar, Optimizar, Motores, Fábrica
    "Industrial": [6, 7, 14, 22],         # Organizar, Optimizar, Procesos
    "Administracion": [5, 6, 12, 16, 21], # Dinero, Liderazgo, Negocio, Mercado
    "Contaduria": [1, 5, 13, 20],         # Números, Dinero, Impuestos, Facturas
    "Gestion": [6, 12, 16, 21]            # Liderazgo, Negocio, Mercado, Juntas
}

carreras = list(mapa_preguntas.keys())

data = []

def generar_respuesta_likert(es_clave):
    """
    Si es una pregunta clave para su carrera, tiende a responder 4 o 5.
    Si NO es clave, responde aleatorio pero tirando a bajo/medio (1-3).
    """
    if es_clave:
        # Probabilidades para preguntas de SU área: [1, 2, 3, 4, 5]
        # Muy probable 4 y 5
        return random.choices([1, 2, 3, 4, 5], weights=[0.02, 0.03, 0.15, 0.40, 0.40])[0]
    else:
        # Probabilidades para preguntas ajenas:
        # Más probable 1, 2 o 3. A veces 4 o 5 (porque pueden ser buenos en otras cosas)
        return random.choices([1, 2, 3, 4, 5], weights=[0.30, 0.30, 0.25, 0.10, 0.05])[0]

print("Generando datos numéricos...")

for carrera in carreras:
    preguntas_clave = mapa_preguntas[carrera]
    
    for _ in range(NUM_MUESTRAS):
        fila = {'Carrera_Target': carrera}
        
        # Generar Q1 a Q24 (Escala 1-5)
        for i in range(1, 25):
            es_clave = i in preguntas_clave
            fila[f'Q{i}'] = generar_respuesta_likert(es_clave)
            
        # Generar Q25 (Materias - Opción Múltiple a-f)
        # Aquí forzamos un poco la tendencia según la carrera
        if carrera == "Software":
            fila['Q25'] = random.choices(['a', 'b', 'f'], weights=[0.8, 0.1, 0.1])[0]
        elif carrera in ["Civil", "Mecanica", "Mecatronica"]:
            fila['Q25'] = random.choices(['b', 'c', 'a'], weights=[0.4, 0.4, 0.2])[0]
        elif carrera in ["Administracion", "Gestion"]:
            fila['Q25'] = random.choices(['e', 'f', 'd'], weights=[0.6, 0.2, 0.2])[0]
        elif carrera == "Contaduria":
            fila['Q25'] = random.choices(['d', 'a', 'e'], weights=[0.8, 0.1, 0.1])[0]
        elif carrera == "Industrial":
            fila['Q25'] = random.choices(['f', 'e', 'c'], weights=[0.7, 0.2, 0.1])[0]
            
        data.append(fila)

df_likert = pd.DataFrame(data)
df_likert.to_csv('datos/DATASET_LIKERT_NUMERICO.csv', index=False)
print("¡Dataset Numérico Generado!")
print(df_likert.head())