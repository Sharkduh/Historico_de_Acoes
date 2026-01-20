import requests
import sqlite3
from datetime import datetime
import time

API_KEY = 'VIUQ02YWJGLF43EP'
SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'AMZN']

def init_db():
    conn = sqlite3.connect('market_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT, price REAL, sentiment REAL, timestamp DATETIME)''')
    conn.commit()
    return conn

def run_pipeline():
    conn = init_db()
    cursor = conn.cursor()
    
    for symbol in SYMBOLS:
        print(f"-> Coletando {symbol}...")
        try:
            # Coleta
            r = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}').json()
            price = float(r.get('Global Quote', {}).get('05. price', 0))
            
            # Persistência (Load)
            cursor.execute("INSERT INTO stocks (symbol, price, timestamp) VALUES (?, ?, ?)", 
                           (symbol, price, datetime.now()))
            conn.commit()
            
            # Análise (Transform) - Compara com a média do banco
            cursor.execute("SELECT AVG(price) FROM stocks WHERE symbol=?", (symbol,))
            avg_price = cursor.fetchone()[0]
            
            status = "ALTA" if price > avg_price else "BAIXA"
            print(f"   Status {symbol}: {status} (Atual: {price} / Média: {avg_price:.2f})")
            
        except Exception as e:
            print(f"   Erro em {symbol}: {e}")
        
        time.sleep(15)
    
    conn.close()

if __name__ == "__main__":
    run_pipeline()
    print("\n[OK] Dados salvos no SQLite e Pipeline finalizado.")
