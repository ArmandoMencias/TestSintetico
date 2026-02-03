import pandas as pd
import random

# --- CONFIGURACIÓN ---
NUM_MUESTRAS_POR_CARRERA = 50  # Generaremos 200 perfiles por cada carrera (Total ~1600 filas)

# Lista de carreras a incluir en el modelo
carreras_map = {
    "Ingeniería de Software": 'a',
    "Ingeniería Mecatrónica": 'b',
    "Ingeniería Mecánica Eléctrica": 'b',
    "Ingeniería Civil": 'c',
    "Administración": 'd',
    "Contaduría": 'd',
    "Gestión y Dirección de Negocios": 'd',
    "Ingeniería Industrial": 'e'
}

# Las opciones disponibles en el test (a, b, c, d, e)
opciones = ['a', 'b', 'c', 'd', 'e']

def obtener_pesos(letra_dominante):
    """
    Define la probabilidad de elegir cada inciso según el perfil.
    Le damos un 70% de probabilidad a su letra dominante y repartimos
    el 30% restante entre las otras para dar realismo (ruido).
    """
    pesos = []
    for opcion in opciones:
        if opcion == letra_dominante:
            pesos.append(0.70)  # 70% de probabilidad de elegir su área
        else:
            pesos.append(0.075) # 7.5% de probabilidad para las otras (ruido)
    return pesos

def generar_encuesta_simulada(carrera, letra_dominante):
    """Genera una fila de respuestas para un alumno hipotético"""
    pesos = obtener_pesos(letra_dominante)
    
    fila = {}
    
    # Generamos respuestas para las 20 preguntas
    for i in range(1, 21):
        pregunta_id = f"P{i:02d}" # Ej: P01, P02...
        respuesta = random.choices(opciones, weights=pesos, k=1)[0]
        fila[pregunta_id] = respuesta
    
    # Agregamos la etiqueta de la carrera (Target)
    fila['Carrera_Target'] = carrera
    
    # Agregamos nivel de satisfacción (simulando que son egresados felices)
    # 80% de probabilidad de ser 4 o 5 (Satisfecho/Muy Satisfecho)
    fila['Satisfaccion'] = random.choices([3, 4, 5], weights=[0.1, 0.4, 0.5], k=1)[0]
    
    return fila

# --- EJECUCIÓN ---
datos_completos = []

print("Generando datos sintéticos...")

for carrera, letra_dominante in carreras_map.items():
    print(f"Creando {NUM_MUESTRAS_POR_CARRERA} perfiles para: {carrera} (Perfil '{letra_dominante}')")
    for _ in range(NUM_MUESTRAS_POR_CARRERA):
        datos_completos.append(generar_encuesta_simulada(carrera, letra_dominante))

# Convertir a DataFrame
df = pd.DataFrame(datos_completos)

# Guardar a CSV
nombre_archivo = 'dataset_vibe_profesional.csv'
df.to_csv(nombre_archivo, index=False)

print(f"\n¡Listo! Archivo '{nombre_archivo}' generado con éxito.")
print(f"Total de registros: {len(df)}")
print("\nVista previa de los datos:")
print(df.head())