#!/usr/bin/env python3


import csv

def read(path):
    out=[]
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            def to_float(x):
                try: return float(x)
                except: return None
            out.append({
                "symbol": row["symbol"],
                "p930": to_float(row["price_930"]),
                "p1030": to_float(row["price_1030"]),
                "v930": to_float(row["volume_930"]),
                "v1030": to_float(row["volume_1030"])
            })
    return out


def analyze(rows):
    res=[]
    for r in rows:
        p1, p2 = r["p930"], r["p1030"]
        v1, v2 = r["v930"], r["v1030"]

        if not p1 or not p2 or not v1 or not v2:
            continue

        price_pct = ((p2 - p1) / p1) * 100
        vol_pct = ((v2 - v1) / v1) * 100

        if price_pct > 0 and vol_pct > 0:
            res.append({
                "symbol": r["symbol"],
                "pc": price_pct,
                "vc": vol_pct,
                "mom": price_pct * vol_pct
            })

    return sorted(res, key=lambda x: x["mom"], reverse=True)


def main():
    rows = read("intraday.csv")
    res = analyze(rows)

    print("Rank | Symbol | Price% | Vol% | Momentum")
    print("------------------------------------------")
    for i, r in enumerate(res, 1):
        print(i, r["symbol"], round(r["pc"],3), round(r["vc"],3), round(r["mom"],3))


if __name__=="__main__":
    main()
