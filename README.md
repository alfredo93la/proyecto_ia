# Agente Inteligente para la Predicción de Deserción Escolar en ESCOM

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-orange)
![Flask](https://img.shields.io/badge/Flask-Backend-green)
![Status](https://img.shields.io/badge/Status-Prototipo%20Funcional-success)

**Este es un agente inteligente híbrido diseñado para detectar y prevenir la deserción escolar en estudiantes de Ingeniería en Sistemas Computacionales (ESCOM - IPN).

El sistema combina la potencia probabilística de una **Red Neuronal Artificial** con la precisión determinista de un **Sistema Experto** basado en el reglamento académico, ofreciendo un diagnóstico integral de la trayectoria del alumno.

---

## 🚀 Características Principales

### 1. Arquitectura Híbrida Neuro-Simbólica
A diferencia de los predictores tradicionales, este sistema opera en dos capas:
* **Capa Probabilística (Deep Learning):** Un modelo de Red Neuronal (MLP con Dropout) analiza patrones ocultos en variables socioeconómicas y académicas para estimar la *probabilidad* de abandono.
* **Capa Determinista (Lógica Simbólica):** Un motor de reglas validado contra el plan de estudios de la ESCOM (387 Créditos) analiza la viabilidad matemática de terminar la carrera a tiempo.

### 2. Validación con Datos del SAES
El sistema incorpora variables críticas del entorno real:
* **Detección de Desfase:** Calcula si los créditos obtenidos corresponden al semestre cursado.
* **Viabilidad Matemática:** Determina si es matemáticamente posible terminar la carrera con los periodos restantes (Cálculo de "Velocidad de Crucero").
* **Hitos Curriculares:** Alertas automáticas para inicio de Servicio Social y Trámites de Titulación.

### 3. Interfaz Web Responsiva
Desarrollada en HTML5 y Bootstrap, capaz de desplegarse en red local para acceso desde dispositivos móviles.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Backend:** Flask (Micro-framework)
* **Inteligencia Artificial:** TensorFlow / Keras
* **Procesamiento de Datos:** NumPy, Pandas, Scikit-learn
* **Persistencia de Modelos:** Joblib (Scalers) y H5 (Pesos neuronales)
* **Frontend:** HTML5, CSS3, JavaScript (Chart.js para visualización)

---

## 📋 Pre-requisitos

Asegúrate de tener instalado Python 3.8 o superior. Las dependencias necesarias se encuentran en `requirements.txt`.

```bash
flask
tensorflow
numpy
pandas
scikit-learn
joblib
