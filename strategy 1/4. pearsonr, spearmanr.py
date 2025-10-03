import pandas as pd
from scipy.stats import pearsonr, spearmanr
import json

# 读取数据
df = pd.read_csv(r"D:\pythonProject1\strategy 1\top_50_price_all price.csv")

# 创建结果列表
result = []

# 按日期分组处理
for date, group in df.groupby('date'):
    # 获取QQQ数据行（symbol包含"QQQ"即可）
    qqq_row = group[group['symbol'].str.contains('QQQ', case=False)]
    if qqq_row.empty:
        continue  # 如果这天没有QQQ，跳过

    qqq_series = qqq_row.iloc[0][['open1', 'open2', 'open3', 'open4', 'open5', 'end_close']].tolist()
    if any(pd.isna(x) for x in qqq_series):
        continue  # QQQ 有缺失，跳过

    # 遍历同一天的所有其他股票
    for _, row in group.iterrows():
        if 'QQQ' in row['symbol']:
            continue  # 跳过QQQ本身

        stock_series = row[['open1', 'open2', 'open3', 'open4', 'open5', 'end_close']].tolist()
        if any(pd.isna(x) for x in stock_series):
            continue

        try:
            pearson_corr, _ = pearsonr(stock_series, qqq_series)
            spearman_corr, _ = spearmanr(stock_series, qqq_series)
        except:
            continue

        if pearson_corr > 0.9 and spearman_corr > 0.9:
            result.append({
                'date': date,
                'symbol': row['symbol'],
                'pearson_corr': round(pearson_corr, 4),
                'spearman_corr': round(spearman_corr, 4),
                'open1': row['open1'],
                'open2': row['open2'],
                'open3': row['open3'],
                'open4': row['open4'],
                'open5': row['open5'],
                'end_close': row['end_close']
            })

# 保存为 CSV
output_path = r"D:\pythonProject1\strategy 1\filtered_high_corr_stocks.csv"
pd.DataFrame(result).to_csv(output_path, index=False)
print(f"✅ 筛选完成，结果保存到：{output_path}")
