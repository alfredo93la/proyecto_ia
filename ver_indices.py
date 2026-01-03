import pandas as pd

# Carga solo los nombres de las columnas
df = pd.read_csv('dataset.csv')
# Filtra tal como lo hiciste en el entrenamiento (quitando el Target)
X = df.drop('Target', axis=1)

print("--- MAPA DE ÍNDICES ---")
for i, col in enumerate(X.columns):
    print(f"Índice {i}: {col}")