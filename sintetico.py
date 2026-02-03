import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer

# 1. Cargar tus datos semilla (los 50 por carrera que generamos antes)
# Asegúrate de tener el archivo 'dataset_vibe_profesional.csv' en la misma carpeta
real_data = pd.read_csv('dataset_vibe_profesional.csv')

print(f"Datos originales cargados: {len(real_data)} filas.")

# 2. Detectar la estructura (Metadata)
# SDV necesita saber qué columnas son categóricas y cuáles numéricas.
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(data=real_data)

print("\n--- Estructura detectada por SDV ---")
# Esto es para que veas cómo SDV entiende tus preguntas
print(metadata.to_dict()) 

# 3. Entrenar el Sintetizador
# Usamos GaussianCopulaSynthesizer porque es rápido y excelente para 
# detectar correlaciones en respuestas de opción múltiple (categóricas).
print("\nEntrenando el modelo (aprendiendo patrones)...")
synthesizer = GaussianCopulaSynthesizer(metadata)
synthesizer.fit(real_data)

# 4. Generar nuevos datos sintéticos
# Aquí le pedimos que cree 2000 perfiles nuevos basados en lo aprendido
CANTIDAD_A_GENERAR = 2000
synthetic_data = synthesizer.sample(num_rows=CANTIDAD_A_GENERAR)

print(f"\n¡Datos generados! {len(synthetic_data)} nuevas filas.")

# 5. Guardar el nuevo Dataset Robusto
# Es buena práctica agregar un prefijo para distinguir lo real de lo sintético
synthetic_data.to_csv('dataset_vibe_SDV_robusto.csv', index=False)

print("Archivo 'dataset_vibe_SDV_robusto.csv' guardado exitosamente.")

# --- BONUS: REVISIÓN DE CALIDAD ---
# SDV tiene una herramienta para decirte qué tan parecidos son los datos nuevos a los viejos
from sdv.evaluation.single_table import evaluate_quality

print("\nEvaluando la calidad de los datos sintéticos (0 a 100%)...")
quality_report = evaluate_quality(
    real_data,
    synthetic_data,
    metadata
)

# Un puntaje arriba de 80% es excelente. 
# Significa que estadísticamente son "indistinguibles" pero no son copias exactas.