import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

print("Data loaded. First rows:")
print(df.head())

# ============================================
# MISSING VALUE CHECK
# ============================================

print("\nMissing values per column:")
print(df.isna().sum())

df = df.dropna()

# ============================================
# DESCRIPTIVE STATISTICS
# ============================================

desc = df.describe().T
desc["skewness"] = df.skew()
desc["kurtosis"] = df.kurtosis()

print("\nDescriptive Statistics:")
print(desc)

desc.to_csv("data/descriptive_stats.csv")

# ============================================
# 1. PRICE TREND (TIME SERIES)
# ============================================

df[['SPY_price', 'AGG_price']].plot(title="1.Price Trend (2019–2024)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.show()

# ============================================
# 2. HISTOGRAMS OF RETURNS
# ============================================

df[['SPY_return', 'AGG_return']].hist(bins=50, figsize=(10, 5))
plt.suptitle("2.Distribution of Daily Returns (SPY & AGG)")
plt.show()

# ============================================
# 3. BOXPLOTS - OUTLIER ANALYSIS
# ============================================

plt.figure(figsize=(7,5))
sns.boxplot(data=df[['SPY_return','AGG_return']])
plt.title("3.Boxplot of Daily Returns")
plt.show()

# ============================================
# 4. SCATTER PLOT - RELATIONSHIP
# ============================================

plt.figure(figsize=(6,6))
plt.scatter(df['SPY_return'], df['AGG_return'], alpha=0.5)
plt.xlabel("SPY Daily Returns")
plt.ylabel("AGG Daily Returns")
plt.title("4.Scatter Plot: SPY vs AGG Returns")
plt.show()

# ============================================
# 5. CORRELATION HEATMAP
# ============================================

plt.figure(figsize=(5,4))
sns.heatmap(df[['SPY_return','AGG_return']].corr(), annot=True, cmap="coolwarm")
plt.title("5.Correlation Heatmap")
plt.show()

# ============================================
# 6. ROLLING VOLATILITY
# ============================================


df[['SPY_vol','AGG_vol']].plot(title="6.Rolling 20-Day Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.show()

# ============================================
# 7. MOMENTUM INDICATOR (MA20)
# ============================================

plt.figure(figsize=(10,5))
plt.plot(df.index, df['SPY_price'], label="SPY Price")
plt.plot(df.index, df['SPY_ma20'], label="SPY 20-Day MA")
plt.title("7.Momentum Indicator (MA20) for SPY")
plt.legend()
plt.show()
