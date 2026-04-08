from flask import Flask, jsonify, render_template
import requests
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

pares = [
"EURUSD","GBPUSD","USDJPY","AUDUSD",
"USDCAD","USDCHF","NZDUSD","EURJPY","GBPJPY","AUDJPY"
]

def calcular_indicadores(precos):

    df = pd.DataFrame(precos, columns=["close"])

    df["ema9"] = df["close"].ewm(span=9).mean()
    df["ema21"] = df["close"].ewm(span=21).mean()

    delta = df["close"].diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = ganho / perda
    df["rsi"] = 100 - (100 / (1 + rs))

    ultima = df.iloc[-1]

    if ultima["ema9"] > ultima["ema21"] and ultima["rsi"] > 55:
        return "COMPRA"

    if ultima["ema9"] < ultima["ema21"] and ultima["rsi"] < 45:
        return "VENDA"

    return "AGUARDAR"


def pegar_precos(par):

    base = par[:3]
    quote = par[3:]

    url = f"https://api.frankfurter.app/2024-01-01..2024-12-31?from={base}&to={quote}"

    r = requests.get(url)

    data = r.json()

    precos = []

    for d in data["rates"]:
        precos.append(data["rates"][d][quote])

    return precos[-100:]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sinais")
def sinais():

    resultados = []

    for par in pares:

        try:

            precos = pegar_precos(par)

            sinal = calcular_indicadores(precos)

        except:
            sinal = "ERRO"

        resultados.append({
            "par": par,
            "sinal": sinal,
            "hora": datetime.now().strftime("%H:%M:%S")
        })

    return jsonify(resultados)


if __name__ == "__main__":
    port = int(os.environ.get("PORT",3000))
    app.run(host="0.0.0.0", port=port)
