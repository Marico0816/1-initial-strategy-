import pandas as pd

# 1. Wikipedia 的纳斯达克100成分股链接
url = "https://en.wikipedia.org/wiki/NASDAQ-100"

# 2. 获取所有表格
tables = pd.read_html(url)

# 3. 打印所有表格的列名，找出哪张表有你要的 ticker 列
for i, table in enumerate(tables):
    print(f"\nTable {i} columns: {table.columns.tolist()}")
