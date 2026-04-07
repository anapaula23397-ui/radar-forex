from flask import Flask, jsonify
import yfinance as yf
import pandas as pd
import os

app = Flask(__name__)

pares = [
"EURUSD=X",
"GBPUSD=X",
"AUDUSD=X",
"USDJPY=X",
"USDCAD=X",
"USDCHF=X",
"NZDUSD=X"
]

@app.route("/")
def home():
    return "Radar Forex Online"

@app.route("/sinais")
def sinais():

    resultados = []

    for par in pares:

        try:

            data = yf.download(par, interval="1m", period="1d")

            close = data["Close"]

            ema9 = close.ewm(span=9).mean()
            ema21 = close.ewm(span=21).mean()

            if ema9.iloc[-1] > ema21.iloc[-1]:
                resultados.append({"par": par, "sinal": "COMPRA"})

            elif ema9.iloc[-1] < ema21.iloc[-1]:
                resultados.append({"par": par, "sinal": "VENDA"})

        except:
            pass

    return jsonify(resultados)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
