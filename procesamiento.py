import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Cargar el dataset
df = pd.read_csv('dataset.csv')

# Filtrado y definición del Target
# La columna 'Target' tiene: 'Dropout', 'Graduate', 'Enrolled'.
# Para tu objetivo (predecir abandono), convertiremos esto a binario:
# 1 = Dropout (Abandono), 0 = No Abandono (Graduate/Enrolled)
df['Target'] = df['Target'].apply(lambda x: 1 if x == 'Dropout' else 0)

# Separar características (X) y etiqueta (y)
X = df.drop('Target', axis=1)
y = df['Target']

# División del set de datos (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalado de datos
# Las redes neuronales convergen mejor si los datos tienen media 0 y desviación 1
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Guardar los datos procesados y el escalador para usarlo en la web después
np.save('X_train.npy', X_train_scaled)
np.save('X_test.npy', X_test_scaled)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)
joblib.dump(scaler, 'scaler.pkl') # Guardamos el escalador para normalizar los nuevos datos que lleguen de la web

print("Preprocesamiento terminado.")
print(f"Dimensiones de entrada (Input Shape): {X_train.shape[1]}")