from flask import Flask, jsonify, render_template
import os
import requests

app = Flask(__name__)

pares = [
"EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD",
"USDCHF","NZDUSD","EURJPY","GBPJPY","AUDJPY"
]

def calcular_sinal(precos):

    if len(precos) < 21:
        return "AGUARDAR"

    ema9 = sum(precos[-9:]) / 9
    ema21 = sum(precos[-21:]) / 21

    if ema9 > ema21:
        return "COMPRA"
    elif ema9 < ema21:
        return "VENDA"
    else:
        return "AGUARDAR"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sinais")
def sinais():

    resultados = []

    for par in pares:

        try:

            url = f"https://api.exchangerate.host/timeseries?start_date=2024-01-01&end_date=2024-12-31&base={par[:3]}&symbols={par[3:]}"
            r = requests.get(url)
            data = r.json()

            precos = []

            for d in data["rates"]:
                precos.append(data["rates"][d][par[3:]])

            sinal = calcular_sinal(precos)

        except:
            sinal = "ERRO"

        resultados.append({
            "par": par,
            "sinal": sinal
        })

    return jsonify(resultados)


if __name__ == "__main__":
    port = int(os.environ.get("PORT",3000))
    app.run(host="0.0.0.0", port=port)
