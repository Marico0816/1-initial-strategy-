import pandas as pd

# 读取完整交易表
df = pd.read_csv(r"D:\pythonProject1\strategy 1\final_trade_log_relative_to_QQQ.csv")

# 拆分做多和做空数据（保留 symbol）
long_trades = df[['symbol', 'buy_date', 'buy_price', 'sell_date', 'sell_price']].dropna()
short_trades = df[['symbol', 'short_sell_date', 'short_sell_price', 'buy_to_cover_date', 'buy_to_cover_price']].dropna()

# 保存为两个独立 CSV 文件
long_trades.to_csv(r"D:\pythonProject1\strategy 1\long_trades.csv", index=False)
short_trades.to_csv(r"D:\pythonProject1\strategy 1\short_trades.csv", index=False)

# 打印预览
print("做多记录示例：")
print(long_trades.head())

print("\n做空记录示例：")
print(short_trades.head())
