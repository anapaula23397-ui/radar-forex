from flask import Flask, jsonify, render_template
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
    return render_template("index.html")

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

            preco = close.iloc[-1]

# COMPRA
if ema9.iloc[-1] > ema21.iloc[-1] and rsi.iloc[-1] > 50:
    resultados.append({"par":par,"sinal":"COMPRA"})

# VENDA
elif ema9.iloc[-1] < ema21.iloc[-1] and rsi.iloc[-1] < 50:
    resultados.append({"par":par,"sinal":"VENDA"})

# TOQUE NA MÉDIA (gera mais sinais)
elif preco > ema9.iloc[-1]:
    resultados.append({"par":par,"sinal":"COMPRA"})

elif preco < ema9.iloc[-1]:
    resultados.append({"par":par,"sinal":"VENDA"})

        except:
            pass

    return jsonify(resultados)

import os

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
