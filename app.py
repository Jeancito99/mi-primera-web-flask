from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import os

app = Flask(__name__)

# Variable global para mantener nuestro modelo en memoria listo para predecir
modelo = None

def entrenar_modelo_remoto():
    global modelo
    # CORRECCIÓN CRÍTICA: Convertimos tu enlace de visualización a enlace de descarga directa de Drive
    url_directa = "https://drive.google.com/uc?export=download&id=1D3S0dpMH-yQl1VRKec1lCZ7S0iZp-zJB"
    
    try:
        print("📡 Conectando a la nube y descargando dataset...")
        dataset = pd.read_csv(url_directa)
        
        X_train = dataset[['Monto', 'Hora', 'EnLinea']]
        y_train = dataset['EsFraude']

        modelo = DecisionTreeClassifier(random_state=42)
        modelo.fit(X_train, y_train)
        print("🧠 ¡Modelo de IA entrenado remotamente con éxito!")
        
    except Exception as e:
        print(f"⚠️ Error de red o URL inválida ({e}). Activando simulación local de contingencia...")
        # Datos de respaldo para que tu app en Render NUNCA se caiga si falla Google Drive
        datos_respaldo = {
            'Monto': [100.0, 2500.0, 50.0, 1800.0, 950.0, 20.0],
            'Hora': [12, 3, 14, 23, 1, 16],
            'EnLinea': [1, 1, 0, 1, 1, 0],
            'EsFraude': [0, 1, 0, 1, 1, 0]
        }
        dataset = pd.DataFrame(datos_respaldo)
        X_train = dataset[['Monto', 'Hora', 'EnLinea']]
        y_train = dataset['EsFraude']
        modelo = DecisionTreeClassifier(random_state=42)
        modelo.fit(X_train, y_train)
        print("📡 Simulación activada: Modelo entrenado con datos de contingencia.")

# Entrenamos el modelo inmediatamente al levantar la aplicación web
entrenar_modelo_remoto()

# Ruta principal: Maneja la visualización inicial (GET) y el envío del formulario (POST)
@app.route('/', methods=['GET', 'POST'])
def home():
    resultado = None
    clase_alerta = ""
    
    if request.method == 'POST':
        try:
            # 1. CAPTURA: Extraemos los datos que el usuario escribió en el formulario HTML
            monto = float(request.form['monto'])
            hora = int(request.form['hora'])
            en_linea = int(request.form['en_linea'])
            
            # 2. PREDICCIÓN: Pasamos los datos al árbol de decisión
            nueva_transaccion = [[monto, hora, en_linea]]
            prediccion = modelo.predict(nueva_transaccion)
            
            # 3. CLASIFICACIÓN: Evaluamos la salida de la IA
            if prediccion[0] == 1:
                resultado = "⚠️ ALERTA: La transacción se clasificó como FRAUDE."
                clase_alerta = "danger"  # Color rojo para la interfaz
            else:
                resultado = "✅ Transacción legítima aprobada."
                clase_alerta = "success" # Color verde para la interfaz
                
        except Exception as error:
            resultado = f"❌ Error al procesar los datos: {str(error)}"
            clase_alerta = "warning"
            
    # Le enviamos los resultados (si existen) a la página HTML para que los renderice
    return render_template('index.html', resultado=resultado, clase_alerta=clase_alerta)

if __name__ == '__main__':
    # Configuración obligatoria para que Render asigne su propio puerto dinámico
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)