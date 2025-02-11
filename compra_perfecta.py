from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def analizar_compra_perfecta(ticker, time_frame):
    data = yf.download(ticker, interval=time_frame, progress=False)
    if data.empty:
        return f"No hay datos para {ticker}."

    # Cálculo de EWO y medias móviles
    data['EWO'] = data['Close'].ewm(span=21, adjust=False).mean()
    ma_21 = data['Close'].ewm(span=21, adjust=False).mean()
    ma_55 = data['Close'].ewm(span=55, adjust=False).mean()

    # Condición para la 'Compra Perfecta'
    if data['EWO'].iloc[-1] > 0 and ma_21.iloc[-1] > ma_55.iloc[-1]:
        return f"¡Señal de Compra Perfecta para {ticker}!"
    else:
        return f"No hay señal para {ticker}."

@app.route('/', methods=['GET'])
def index():
    return "¡La aplicación Compra Perfecta está funcionando!"

@app.route('/analizar', methods=['POST'])
def analizar():
    content = request.json
    tickers = content.get('tickers', [])
    time_frame = content.get('time_frame', '1m')
    
    resultados = {ticker: analizar_compra_perfecta(ticker, time_frame) for ticker in tickers}
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
