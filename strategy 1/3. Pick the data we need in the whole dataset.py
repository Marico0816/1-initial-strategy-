import pandas as pd

# 读取文件
top50_df = pd.read_csv(r"D:\pythonProject1\strategy 1\top_50_plus_QQQ.csv", parse_dates=['end_date'])
price_df = pd.read_csv(r"D:\pythonProject1\strategy 1\sp500_merged_full_data.csv", parse_dates=['date'])

# 保留需要列
price_df = price_df[['Symbol', 'date', 'open', 'close']]
top50_df.rename(columns={'symbol': 'Symbol'}, inplace=True)

# 建立价格查找字典
price_lookup = price_df.set_index(['Symbol', 'date']).to_dict(orient='index')

# 获取全部交易日
trading_dates = sorted(price_df['date'].unique())

# 获取过去5个交易日
def get_last_5_trading_days(end_date):
    if end_date not in trading_dates:
        return None
    idx = trading_dates.index(end_date)
    if idx < 4:
        return None
    return trading_dates[idx - 4: idx + 1]

# 构建 top_50_price_info
top_50_price_info = {}

for _, row in top50_df.iterrows():
    end_date = row['end_date']
    symbol = row['Symbol']
    date_str = end_date.strftime('%Y-%m-%d')

    date_list = get_last_5_trading_days(end_date)
    if date_list is None:
        continue

    info = {'symbol': symbol}

    for i, date_i in enumerate(date_list):
        key = (symbol, date_i)
        info[f'open{i + 1}'] = price_lookup.get(key, {}).get('open', None)

    # 第5天的收盘价
    info['end_close'] = price_lookup.get((symbol, date_list[-1]), {}).get('close', None)

    top_50_price_info.setdefault(date_str, []).append(info)


import pandas as pd

# 展开 top_50_price_info 字典为列表
records = []
for date_str, stock_list in top_50_price_info.items():
    for stock in stock_list:
        record = {'date': date_str}
        record.update(stock)
        records.append(record)

# 转换为 DataFrame
df = pd.DataFrame(records)

# 保存为 CSV 文件
output_csv_path = r"D:\pythonProject1\strategy 1\top_50_price_all price.csv"
df.to_csv(output_csv_path, index=False)

print(f"✅ CSV 文件已保存：{output_csv_path}")