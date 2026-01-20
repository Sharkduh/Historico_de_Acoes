import requests
import json
import time

API_KEY = 'VIUQ02YWJGLF43EP'
SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'AMZN']

# Base de Dados Históricos (Jarvis Knowledge 2024-2025)
HISTORICAL = {
    'AAPL': {'l24': 97.0, 'l25': 105.2, 'c24': 268.0, 'c25': 282.0},
    'GOOGL': {'l24': 73.8, 'l25': 88.5, 'c24': 212.0, 'c25': 225.0},
    'MSFT': {'l24': 88.1, 'l25': 102.3, 'c24': 145.0, 'c25': 160.0},
    'NVDA': {'l24': 29.7, 'l25': 65.4, 'c24': 18.0, 'c25': 25.0},
    'AMZN': {'l24': 30.4, 'l25': 42.1, 'c24': 545.0, 'c25': 570.0}
}

def get_data(symbol):
    print(f"Sincronizando {symbol} (API + Histórico)...")
    # API: Cotação
    price_r = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}').json()
    quote = price_r.get('Global Quote', {})
    
    # API: Fundamentalista
    fund_r = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}').json()
    
    # API: Sentimento
    sent_r = requests.get(f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={API_KEY}').json()
    feed = sent_r.get('feed', [])
    avg_sent = sum([float(n['overall_sentiment_score']) for n in feed[:5]]) / 5 if feed else 0

    h = HISTORICAL.get(symbol, {'l24':0, 'l25':0, 'c24':0, 'c25':0})
    growth = ((h['l25'] - h['l24']) / h['l24']) * 100 if h['l24'] > 0 else 0

    return {
        "symbol": symbol,
        "price": quote.get('05. price', '0.00'),
        "change": quote.get('10. change percent', '0%'),
        "pe": fund_r.get('PERatio', 'N/A'),
        "sent": round(avg_sent, 2),
        "growth": round(growth, 1),
        "l24": h['l24'], "l25": h['l25'],
        "c24": h['c24'], "c25": h['c25']
    }

results = []
for s in SYMBOLS:
    results.append(get_data(s))
    time.sleep(15) # Respeitando limite da API gratuita

html_content = f"""
<html>
<head>
    <title>Análise de Mercado</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: #f1f5f9; padding: 20px; }}
        .container {{ max-width: 1200px; margin: auto; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid #334155; padding-bottom: 20px; }}
        #search {{ padding: 10px 20px; border-radius: 20px; border: none; background: #1e293b; color: white; width: 300px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2); }}
        .stats {{ display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 0.9em; }}
        .chart-container {{ height: 220px; }}
        .growth {{ color: #4ade80; font-weight: bold; background: rgba(74, 222, 128, 0.1); padding: 2px 8px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Análise de Mercado</h1>
            <input type="text" id="search" onkeyup="filter()" placeholder="Buscar ação...">
        </div>
        <div class="grid" id="cardGrid">
"""

for r in results:
    html_content += f"""
        <div class="card" data-symbol="{r['symbol']}">
            <div class="stats">
                <h2 style="margin:0; color:#38bdf8;">{r['symbol']}</h2>
                <span class="growth">▲ {r['growth']}% Lucro</span>
            </div>
            <div class="stats">
                <span>Preço: <strong>${float(r['price']):.2f}</strong> ({r['change']})</span>
                <span>P/E: <strong>{r['pe']}</strong> | Sent: <strong>{r['sent']}</strong></span>
            </div>
            <div class="chart-container">
                <canvas id="chart-{r['symbol']}"></canvas>
            </div>
        </div>
        <script>
            new Chart(document.getElementById('chart-{r['symbol']}'), {{
                type: 'bar',
                data: {{
                    labels: ['Lucro 24x25 (Bi)', 'Custos 24x25 (Bi)'],
                    datasets: [
                        {{ label: '2024', data: [{r['l24']}, {r['c24']}], backgroundColor: '#64748b' }},
                        {{ label: '2025', data: [{r['l25']}, {r['c25']}], backgroundColor: '#38bdf8' }}
                    ]
                }},
                options: {{ 
                    responsive: true, maintainAspectRatio: false,
                    plugins: {{ legend: {{ labels: {{ color: '#fff' }} }} }},
                    scales: {{ y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }}, x: {{ ticks: {{ color: '#94a3b8' }} }} }}
                }}
            }});
        </script>
    """

html_content += """
        </div>
    </div>
    <script>
    function filter() {
        let val = document.getElementById('search').value.toUpperCase();
        let cards = document.getElementsByClassName('card');
        for (let card of cards) {
            card.style.display = card.dataset.symbol.includes(val) ? "" : "none";
        }
    }
    </script>
</body>
</html>
"""

with open("index.html", "w") as f: f.write(html_content)
print("Terminal de Mercado Pronto! Abra o index.html")
