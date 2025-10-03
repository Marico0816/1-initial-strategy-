from ib_insync import *
import pandas as pd
import time

# 1. 连接 TWS 实盘账户
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# 2. 加载 S&P 500 股票列表（建议提供.csv文件，或者这里写死）
symbols = [
    'QQQ'
]  # 替换为完整列表

# 3. 下载历史数据
for symbol in symbols:
    try:
        print(f"📥 正在下载：{symbol}")
        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)

        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='5 Y',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )

        df = util.df(bars)
        df.to_csv(f'sp500_data/{symbol}_history.csv', index=False)
        print(f"✅ 成功保存 {symbol}_history.csv")

        time.sleep(1.5)  # 防止请求过快被断开连接

    except Exception as e:
        print(f"❌ 失败：{symbol}，原因：{e}")

# 4. 断开连接
ib.disconnect()
