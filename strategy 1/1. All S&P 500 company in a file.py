import pandas as pd
import os

# 所有 CSV 文件存放的文件夹
folder_path = r'D:\pythonProject1\database\sp500_data'

# 存储所有股票的数据
all_data = []

# 遍历文件夹中所有 CSV 文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        symbol = file_name.replace('.csv', '').upper()
        file_path = os.path.join(folder_path, file_name)

        try:
            df = pd.read_csv(file_path, parse_dates=['date'])  # 自动解析日期
            df['Symbol'] = symbol  # 添加股票名称列
            all_data.append(df)
        except Exception as e:
            print(f"读取 {file_name} 失败，原因：{e}")

# 合并为一个大表
df_all = pd.concat(all_data, ignore_index=True)

# 删除缺失值（防止部分股票少字段）
df_all = df_all.dropna()

# 输出部分数据查看
print(df_all.head())

# 保存为 CSV 文件
df_all.to_csv('sp500_merged_full_data.csv', index=False)
