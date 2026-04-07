from flask import Flask, jsonify
import yfinance as yf
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

app = Flask(__name__)

pares = [

"EURUSD=X","GBPUSD=X","AUDUSD=X","NZDUSD=X","USDCAD=X","USDCHF=X","USDJPY=X",

"EURGBP=X","EURAUD=X","EURNZD=X","EURCAD=X","EURCHF=X","EURJPY=X",

"GBPAUD=X","GBPNZD=X","GBPCAD=X","GBPCHF=X","GBPJPY=X",

"AUDNZD=X","AUDCAD=X","AUDCHF=X","AUDJPY=X",

"NZDCAD=X","NZDCHF=X","NZDJPY=X",

"CADCHF=X","CADJPY=X",

"CHFJPY=X"

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

            ema9 = EMAIndicator(close,9).ema_indicator()
            ema21 = EMAIndicator(close,21).ema_indicator()

            rsi = RSIIndicator(close,14).rsi()

            if ema9.iloc[-1] > ema21.iloc[-1] and rsi.iloc[-1] > 55:
                resultados.append({"par":par,"sinal":"COMPRA"})

            elif ema9.iloc[-1] < ema21.iloc[-1] and rsi.iloc[-1] < 45:
                resultados.append({"par":par,"sinal":"VENDA"})

        except:
            pass

    return jsonify(resultados)

import os

port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
