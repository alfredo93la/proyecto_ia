import numpy as np
from flask import Flask, request, jsonify, render_template
from keras.models import load_model
import joblib

app = Flask(__name__)

# --- CARGA DEL MODELO Y ESCALADOR ---
model = load_model('modelo_dropout.h5')
scaler = joblib.load('scaler.pkl')

def generar_recomendacion(probabilidad, debtor, promedio_general, promedio_anterior, periodos_cursados, creditos, periodos_restantes, displaced):
    recomendaciones = []
    
    # CONSTANTES ESCOM
    TOTAL_CREDITOS = 387.0
    CARGA_MAXIMA = 77.4
    CARGA_MEDIA = 48.38
    
    creditos_faltantes = TOTAL_CREDITOS - creditos
    avance_pct = (creditos / TOTAL_CREDITOS) * 100

    # ANÁLISIS DE CRÉDITOS RESTANTES
    velocidad_necesaria = 0
    if periodos_restantes > 0:
        velocidad_necesaria = creditos_faltantes / periodos_restantes
        
        if creditos_faltantes <= 0:
            recomendaciones.append("**¡FELICIDADES!** Has cubierto todos los créditos. Inicia trámite de titulación.")
        elif velocidad_necesaria > CARGA_MAXIMA:
            recomendaciones.append(f"**IMPOSIBLE TERMINAR:** Matemáticamente no puedes acabar. Necesitas {velocidad_necesaria:.1f} créditos/semestre y el máximo es {CARGA_MAXIMA}. Consulta a Control Escolar.")
        elif velocidad_necesaria > (CARGA_MAXIMA - 15):
            recomendaciones.append(f"**ALERTA MÁXIMA:** Estás al límite. Necesitas meter {velocidad_necesaria:.1f} créditos todos los semestres restantes.")
        elif velocidad_necesaria > (CARGA_MEDIA + 5):
            recomendaciones.append(f"**Acelerar Paso:** Necesitas promediar {velocidad_necesaria:.1f} créditos por semestre (más de la carga media).")
    else:
        if creditos_faltantes > 0:
            recomendaciones.append("**TIEMPO AGOTADO:** Se acabaron tus periodos reglamentarios y aún debes créditos.")

    # ANÁLISIS DE RIESGO (Redes Neuronales)
    if probabilidad > 50:
        recomendaciones.append("**Alerta Crítica:** Riesgo muy alto detectado por patrones históricos.")
    elif probabilidad > 20:
        recomendaciones.append("**Atención:** Estás en zona de riesgo.")

    # 3. REGLA ESPECÍFICA: FORÁNEOS (NUEVO)
    if displaced == 1.0:
        recomendaciones.append("**Apoyo Foráneo:** Al ser foráneo, consulta las becas de 'Transporte' y 'Manutención' del IPN para asegurar tu estabilidad económica.")

    # ANÁLISIS DE TRAYECTORIA (Promedios)
    if promedio_anterior < (promedio_general - 1.0):
        recomendaciones.append("**Tendencia Negativa:** Tu rendimiento reciente cayó drásticamente respecto a tu promedio general.")
    elif promedio_anterior > (promedio_general + 0.5):
        recomendaciones.append("**Tendencia Positiva:** ¡Bien! Estás subiendo tu promedio respecto a tu histórico.")

    if promedio_general < 6.0:
        recomendaciones.append("**Promedio reprobatorio:** Tu promedio es crítico. Considera regularización.")

    # PORCENTAJES DE AVANCE
    if 60 <= avance_pct < 70:
        recomendaciones.append(f"**Protocolo de TT:** Tienes {avance_pct:.1f}% de avance. Empieza a buscar tema de Trabajo Terminal.")
    
    if avance_pct >= 70:
        recomendaciones.append("**Titulación:** Superaste el 70%. Ya puedes iniciar tu Servicio Social y Estancia Profesional.")

    # REGLAS GENERALES
    if debtor == 1:
        if periodos_cursados >= 9:
             recomendaciones.append("**Dictamen:** Tienes adeudos y estás en semestres finales. Revisa tu tiempo máximo.")
        else:
             recomendaciones.append("**Regularización:** Prioriza salvar materias en ETS antes de adelantar nuevas.")

    # Mensaje por defecto
    if not recomendaciones:
        recomendaciones.append(f"**Mantenimiento:** Buen ritmo. Necesitas {velocidad_necesaria:.1f} créditos/semestre para graduarte a tiempo.")

    return recomendaciones

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Extracción de variables
        periodos_cursados = int(data['periodos_cursados'])
        turno = float(data['turno'])
        debtor = float(data['debtor'])
        scholarship = float(data['scholarship'])
        age = float(data['age'])
        promedio_general = float(data['promedio_general'])
        promedio_anterior = float(data['promedio_anterior'])
        displaced = float(data['displaced'])
        
        # Variables SAES
        creditos = float(data['creditos'])
        periodos_restantes = int(data['periodos_restantes'])
        
        # Vector para la IA (34 neuronas)
        input_data = np.zeros((1, 34))
        input_data += 0.5 
        
        # Mapeo
        input_data[0, 4] = turno
        input_data[0, 13] = debtor
        input_data[0, 14] = 1.0       
        input_data[0, 16] = scholarship
        input_data[0, 17] = age
        input_data[0, 23] = promedio_general * 2  
        input_data[0, 29] = promedio_anterior * 2
        input_data[0, 32] = displaced

        # Predicción
        input_scaled = scaler.transform(input_data)
        prediction_prob = model.predict(input_scaled)[0][0]
        percentage = round(prediction_prob * 100, 2)
        
        if percentage > 50:
            risk_level = "RIESGO ALTO"
        elif percentage > 20:
            risk_level = "RIESGO MEDIO"
        else:
            risk_level = "RIESGO BAJO"

        # Generar Consejos con TODAS las variables
        consejos = generar_recomendacion(percentage, debtor, promedio_general, promedio_anterior, periodos_cursados, creditos, periodos_restantes, displaced)

        return jsonify({
            'probability': percentage,
            'risk': risk_level,
            'advice': consejos
        })

    except Exception as e:
        print(f"ERROR SERVIDOR: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)