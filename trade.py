import requests

API_KEY = 'VIUQ02YWJGLF43EP'
SYMBOL = 'AAPL'

def get_market_analysis():
    # 1. Pegar Preço Atual
    url_p = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={SYMBOL}&apikey={API_KEY}'
    price_data = requests.get(url_p).json().get('Global Quote', {})
    
    if not price_data:
        return "Erro: Verifique sua cota de API ou o Ticker."

    price = float(price_data['05. price'])

    # 2. Pegar Sentimento das Notícias
    url_s = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={SYMBOL}&apikey={API_KEY}'
    sent_data = requests.get(url_s).json()
    
    feed = sent_data.get('feed', [])
    if feed:
        scores = [float(news['overall_sentiment_score']) for news in feed[:5]]
        avg_sent = sum(scores) / len(scores)
    else:
        avg_sent = 0

    # 3. Resultado
    print(f"\n--- RELATÓRIO {SYMBOL} ---")
    print(f"Preço: ${price}")
    print(f"Sentimento (0 a 1): {avg_sent:.2f}")
    
    if avg_sent > 0.15:
        return "SINAL: COMPRA (Sentimento Otimista)"
    elif avg_sent < -0.15:
        return "SINAL: VENDA (Sentimento Pessimista)"
    else:
        return "SINAL: NEUTRO"

if __name__ == "__main__":
    print(get_market_analysis())
