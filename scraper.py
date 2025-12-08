#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import csv
import time
from datetime import datetime, time as dtime
import pytz

WIKI_URL = "https://en.wikipedia.org/wiki/NIFTY_50"
HEADERS = {"User-Agent": "Mozilla/5.0"}

IST = pytz.timezone("Asia/Kolkata")

# ----------- SCRAPE NIFTY 50 TICKERS -----------
def get_nifty50_tickers():
    r = requests.get(WIKI_URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    tickers = []
    for t in tables:
        heads = [th.get_text(strip=True).lower() for th in t.find_all("th")]
        if "symbol" in "".join(heads):
            for row in t.find_all("tr")[1:]:
                cols = [c.get_text(strip=True) for c in row.find_all("td")]
                if cols:
                    tickers.append(cols[0].upper())
            break

    return list(dict.fromkeys(tickers))


# ----------- FETCH 1-MIN INTRADAY -----------

def get_minute_value(df, target_dt):
    """Return nearest 1-min candle row"""
    if df.empty:
        return None

    df = df.copy()
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")

    df.index = df.index.tz_convert(IST)
    idx = (df.index - target_dt).abs().argmin()
    return df.iloc[idx]


# ----------- MAIN -----------

def main():
    tickers = get_nifty50_tickers()

    today = datetime.now(IST).date()
    dt_930 = IST.localize(datetime.combine(today, dtime(9, 30)))
    dt_1030 = IST.localize(datetime.combine(today, dtime(10, 30)))

    with open("intraday.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["symbol","price_930","price_1030","volume_930","volume_1030"])

        for t in tickers:
            yf_symbol = f"{t}.NS"
            try:
                data = yf.Ticker(yf_symbol).history(interval="1m", period="1d")

                r930 = get_minute_value(data, dt_930)
                r1030 = get_minute_value(data, dt_1030)

                p930 = float(r930["Close"]) if r930 is not None else ""
                p1030 = float(r1030["Close"]) if r1030 is not None else ""

                v930 = int(r930["Volume"]) if r930 is not None else ""
                v1030 = int(r1030["Volume"]) if r1030 is not None else ""

                w.writerow([t, p930, p1030, v930, v1030])

            except:
                w.writerow([t, "", "", "", ""])

            time.sleep(0.8)

    print("intraday.csv created successfully.")


if __name__ == "__main__":
    main()
