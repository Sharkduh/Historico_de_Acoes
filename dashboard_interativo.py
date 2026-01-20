import requests

API_KEY = 'VIUQ02YWJGLF43EP'
# Lista ampliada para testar a busca
SYMBOLS = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'GOOGL', 'NVDA', 'META', 'NFLX']

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

results = [get_data(s) for s in SYMBOLS]

html_content = f"""
<html>
<head>
    <title>Dashboard Pro - Jarvis</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; padding: 40px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
        #searchBar {{ 
            padding: 12px 20px; width: 300px; border-radius: 25px; border: none; 
            background: #1e293b; color: white; font-size: 16px; outline: none;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }}
        .card {{ 
            background: #1e293b; padding: 25px; border-radius: 15px; 
            text-align: center; transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-5px); }}
        .symbol {{ font-size: 1.5em; font-weight: bold; color: #38bdf8; }}
        .price {{ font-size: 22px; margin: 15px 0; color: #f8fafc; }}
        .sent-high {{ color: #4ade80; }}
        .sent-low {{ color: #fb7185; }}
        .sent-neu {{ color: #fbbf24; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Market Sentiment Dashboard</h1>
        <input type="text" id="searchBar" onkeyup="filterCards()" placeholder="Pesquisar Ticker (Ex: AAPL)...">
    </div>
    
    <div class="grid" id="cardGrid">
"""

for res in results:
    color_class = "sent-high" if res['sentiment'] > 0.15 else "sent-low" if res['sentiment'] < -0.15 else "sent-neu"
    html_content += f"""
        <div class="card" data-symbol="{res['symbol']}">
            <div class="symbol">{res['symbol']}</div>
            <div class="price">${float(res['price']):.2f}</div>
            <div class="sentiment">Sentimento: <span class="{color_class}">{res['sentiment']}</span></div>
        </div>
    """

html_content += """
    </div>

    <script>
    function filterCards() {
        let input = document.getElementById('searchBar').value.toUpperCase();
        let cards = document.getElementsByClassName('card');
        
        for (let i = 0; i < cards.length; i++) {
            let symbol = cards[i].getAttribute('data-symbol');
            if (symbol.includes(input)) {
                cards[i].style.display = "";
            } else {
                cards[i].style.display = "none";
            }
        }
    }
    </script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)

print("Dashboard com busca gerado com sucesso!")
