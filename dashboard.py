import requests

API_KEY = 'VIUQ02YWJGLF43EP'
SYMBOLS = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'GOOGL']

def get_data(symbol):
    url_p = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    price_data = requests.get(url_p).json().get('Global Quote', {})
    price = price_data.get('05. price', '0.00')

    url_s = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={API_KEY}'
    sent_data = requests.get(url_s).json()
    feed = sent_data.get('feed', [])
    scores = [float(news['overall_sentiment_score']) for news in feed[:10]]
    avg_sent = sum(scores) / len(scores) if scores else 0
    return {"symbol": symbol, "price": price, "sentiment": round(avg_sent, 2)}

# Coletando dados para todas as empresas
results = [get_data(s) for s in SYMBOLS]

# Gerando o Dashboard em HTML
html_content = f"""
<html>
<head>
    <title>Dashboard Financeiro do Jarvis</title>
    <style>
        body {{ font-family: sans-serif; background: #121212; color: white; padding: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .card {{ background: #1e1e1e; padding: 20px; border-radius: 10px; border-top: 5px solid #00ff00; text-align: center; }}
        .price {{ font-size: 24px; font-weight: bold; margin: 10px 0; }}
        .sent-high {{ color: #00ff00; }}
        .sent-low {{ color: #ff4444; }}
        .sent-neu {{ color: #ffff00; }}
    </style>
</head>
<body>
    <h1>Dashboard de Sentimento de Mercado</h1>
    <div class="grid">
"""

for res in results:
    color_class = "sent-high" if res['sentiment'] > 0.15 else "sent-low" if res['sentiment'] < -0.15 else "sent-neu"
    html_content += f"""
        <div class="card">
            <h2>{res['symbol']}</h2>
            <div class="price">${res['price']}</div>
            <div class="sentiment">Sentimento: <span class="{color_class}">{res['sentiment']}</span></div>
        </div>
    """

html_content += "</div></body></html>"

with open("index.html", "w") as f:
    f.write(html_content)

print("Dashboard gerado com sucesso em index.html!")
