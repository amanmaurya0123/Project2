# Intraday Momentum Analysis Project

## Files
- **scraper.py** — Scrapes NIFTY 50 tickers + live price/volume from Yahoo Finance.
- **analyze.py** — Calculates price change %, volume change %, momentum score and ranks stocks.
- **requirements.txt** — Python dependencies.

## How to Run
```
pip install -r requirements.txt
python scraper.py
python analyze.py
```

## Output
- `intraday.csv` — Generated automatically by scraper.py
