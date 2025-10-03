import pandas as pd

# 读取数据
signal_df = pd.read_csv(r"D:\pythonProject1\strategy 1\buy_candidates_with_return_diff.csv")
price_df = pd.read_csv(r"D:\pythonProject1\strategy 1\expanded_trade_6days_rows.csv")

# 日期格式处理
signal_df['date'] = pd.to_datetime(signal_df['date']).dt.date
price_df['date'] = pd.to_datetime(price_df['date']).dt.date

results = []

for _, row in signal_df.iterrows():
    symbol = row['symbol']
    start_date = row['date']
    entry_price = row['end_close']
    stock_return = row['stock_return']
    qqq_return = row['qqq_return']

    # 提取正股的未来4天价格
    stock_future = price_df[(price_df['symbol'] == symbol) & (price_df['date'] > start_date)].sort_values('date').head(4)

    # 提取QQQ的未来4天价格
    qqq_future = price_df[(price_df['symbol'] == 'QQQ_HISTORY') & (price_df['date'] > start_date)].sort_values('date').head(4)

    exit_price = None
    exit_date = None

    for i in range(min(len(stock_future), len(qqq_future))):
        stock_day = stock_future.iloc[i]
        qqq_day = qqq_future.iloc[i]

        stock_ratio = (stock_day['close'] - entry_price) / entry_price
        qqq_entry = qqq_future.iloc[0]['close']  # QQQ开仓日价格
        qqq_ratio = (qqq_day['close'] - qqq_entry) / qqq_entry

        if stock_return < qqq_return:
            # 做多逻辑：QQQ 涨得比正股多 → 平仓
            if qqq_ratio > stock_ratio:
                exit_price = stock_day['close']
                exit_date = stock_day['date']
                break
        else:
            # 做空逻辑：QQQ 跌得比正股多 → 平仓
            if qqq_ratio < stock_ratio:
                exit_price = stock_day['close']
                exit_date = stock_day['date']
                break

    # 如果未触发止盈，则第4天强平
    if exit_price is None and not stock_future.empty:
        last_day = stock_future.iloc[-1]
        exit_price = last_day['close']
        exit_date = last_day['date']

    if stock_return < qqq_return:
        # 做多记录
        results.append({
            'symbol': symbol,
            'buy_date': start_date,
            'buy_price': entry_price,
            'sell_date': exit_date,
            'sell_price': exit_price
        })
    else:
        # 做空记录
        results.append({
            'symbol': symbol,
            'short_sell_date': start_date,
            'short_sell_price': entry_price,
            'buy_to_cover_date': exit_date,
            'buy_to_cover_price': exit_price
        })

# 保存结果
result_df = pd.DataFrame(results)
result_df.to_csv(r"D:\pythonProject1\strategy 1\final_trade_log_relative_to_QQQ.csv", index=False)
print(result_df.head())
