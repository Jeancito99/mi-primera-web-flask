from flask import Flask, jsonify
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

@app.route("/")
def inicio():

    file_id = "1D3S0dpMH-yQl1VRKec1lCZ7S0iZp-zJB"
    url_nube = f"https://drive.google.com/uc?id={file_id}"

    dataset = pd.read_csv(url_nube)

    X_train = dataset[['Monto', 'Hora', 'EnLinea']]
    y_train = dataset['EsFraude']

    modelo = DecisionTreeClassifier(random_state=42)
    modelo.fit(X_train, y_train)

    nueva_transaccion = [[850.00, 23, 1]]
    prediccion = modelo.predict(nueva_transaccion)

    return jsonify({
        "fraude": int(prediccion[0])
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)