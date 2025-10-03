import pandas as pd

# 第一步：读取数据
file_path = r"D:\pythonProject1\strategy 1\sp500_merged_full_data.csv"
df = pd.read_csv(file_path, parse_dates=['date'])

# 筛选日期范围
df = df[(df['date'] >= '2020-01-01') & (df['date'] <= '2025-07-11')]

# 确保排序正确（按公司+日期）
df = df.sort_values(by=['Symbol', 'date'])

# 用 rolling 滚动计算每家公司 5 天交易金额总和（volume × average）
result_list = []

for symbol, group in df.groupby('Symbol'):
    group = group.sort_values('date')
    group['value'] = group['volume'] * group['average']
    group['value_sum'] = group['value'].rolling(window=5).sum()
    group = group.dropna(subset=['value_sum'])

    for _, row in group.iterrows():
        result_list.append({
            'end_date': row['date'].strftime('%Y-%m-%d'),
            'value_sum': row['value_sum'],
            'symbol': symbol
        })

# 转为 DataFrame
rolling_df = pd.DataFrame(result_list)

# 每天选出成交金额最大的前 50 家公司
top_50_per_day = (
    rolling_df
    .groupby('end_date', group_keys=False)
    .apply(lambda x: x.nlargest(50, 'value_sum'))
    .reset_index(drop=True)
)

# 按日期和成交金额排序
top_50_per_day = top_50_per_day.sort_values(by=['end_date', 'value_sum'], ascending=[True, False])


# 接下来：提取所有 QQQ 的 value_sum 数据
qqq_data = rolling_df[rolling_df['symbol'] == 'QQQ']

# 合并 QQQ 数据和 top 50 数据
combined = pd.concat([top_50_per_day, qqq_data])

# 对每个日期，保留前 50 大以及 QQQ（即使 QQQ 不在前 50）
# 方法是：对每个日期按 value_sum 排序，保留所有 QQQ + 前 50
def ensure_qqq(df):
    if 'QQQ' in df['symbol'].values:
        # 如果 QQQ 已在其中，就直接取前 50
        return df.sort_values('value_sum', ascending=False).head(50)
    else:
        # 如果 QQQ 不在，就额外加入 QQQ，再取前 50 + QQQ
        qqq_row = qqq_data[qqq_data['end_date'] == df['end_date'].iloc[0]]
        df = pd.concat([df, qqq_row], ignore_index=True)
        return df.sort_values('value_sum', ascending=False).drop_duplicates('symbol').head(51)

final_df = (
    combined
    .groupby('end_date', group_keys=False)
    .apply(ensure_qqq)
    .reset_index(drop=True)
)

# 最终排序
final_df = final_df.sort_values(by=['end_date', 'value_sum'], ascending=[True, False])

# 保存结果
final_output_path = r"D:\pythonProject1\strategy 1\top_50_plus_QQQ.csv"
final_df.to_csv(final_output_path, index=False)

print("包含 QQQ 的文件保存成功，预览前几行：")
print(final_df.head(100))


