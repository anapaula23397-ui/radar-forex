from flask import Flask, jsonify, render_template
import os
import random
from datetime import datetime

app = Flask(__name__)

pares = [
"EURUSD",
"GBPUSD",
"USDJPY",
"AUDUSD",
"USDCAD",
"USDCHF",
"NZDUSD",
"EURJPY",
"GBPJPY",
"AUDJPY",
"EURGBP",
"GBPAUD",
"EURAUD",
"GBPCAD",
"AUDCAD"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sinais")
def sinais():

    resultados = []

    for par in pares:

        numero = random.randint(0,100)

        if numero > 55:
            sinal = "COMPRA"
        elif numero < 45:
            sinal = "VENDA"
        else:
            sinal = "AGUARDAR"

        hora = datetime.now().strftime("%H:%M:%S")

        resultados.append({
            "par":par,
            "sinal":sinal,
            "hora":hora
        })

    return jsonify(resultados)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",3000))
    app.run(host="0.0.0.0",port=port)
