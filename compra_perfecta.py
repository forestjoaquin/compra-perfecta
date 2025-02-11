import yfinance as yf
import pandas as pd
import pandas_ta as ta

def analizar_compra_perfecta(ticker, time_frame):
    data = yf.download(ticker, interval=time_frame, period='7d')
    if data.empty:
        print(f"No hay datos para {ticker}.")
        return
    
    # Corrección aquí
    data['EWO'] = data['Close'].ewm(span=21, adjust=False).mean() - data['Close'].ewm(span=55, adjust=False).mean()

    ma_21 = data['Close'].ewm(span=21, adjust=False).mean()
    ma_55 = data['Close'].ewm(span=55, adjust=False).mean()
    
    if data['EWO'].iloc[-1] > 0 and ma_21.iloc[-1] > ma_55.iloc[-1]:
        print(f"¡Señal de Compra Perfecta para {ticker}!")
    else:
        print(f"No hay señal para {ticker}.")

# Ejemplo de uso
analizar_compra_perfecta('AAPL', '15m')
