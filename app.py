from flask import Flask, jsonify
import yfinance as yf
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

app = Flask(__name__)

pares = ["EURUSD=X","GBPUSD=X","USDJPY=X","AUDUSD=X","USDCAD=X"]

@app.route("/")
def home():
    return "Radar funcionando"

@app.route("/sinais")
def sinais():

    resultados = []

    for par in pares:

        data = yf.download(par, interval="1m", period="1d")

        close = data["Close"]

        ema9 = EMAIndicator(close,9).ema_indicator()
        ema21 = EMAIndicator(close,21).ema_indicator()

        rsi = RSIIndicator(close,14).rsi()

        if ema9.iloc[-1] > ema21.iloc[-1] and rsi.iloc[-1] > 55:
            resultados.append({"par":par,"sinal":"COMPRA"})

        elif ema9.iloc[-1] < ema21.iloc[-1] and rsi.iloc[-1] < 45:
            resultados.append({"par":par,"sinal":"VENDA"})

    return jsonify(resultados)

app.run(host="0.0.0.0", port=3000)
