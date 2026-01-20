import sqlite3
import json

# Dados Históricos que você pediu (Jarvis Knowledge)
HISTORICAL = {
    'AAPL': {'l24': 97.0, 'l25': 105.2, 'c24': 268.0, 'c25': 282.0},
    'GOOGL': {'l24': 73.8, 'l25': 88.5, 'c24': 212.0, 'c25': 225.0},
    'MSFT': {'l24': 88.1, 'l25': 102.3, 'c24': 145.0, 'c25': 160.0},
    'NVDA': {'l24': 29.7, 'l25': 65.4, 'c24': 18.0, 'c25': 25.0},
    'AMZN': {'l24': 30.4, 'l25': 42.1, 'c24': 545.0, 'c25': 570.0}
}

def generate():
    conn = sqlite3.connect('market_data.db')
    cursor = conn.cursor()
    
    html_content = """
    <html>
    <head>
        <title>Terminal de Análise de Mercado</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: 'Inter', sans-serif; background: #0b0f19; color: #e2e8f0; padding: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
            .card { background: #161e2e; border-radius: 12px; padding: 20px; border: 1px solid #2d3748; }
            .header { border-bottom: 2px solid #1e293b; margin-bottom: 20px; padding-bottom: 10px; }
            .status-up { color: #34d399; font-weight: bold; }
            .status-down { color: #fb7185; font-weight: bold; }
            .chart-box { height: 250px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="header"><h1>Análise de Mercado - BI Engine</h1></div>
        <div class="grid">
    """

    for symbol, data in HISTORICAL.items():
        # Busca o dado mais recente e a média no SQL
        cursor.execute("SELECT price FROM stocks WHERE symbol=? ORDER BY timestamp DESC LIMIT 1", (symbol,))
        last_price = cursor.fetchone()
        last_price = last_price[0] if last_price else 0
        
        cursor.execute("SELECT AVG(price) FROM stocks WHERE symbol=?", (symbol,))
        avg_price = cursor.fetchone()[0] or 0
        
        status_class = "status-up" if last_price >= avg_price else "status-down"
        diff = ((last_price - avg_price) / avg_price * 100) if avg_price > 0 else 0

        html_content += f"""
        <div class="card">
            <h2 style="color:#38bdf8; margin:0;">{symbol}</h2>
            <p>Preço Atual: <strong>${last_price:.2f}</strong></p>
            <p>Performance vs Média Banco: <span class="{status_class}">{diff:+.2f}%</span></p>
            <div class="chart-box"><canvas id="chart-{symbol}"></canvas></div>
        </div>
        <script>
            new Chart(document.getElementById('chart-{symbol}'), {{
                type: 'bar',
                data: {{
                    labels: ['Lucro (Bi)', 'Custos (Bi)'],
                    datasets: [
                        {{ label: '2024', data: [{data['l24']}, {data['c24']}], backgroundColor: '#475569' }},
                        {{ label: '2025', data: [{data['l25']}, {data['c25']}], backgroundColor: '#38bdf8' }}
                    ]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ labels: {{ color: '#fff' }} }} }} }}
            }});
        </script>
        """

    html_content += "</div></body></html>"
    with open("index.html", "w") as f: f.write(html_content)
    conn.close()
    print("Dashboard de BI gerado com sucesso!")

if __name__ == "__main__":
    generate()
