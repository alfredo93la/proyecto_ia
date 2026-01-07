import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.metrics import classification_report

# Cargar datos procesados
X_train = np.load('X_train.npy')
X_test = np.load('X_test.npy')
y_train = np.load('y_train.npy')
y_test = np.load('y_test.npy')

# Verificar dimensiones
input_dim = X_train.shape[1]
print(f"Entrenando con {input_dim} características de entrada.")

# Definir la arquitectura de la Red Neuronal
model = Sequential()

# Primera capa oculta (64 neuronas, activación ReLU)
model.add(Dense(64, input_shape=(input_dim,), activation='relu'))
model.add(Dropout(0.2)) 

# Segunda capa oculta (32 neuronas, activación ReLU)
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))

# Capa de salida (1 neurona, activación Sigmoid para probabilidad 0 a 1)
model.add(Dense(1, activation='sigmoid'))

# Compilar el modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# Evaluar el modelo con datos que nunca ha visto (Test set)
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\nPrecisión en Test Set: {accuracy*100:.2f}%")

# Guardar el modelo entrenado
model.save('modelo_dropout.h5')
print("Modelo guardado como 'modelo_dropout.h5'")