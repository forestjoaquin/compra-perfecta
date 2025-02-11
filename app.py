from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd
from datetime import datetime

app = Flask(__name__)
monitored_stocks = {}

def analyze_stock(ticker, time_frame):
    try:
        data = yf.download(ticker, period='1mo', interval=time_frame)
        if data.empty:
            return {"ticker": ticker, "message": "No data found"}

        latest_price = data['Close'].iloc[-1]
        previous_price = data['Close'].iloc[-2] if len(data) > 1 else latest_price
        change_percent = ((latest_price - previous_price) / previous_price) * 100

        signal = "BUY" if change_percent > 0 else "SELL"
        return {
            "ticker": ticker,
            "signal": signal,
            "price": round(latest_price, 2),
            "change_percent": round(change_percent, 2),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

@app.route('/')
def home():
    return "Perfect Buy App is Running!"

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    data = request.json
    ticker = data.get('ticker').upper()
    time_frame = data.get('time_frame')

    if not ticker or not time_frame:
        return jsonify({"error": "Ticker and time frame are required"}), 400

    result = analyze_stock(ticker, time_frame)
    monitored_stocks[ticker] = {
        "time_frame": time_frame,
        "start_price": result.get('price'),
        "start_time": result.get('timestamp')
    }
    return jsonify(result)

@app.route('/status', methods=['GET'])
def get_status():
    status_report = []
    for ticker, info in monitored_stocks.items():
        current_info = analyze_stock(ticker, info['time_frame'])
        gain = round(current_info['price'] - info['start_price'], 2)
        gain_percent = round((gain / info['start_price']) * 100, 2)
        status_report.append({
            "ticker": ticker,
            "start_price": info['start_price'],
            "current_price": current_info['price'],
            "gain": gain,
            "gain_percent": gain_percent,
            "start_time": info['start_time'],
            "last_checked": current_info['timestamp']
        })
    return jsonify(status_report)

@app.route('/remove_stock', methods=['POST'])
def remove_stock():
    data = request.json
    ticker = data.get('ticker').upper()
    if ticker in monitored_stocks:
        del monitored_stocks[ticker]
        return jsonify({"message": f"{ticker} removed from monitoring"}), 200
    return jsonify({"error": f"{ticker} not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
