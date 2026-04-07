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
"GBPAUD"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sinais")
def sinais():

    resultados = []

    for par in pares:

        # lógica simples de tendência
        numero = random.randint(0,100)

        if numero > 50:
            sinal = "COMPRA"
        else:
            sinal = "VENDA"

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
