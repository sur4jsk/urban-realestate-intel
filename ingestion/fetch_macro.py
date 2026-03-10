import yfinance as yf
import pandas as pd
from datetime import datetime, timezone

def fetch_macro_data():
    # 10-year bond yields as proxy for interest rates
    india_proxy = yf.Ticker("^NSEI")   # Nifty 50
    dubai_proxy = yf.Ticker("EEM")     # Emerging markets ETF as Gulf proxy

    india_hist = india_proxy.history(period="1y")[['Close']].rename(columns={'Close': 'index_value'})
    india_hist['market'] = 'bangalore'
    india_hist['fetched_at'] = datetime.now(timezone.utc)

    dubai_hist = dubai_proxy.history(period="1y")[['Close']].rename(columns={'Close': 'index_value'})
    dubai_hist['market'] = 'dubai'
    dubai_hist['fetched_at'] = datetime.now(timezone.utc)

    combined = pd.concat([india_hist, dubai_hist]).reset_index()
    combined.columns = [c.lower() for c in combined.columns]
    return combined

if __name__ == "__main__":
    from db.loader import load_dataframe
    df = fetch_macro_data()
    print(df.head(10))
    print(f"\nFetched {len(df)} rows")
    load_dataframe(df, "macro_indicators")