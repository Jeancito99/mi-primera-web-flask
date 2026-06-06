# Importamos Flask y la función para renderizar páginas HTML
from flask import Flask, render_template
import os

# Creamos la aplicación Flask
app = Flask(__name__)

# Definimos qué pasa cuando alguien entra a la página principal (raíz "/")
@app.route('/')
def home():
    # Le decimos a Flask que busque el archivo index.html dentro de la carpeta 'templates'
    return render_template('index.html')

# Bloque de seguridad para arrancar el servidor localmente
if __name__ == '__main__':
    # Leemos el puerto que nos asigne el servidor de internet, o usamos el 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    # Corremos la aplicación en modo de prueba (debug=True)
    app.run(host='0.0.0.0', port=port, debug=True)