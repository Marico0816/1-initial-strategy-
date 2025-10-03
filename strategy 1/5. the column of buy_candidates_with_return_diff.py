import pandas as pd

# 读取 CSV 文件
stocks_df = pd.read_csv(r"D:\pythonProject1\strategy 1\filtered_high_corr_stocks.csv")
qqq_df = pd.read_csv(r"D:\pythonProject1\strategy 1\top_50_price_all price.csv")




# 提取 QQQ 行，并重命名列方便合并
qqq_df = qqq_df[qqq_df['symbol'] == 'QQQ_HISTORY'][['date', 'open1', 'end_close']]
qqq_df.rename(columns={'open1': 'qqq_open1', 'end_close': 'qqq_end_close'}, inplace=True)


# 合并两个表格，按日期对齐
merged_df = pd.merge(stocks_df, qqq_df, on='date', how='inner')

# 计算正股和QQQ的五天波动率
merged_df['stock_return'] = (merged_df['end_close'] - merged_df['open1']) / merged_df['open1']
merged_df['qqq_return'] = (merged_df['qqq_end_close'] - merged_df['qqq_open1']) / merged_df['qqq_open1']

# 计算波动率差异
merged_df['diff_ratio'] = abs(merged_df['stock_return'] - merged_df['qqq_return'])

# 筛选出波动率差异大于2%的行
filtered_df = merged_df[merged_df['diff_ratio'] > 0.01]

# 只保留需要的列
result_df = filtered_df[['date', 'symbol', 'stock_return', 'qqq_return', 'end_close']]

# 保存为 CSV 文件
result_df.to_csv("buy_candidates_with_return_diff.csv", index=False)

# 输出预览
print(result_df.head())
