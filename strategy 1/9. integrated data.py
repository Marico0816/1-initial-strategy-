import pandas as pd

# 读取做多和做空文件
long_df = pd.read_csv("long_trades.csv")
short_df = pd.read_csv("short_trades.csv")

# 做多盈亏计算
long_df['profit'] = long_df['sell_price'] - long_df['buy_price']
long_stats = {
    "类型": "做多 (Long)",
    "交易数": len(long_df),
    "胜率": f"{(long_df['profit'] > 0).mean():.2%}",
    "平均收益": round(long_df['profit'].mean(), 4),
    "平均盈利": round(long_df[long_df['profit'] > 0]['profit'].mean(), 4),
    "平均亏损": round(long_df[long_df['profit'] <= 0]['profit'].mean(), 4)
}

# 做空盈亏计算
short_df['profit'] = short_df['short_sell_price'] - short_df['buy_to_cover_price']
short_stats = {
    "类型": "做空 (Short)",
    "交易数": len(short_df),
    "胜率": f"{(short_df['profit'] > 0).mean():.2%}",
    "平均收益": round(short_df['profit'].mean(), 4),
    "平均盈利": round(short_df[short_df['profit'] > 0]['profit'].mean(), 4),
    "平均亏损": round(short_df[short_df['profit'] <= 0]['profit'].mean(), 4)
}

# 合并结果并输出为 DataFrame
summary_df = pd.DataFrame([long_stats, short_stats])

# 保存为 CSV 文件
summary_df.to_csv("long_short_trade_stats.csv", index=False)

# 预览输出
print(summary_df)
