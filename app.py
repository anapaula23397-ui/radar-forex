from flask import Flask, jsonify, render_template
import os
import random

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
"AUDJPY"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sinais")
def sinais():

    resultados = []

    for par in pares:

        sinal = random.choice(["COMPRA","VENDA"])

        resultados.append({
            "par":par,
            "sinal":sinal
        })

    return jsonify(resultados)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",3000))
    app.run(host="0.0.0.0",port=port)
