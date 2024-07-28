from flask import Flask, request, jsonify, render_template, send_file, Blueprint
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import io

app = Flask(__name__)

API_KEY = 'YOUR_ALPHAVANTAGE_API_KEY' # alpha vantage api key
main = Blueprint('main', __name__)

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" in data:
        return data["Time Series (Daily)"]
    return None

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/get_stock_prices', methods=['POST'])
def get_stock_prices():
    symbols = request.form.get('symbols').split(',')
    result = []
    for symbol in symbols:
        data = fetch_stock_data(symbol.strip().upper())
        if data:
            latest_date = max(data.keys())
            latest_data = data[latest_date]
            result.append({
                'symbol': symbol.strip().upper(),
                'open': latest_data['1. open'],
                'high': latest_data['2. high'],
                'low': latest_data['3. low'],
                'close': latest_data['4. close']
            })
    return jsonify(prices=result)

@main.route('/get_ytd_plot', methods=['POST'])
def get_ytd_plot():
    symbols = request.form.get('symbols').split(',')
    plots = []
    plt.figure(figsize=(20, 5))
    for symbol in symbols:
        symbol = symbol.strip().upper()
        data = fetch_stock_data(symbol)
        if data:
            dates = []
            closes = []
            for date, metrics in data.items():
                dates.append(datetime.strptime(date, '%Y-%m-%d'))
                closes.append(float(metrics['4. close']))

            df = pd.DataFrame({'date': dates, 'close': closes})
            df = df.sort_values('date')
            df['YTD'] = (df['close'] / df['close'].iloc[0] - 1) * 100

            plt.plot(df['date'], df['YTD'], label=symbol)
    
    plt.xlabel('Date')
    plt.ylabel('YTD Return (%)')
    plt.title('Year-to-Date (YTD) Return')
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
