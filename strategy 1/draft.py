from scipy.stats import pearsonr

x = [1, 1.1, 1.21, 1.331, 1.1979]
y = [2, 2.1, 2.205, 2.31525, 2.083725]

corr, p = pearsonr(x, y)
print(f"皮尔逊系数: {corr:.6f}")
print(f"p 值: {p:.4e}")