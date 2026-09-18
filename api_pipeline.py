import requests
import pandas as pd
import sqlite3
from datetime import datetime

def fetch_live_financial_data():
    # Fetch live USD to INR conversion rate
    print(f"[{datetime.now()}] Fetching live Forex exchange rate (USD -> INR)...")
    forex_url = "https://api.exchangerate-api.com/v4/latest/USD"
    forex_response = requests.get(forex_url).json()
    usd_to_inr_rate = forex_response['rates']['INR']
    print(f"Real-time Exchange Rate: 1 USD = {usd_to_inr_rate} INR")


    # Fetch Live Crypto Data
    print(f"[{datetime.now()}] Fetching live Crypto market data...")
    crypto_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False #sparkline is an array of 168 numbers representing the price of the coin every hour for the past 7 days.
    }
    crypto_response = requests.get(crypto_url, params=params).json()


    # Load into Pandas and filter columns
    df = pd.DataFrame(crypto_response)
    columns_to_keep = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']
    df = df[columns_to_keep]
    df = df.rename(columns={'current_price': 'price_usd'})



    # Converting USD to INR in Real-time
    df['price_inr'] = df['price_usd'] * usd_to_inr_rate


    # Audit_Metadata
    df['forex_rate_used'] = usd_to_inr_rate
    df['pipeline_run_time'] = datetime.now()

    print("\nData successfully extracted and transformed!")
    print(df[['symbol', 'price_usd', 'price_inr', 'forex_rate_used']].head())

    return df

def load_data_to_sqlite(df):
    if df is not None:
        conn = sqlite3.connect('crypto_historical_data.db')
        df.to_sql('market_data', conn, if_exists='append', index=False)
        total_rows = pd.read_sql('SELECT COUNT(*) FROM market_data', conn).iloc[0,0]
        print(f"\nSuccess! Database now contains {total_rows} total rows.")
        conn.close()

if __name__ == "__main__":
    live_data = fetch_live_financial_data()
    load_data_to_sqlite(live_data)