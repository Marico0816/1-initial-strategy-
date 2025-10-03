import pandas as pd

# 读取原始信号和价格数据
signal_df = pd.read_csv(r"D:\pythonProject1\strategy 1\buy_candidates_with_return_diff.csv")
price_df = pd.read_csv(r"D:\pythonProject1\strategy 1\sp500_merged_full_data.csv")

# 格式处理
signal_df['date'] = pd.to_datetime(signal_df['date']).dt.date
price_df['date'] = pd.to_datetime(price_df['date']).dt.date
price_df.rename(columns={'Symbol': 'symbol'}, inplace=True)
price_df.sort_values(['symbol', 'date'], inplace=True)

# 提取 QQQ 收盘价
qqq_df = price_df[price_df['symbol'] == 'QQQ_HISTORY'][['date', 'close']]
qqq_df.rename(columns={'close': 'qqq_close'}, inplace=True)

# 分组股票数据用于快速索引
grouped = price_df.groupby('symbol')

expanded_rows = []

# 遍历每一个信号（symbol + 起始日期）
for _, row in signal_df.iterrows():
    symbol = row['symbol']
    base_date = row['date']

    if symbol not in grouped.groups:
        continue

    symbol_data = grouped.get_group(symbol).reset_index(drop=True)
    idx_list = symbol_data[symbol_data['date'] == base_date].index.tolist()
    if not idx_list:
        continue
    idx = idx_list[0]

    # 提取该股票未来6天数据（含当天）
    if idx + 5 < len(symbol_data):
        future_rows = symbol_data.loc[idx:idx + 5]
        expanded_rows.extend(future_rows.to_dict(orient='records'))

# 转为 DataFrame
expanded_df = pd.DataFrame(expanded_rows)

# 合并对应日期的 QQQ 收盘价
expanded_df = expanded_df.merge(qqq_df, on='date', how='left')

# 输出保存
expanded_df.to_csv(r"D:\pythonProject1\strategy 1\expanded_trade_6days_with_qqq.csv", index=False)

# 打印预览
print(expanded_df.head())
