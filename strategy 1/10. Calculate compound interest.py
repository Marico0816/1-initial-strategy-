import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv("long_trades.csv")
df["buy_date"] = pd.to_datetime(df["buy_date"])
df["sell_date"] = pd.to_datetime(df["sell_date"])
df = df.sort_values(by="buy_date").reset_index(drop=True)

# 初始化参数
initial_capital = 1000.0
capital = initial_capital
last_sell_date = pd.Timestamp.min
capital_evolution = []

# 按条件计算复利
for index, row in df.iterrows():
    if row["buy_date"] > last_sell_date:
        shares_bought = capital / row["buy_price"]
        proceeds = shares_bought * row["sell_price"]
        capital = proceeds
        last_sell_date = row["sell_date"]
        capital_evolution.append({
            "trade": index + 1,
            "symbol": row["symbol"],
            "buy_date": row["buy_date"].date(),
            "sell_date": row["sell_date"].date(),
            "buy_price": row["buy_price"],
            "sell_price": row["sell_price"],
            "capital": capital
        })

# 转换为 DataFrame
capital_df = pd.DataFrame(capital_evolution)

# 绘制图表
plt.figure(figsize=(10, 6))
plt.plot(capital_df["sell_date"], capital_df["capital"], marker='o', linestyle='-')
plt.title("Capital Growth Over Time (Compounded Trades)")
plt.xlabel("Sell Date")
plt.ylabel("Capital")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ===================== 计算关键指标 & 导出 =====================

import numpy as np

# 1) 逐笔收益率（做多：sell/buy - 1）
capital_df["ret_trade"] = capital_df["sell_price"] / capital_df["buy_price"] - 1.0

# 2) 构造按日权益曲线（在每个sell_date打点，其它日期前向填充）
#    起点放在第一笔买入前一天，数值是 initial_capital
if not capital_df.empty:
    start_day = pd.to_datetime(capital_df["buy_date"].iloc[0]) - pd.Timedelta(days=1)
    equity_points = pd.DataFrame({
        "date": [start_day] + list(pd.to_datetime(capital_df["sell_date"])),
        "equity": [initial_capital] + list(capital_df["capital"])
    }).set_index("date").sort_index()

    # 变成日频并向前填充
    daily_eq = equity_points.resample("D").ffill()
else:
    daily_eq = pd.DataFrame(columns=["equity"])

# 3) 基于“日频权益”计算指标
def perf_metrics(daily_equity: pd.DataFrame, risk_free=0.0):
    if daily_equity.empty:
        return {}

    eq = daily_equity["equity"].astype(float)
    rets = eq.pct_change().dropna()  # 日收益率
    if rets.empty:
        return {}

    days = (eq.index[-1] - eq.index[0]).days or 1
    ann_factor = 252  # 交易日年化因子

    # CAGR（按自然日计算）
    cagr = (eq.iloc[-1] / eq.iloc[0]) ** (365.25 / days) - 1

    vol = rets.std() * np.sqrt(ann_factor)
    sharpe = (rets.mean() * ann_factor - risk_free) / vol if vol > 0 else np.nan

    downside = rets[rets < 0].std() * np.sqrt(ann_factor)
    sortino = (rets.mean() * ann_factor - risk_free) / downside if downside > 0 else np.nan

    # 最大回撤
    rolling_max = eq.cummax()
    dd = eq / rolling_max - 1.0
    max_dd = float(dd.min())
    dd_end = dd.idxmin()
    dd_start = eq[:dd_end].idxmax() if not eq[:dd_end].empty else None

    return {
        "Start Date": eq.index[0].date(),
        "End Date": eq.index[-1].date(),
        "Start Equity": float(eq.iloc[0]),
        "End Equity": float(eq.iloc[-1]),
        "Total Return": float(eq.iloc[-1] / eq.iloc[0] - 1),
        "CAGR": float(cagr),
        "Annualized Volatility": float(vol),
        "Sharpe": float(sharpe),
        "Sortino": float(sortino),
        "Max Drawdown": max_dd,
        "Drawdown Start": dd_start.date() if dd_start is not None else None,
        "Drawdown End": dd_end.date() if dd_end is not None else None,
        "Num Trades": int(len(capital_df)),
        "Win Rate": float((capital_df["ret_trade"] > 0).mean()) if len(capital_df) else np.nan,
        "Avg Win": float(capital_df.loc[capital_df["ret_trade"] > 0, "ret_trade"].mean()) if (capital_df["ret_trade"] > 0).any() else np.nan,
        "Avg Loss": float(capital_df.loc[capital_df["ret_trade"] <= 0, "ret_trade"].mean()) if (capital_df["ret_trade"] <= 0).any() else np.nan,
    }

metrics = perf_metrics(daily_eq)
print("\n==== Strategy Performance ====")
for k, v in metrics.items():
    if isinstance(v, float):
        print(f"{k:>22}: {v:.4f}")
    else:
        print(f"{k:>22}: {v}")

# 4) 保存按日权益和图像
daily_eq.to_csv("equity_curve_daily.csv")
plt.figure(figsize=(10, 4.5))
daily_eq["equity"].plot()
plt.title("Strategy Equity Curve (Daily, F-fill between exits)")
plt.xlabel("Date"); plt.ylabel("Equity")
plt.tight_layout()
plt.savefig("equity_curve.png", dpi=180)
print("\n已保存：equity_curve_daily.csv, equity_curve.png")

