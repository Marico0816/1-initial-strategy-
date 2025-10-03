import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(url, header=0)[0]  # 获取成分股表格
symbols = table['Symbol'].tolist()
print(f"共计 {len(symbols)} 支股票")

# 如果你需要保存为 CSV 文件：
pd.DataFrame({'Symbol': symbols}).to_csv('sp500_tickers_full.csv', index=False)
