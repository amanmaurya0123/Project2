#!/usr/bin/env python3
# FULL scraper.py

import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

WIKI_URL = "https://en.wikipedia.org/wiki/NIFTY_50"
YAHOO_QUOTE_URL = "https://finance.yahoo.com/quote/{}.NS"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_nifty50_tickers():
    r = requests.get(WIKI_URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})
    tickers = []
    for t in tables:
        headers = [th.get_text(strip=True).lower() for th in t.find_all("th")]
        if "symbol" in "".join(headers):
            for row in t.find_all("tr")[1:]:
                cols = [c.get_text(strip=True) for c in row.find_all("td")]
                if cols:
                    tickers.append(cols[0].upper())
            break
    return list(dict.fromkeys(tickers))

def parse_yahoo(symbol):
    r = requests.get(YAHOO_QUOTE_URL.format(symbol), headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
    price = float(price_tag.text.replace(",", "")) if price_tag else None

    vol_tag = soup.find("td", {"data-test": "TD_VOLUME-value"})
    if vol_tag:
        txt = vol_tag.text.replace(",", "")
        if txt.endswith("M"):
            vol = int(float(txt[:-1])*1_000_000)
        elif txt.endswith("K"):
            vol = int(float(txt[:-1])*1000)
        else:
            vol = int(float(txt))
    else:
        vol = None

    return price, vol

def main():
    tickers = get_nifty50_tickers()
    with open("intraday.csv","w",newline="") as f:
        w = csv.writer(f)
        w.writerow(["symbol","price","volume","timestamp"])
        for t in tickers:
            try:
                price, vol = parse_yahoo(t)
            except:
                price, vol = None, None
            w.writerow([t, price or "", vol or "", datetime.utcnow().isoformat()])
            time.sleep(1.2)

if __name__ == "__main__":
    main()
