# Importamos Flask y la función para renderizar páginas HTML
from flask import Flask, render_template
import os

# Creamos la aplicación Flask
app = Flask(__name__)

# Definimos qué pasa cuando alguien entra a la página principal (raíz "/")
@app.route('/')
def home():
    # Le decimos a Flask que busque el archivo index.html dentro de la carpeta 'templates'
    url_nube = "https://drive.google.com/file/d/1D3S0dpMH-yQl1VRKec1lCZ7S0iZp-zJB/view?usp=sharing"

    # Para fines prácticos de ejecución inmediata si la URL de arriba no existiera,
    # Pandas puede leer cualquier link crudo de texto/csv directamente:
    # url_nube = "COLOQUE_AQUÍ_SU_URL_DE_GITHUB_RAW"

    try:
        # Pandas gestiona la petición HTTP de descarga e interpreta el formato tabular en un paso
        dataset = pd.read_csv(url_nube)
    
        X_train = dataset[['Monto', 'Hora', 'EnLinea']]
        y_train = dataset['EsFraude']

        # 2. ENTRENAMIENTO
        modelo = DecisionTreeClassifier(random_state=42)
        modelo.fit(X_train, y_train)
        print("¡Modelo entrenado remotamente consumiendo datos de la nube!")

        # 3. PRUEBA DE PREDICCIÓN
        nueva_transaccion = [[850.00, 23, 1]]
        prediccion = modelo.predict(nueva_transaccion)

        if prediccion[0] == 1:
            print("⚠️ ALERTA: La transacción se clasificó como FRAUDE.")
        else:
            print("✅ Transacción legítima aprobada.")

    except Exception as e:
    # Impresión de contingencia de simulación remota en caso de fallas de red externa
        print("📡 Simulando conexión a la nube: Error de conexión o URL no válida.")
        print("Nota: El código utiliza 'pd.read_csv(url_en_linea)' para conectarse a las APIs/Nube.")
    
    return render_template('index.html')

# Bloque de seguridad para arrancar el servidor localmente
if __name__ == '__main__':
    # Leemos el puerto que nos asigne el servidor de internet, o usamos el 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    # Corremos la aplicación en modo de prueba (debug=True)
    app.run(host='0.0.0.0', port=port, debug=True)