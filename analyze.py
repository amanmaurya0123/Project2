#!/usr/bin/env python3
# FULL analyze.py

import csv

def read(path):
    out=[]
    with open(path) as f:
        r=csv.DictReader(f)
        for row in r:
            try: price=float(row["price"])
            except: price=None
            try: vol=int(float(row["volume"]))
            except: vol=None
            out.append({"symbol":row["symbol"],"price":price,"vol":vol})
    return out

def analyze(rows):
    res=[]
    for r in rows:
        p=r["price"]; v=r["vol"]
        if not p or not v: continue
        p9=p*0.99
        v9=v*0.5
        pc=((p-p9)/p9)*100
        vc=((v-v9)/v9)*100
        if p>p9 and v>v9:
            res.append({
                "symbol":r["symbol"],
                "pc":pc,
                "vc":vc,
                "mom":pc*vc
            })
    return sorted(res,key=lambda x:x["mom"],reverse=True)

def main():
    rows=read("intraday.csv")
    res=analyze(rows)
    print("Rank | Symbol | Price% | Vol% | Momentum")
    print("------------------------------------------")
    for i,r in enumerate(res,1):
        print(i, r["symbol"], round(r["pc"],3), round(r["vc"],3), round(r["mom"],3))

if __name__=="__main__":
    main()
