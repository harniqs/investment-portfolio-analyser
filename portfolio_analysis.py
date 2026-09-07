import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. PORTFOLIO SETTINGS
# --------------------------------------------------

tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"]

start_date = "2024-01-01"
end_date = "2026-01-01"

risk_free_rate = 0.04
initial_investment = 10000


# --------------------------------------------------
# 2. DOWNLOAD HISTORICAL MARKET DATA
# --------------------------------------------------

data = yf.download(
    tickers,
    start=start_date,
    end=end_date,
    auto_adjust=True,
    progress=False
)


# Extract closing prices
closing_prices = data["Close"]

# Keep columns in the same order as our ticker list
closing_prices = closing_prices[tickers]


# --------------------------------------------------
# 3. CALCULATE DAILY RETURNS
# --------------------------------------------------

daily_returns = closing_prices.pct_change().dropna()


# --------------------------------------------------
# 4. INDIVIDUAL STOCK METRICS
# --------------------------------------------------

# Annualised return
annual_returns = daily_returns.mean() * 252

# Annualised volatility
annual_volatility = daily_returns.std() * np.sqrt(252)

# Sharpe ratio
sharpe_ratio = (
    annual_returns - risk_free_rate
) / annual_volatility


# --------------------------------------------------
# 5. MAXIMUM DRAWDOWN FOR EACH STOCK
# --------------------------------------------------

cumulative_returns = (1 + daily_returns).cumprod()

running_max = cumulative_returns.cummax()

drawdown = cumulative_returns / running_max - 1

max_drawdown = drawdown.min()


# --------------------------------------------------
# 6. STOCK SUMMARY TABLE
# --------------------------------------------------

summary = pd.DataFrame({
    "Annual Return": annual_returns,
    "Annual Volatility": annual_volatility,
    "Sharpe Ratio": sharpe_ratio,
    "Maximum Drawdown": max_drawdown
})

print("\nStock Summary")
print("-" * 60)
print(summary.round(4))


# --------------------------------------------------
# 7. CREATE EQUAL-WEIGHT PORTFOLIO
# --------------------------------------------------

# Automatically creates equal weights
weights = pd.Series(
    1 / len(tickers),
    index=tickers
)

print("\nPortfolio Weights")
print("-" * 40)
print(weights)


# --------------------------------------------------
# 8. PORTFOLIO RETURN
# --------------------------------------------------

portfolio_return = (
    annual_returns * weights
).sum()


# --------------------------------------------------
# 9. PORTFOLIO VOLATILITY
# --------------------------------------------------

covariance_matrix = daily_returns.cov() * 252

portfolio_variance = weights.dot(
    covariance_matrix.dot(weights)
)

portfolio_volatility = np.sqrt(
    portfolio_variance
)


# --------------------------------------------------
# 10. PORTFOLIO SHARPE RATIO
# --------------------------------------------------

portfolio_sharpe = (
    portfolio_return - risk_free_rate
) / portfolio_volatility


# --------------------------------------------------
# 11. PORTFOLIO DAILY RETURNS AND GROWTH
# --------------------------------------------------

portfolio_daily_returns = daily_returns.dot(weights)

portfolio_growth = (
    (1 + portfolio_daily_returns).cumprod()
    * initial_investment
)


# --------------------------------------------------
# 12. PORTFOLIO CAGR
# --------------------------------------------------

years = (
    portfolio_growth.index[-1]
    - portfolio_growth.index[0]
).days / 365.25

portfolio_cagr = (
    portfolio_growth.iloc[-1]
    / initial_investment
) ** (1 / years) - 1


# --------------------------------------------------
# 13. PORTFOLIO MAXIMUM DRAWDOWN
# --------------------------------------------------

portfolio_running_max = portfolio_growth.cummax()

portfolio_drawdown = (
    portfolio_growth
    / portfolio_running_max
) - 1

portfolio_max_drawdown = portfolio_drawdown.min()


# --------------------------------------------------
# 14. DISPLAY PORTFOLIO RESULTS
# --------------------------------------------------

print("\nEqual-Weight Portfolio")
print("-" * 40)

print(f"Annualised Return: {portfolio_return:.2%}")
print(f"CAGR: {portfolio_cagr:.2%}")
print(f"Annualised Volatility: {portfolio_volatility:.2%}")
print(f"Sharpe Ratio: {portfolio_sharpe:.2f}")
print(f"Maximum Drawdown: {portfolio_max_drawdown:.2%}")


# --------------------------------------------------
# 15. CORRELATION MATRIX
# --------------------------------------------------

correlation_matrix = daily_returns.corr()

print("\nCorrelation Matrix")
print("-" * 40)
print(correlation_matrix.round(2))


# --------------------------------------------------
# 16. PORTFOLIO GROWTH CHART
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    portfolio_growth.index,
    portfolio_growth
)

plt.title(
    f"Growth of ${initial_investment:,.0f} Equal-Weight Portfolio"
)

plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.grid(True)

plt.tight_layout()
plt.show()


# --------------------------------------------------
# 17. RISK VS RETURN CHART
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.scatter(
    annual_volatility,
    annual_returns
)

for ticker in tickers:
    plt.annotate(
        ticker,
        (
            annual_volatility[ticker],
            annual_returns[ticker]
        )
    )

plt.title("Risk vs Return")
plt.xlabel("Annualised Volatility")
plt.ylabel("Annualised Return")
plt.grid(True)

plt.tight_layout()
plt.show()


# --------------------------------------------------
# 18. CORRELATION HEATMAP
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.imshow(
    correlation_matrix,
    cmap="coolwarm",
    interpolation="nearest"
)

# Display correlation values
for i in range(len(correlation_matrix.index)):
    for j in range(len(correlation_matrix.columns)):
        plt.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns,
    rotation=45
)

plt.yticks(
    range(len(correlation_matrix.index)),
    correlation_matrix.index
)

plt.title("Stock Return Correlation Matrix")

plt.tight_layout()
plt.show()