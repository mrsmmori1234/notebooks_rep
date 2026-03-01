# 監視対象の設定
# 名前: シンボル
from ast import Global


from ast import Global


TARGET_MARKETS = {
    "S&P 500": "^GSPC",
    "Nikkei 225": "^N225",
    "Gold": "GC=F",
    "VIX": "^VIX",
    "USD/JPY": "JPY=X",
    "Crude Oil": "CL=F",
    "Bitcoin": "BTC-USD",
    "Global X Cybersecurity ETF": "BUG",
    "iShares MSCI EM Latin America UCITS ETF USD D": "ILF",
    "Xtrackers MSCI India Swap UCITS 1C ETF": "INDA",
    "Global X FTSE Southeast Asia ETF": "FAS",
    "Global X Data Center & Digital Infrastructure": "DGT",
    "iShares Global Infrastructure ETF": "IGF",
    "iShares Global Healthcare (IXJ)": "IXJ",
    "Parkway Life REIT": "PWRD",
    "COPX": "COPX",
    "REMX": "REMX",
    "CIBR": "CIBR",
    "HACK": "HACK",
    "MOO": "MOO",
    "Water Related Business": "WTR"
}

# グラフの設定
PERIOD = "1mo"  # 取得期間 (1d, 5d, 1mo, 3mo, 1y, max)
INTERVAL = "1d" # 間隔 (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
SAVE_FILENAME = "market_report.png"