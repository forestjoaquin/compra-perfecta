import yfinance as yf
import pandas_ta as ta
import time
import requests

# Tu número de teléfono y API para notificaciones SMS (reemplaza si es necesario)
telefono = "+19096650080"
sinch_api_url = "https://us.sms.api.sinch.com/xms/v1/be7bf3af69a74b1ba7b60f5952a88cd4/batches"
sinch_api_token = "e7bc63f435684189a4f545d922f79c93"

# Función para enviar notificaciones SMS
def enviar_sms(mensaje):
    payload = {
        "from": "12085813939",
        "to": [telefono],
        "body": mensaje
    }
    headers = {
        "Authorization": f"Bearer {sinch_api_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(sinch_api_url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

# Estrategia de Compra Perfecta
def analizar_compra_perfecta(ticker, time_frame):
    data = yf.download(ticker, interval=time_frame, period="7d")
    
    if data.empty:
        print(f"No hay datos para {ticker}")
        return
    
    data["EWO"] = ta.ewm(data["Close"], span=21) - ta.ewm(data["Close"], span=55)
    data["RSI"] = ta.rsi(data["Close"], length=14)
    data["MA21"] = ta.sma(data["Close"], length=21)
    data["MA55"] = ta.sma(data["Close"], length=55)

    ultima_fila = data.iloc[-1]

    if (
        ultima_fila["EWO"] > 0 and
        ultima_fila["RSI"] < 70 and
        ultima_fila["MA21"] > ultima_fila["MA55"]
    ):
        mensaje = f"¡Compra Perfecta detectada para {ticker} en el time frame {time_frame}!"
        enviar_sms(mensaje)
        print(mensaje)
    else:
        print(f"No hay señal de compra perfecta para {ticker}")

# Lista de acciones a monitorear
acciones = {"AAPL": "15m", "GOOG": "1h", "TSLA": "5m"}

while True:
    for ticker, time_frame in acciones.items():
        print(f"Monitoreando {ticker} en {time_frame}...")
        analizar_compra_perfecta(ticker, time_frame)
    time.sleep(300)  # Espera 5 minutos antes de repetir	

