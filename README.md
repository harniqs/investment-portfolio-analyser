# Investment Portfolio Analyser

An interactive Python application that analyses the historical performance, risk and diversification of a custom equity portfolio.

## Project Overview

I built this project to combine my interests in finance and computer science by creating a tool that converts historical market data into useful portfolio insights.

Users can enter their own stock tickers, choose a time period and investment amount, and analyse the historical risk and performance of an equal-weight portfolio.

## Features

- Custom stock ticker selection
- Adjustable start and end dates
- Adjustable initial investment
- Historical market data retrieval
- Annualised return calculation
- Annualised volatility calculation
- Sharpe ratio analysis
- Maximum drawdown analysis
- Equal-weight portfolio construction
- Portfolio growth visualisation
- Risk vs return comparison
- Asset correlation heatmap
- Individual stock performance analysis

## Technologies Used

- Python
- pandas
- NumPy
- yfinance
- Matplotlib
- Streamlit

## Financial Metrics
-------------------------------
### Ticker
The ticker is the unique symbol used to identify each company or security on a stock exchange. For example, AAPL represents Apple and NAB.AX represents National Australia Bank on the Australian Securities Exchange.

### Portfolio Weight
Shows the percentage of the portfolio allocated to each selected stock. The current version uses an equal-weight approach, meaning every selected stock receives the same allocation.

### Initial Investment
The dollar amount entered by the user as the starting value of the portfolio. Changing this amount changes the dollar value shown in the portfolio growth chart but does not change percentage-based risk or return metrics.

### Annualised Return
Estimates the average yearly return of an investment using historical daily returns. A higher annualised return indicates stronger historical performance over the selected period.

### Annualised Volatility
Measures how much the returns of an investment fluctuate over time. Higher volatility generally indicates greater uncertainty and investment risk.

### Sharpe Ratio
Measures risk-adjusted performance by comparing the return earned above the risk-free rate with the amount of volatility taken.

A higher Sharpe ratio generally indicates stronger historical return relative to risk.

### Risk-Free Rate
Represents the assumed return available from a relatively low-risk investment. It is used when calculating the Sharpe ratio.

### Maximum Drawdown
Measures the largest percentage decline from a previous peak to a subsequent low during the selected period.

It helps show the severity of historical losses that may not be obvious from average return or volatility alone.

### Portfolio Return
Measures the annualised return of the overall portfolio based on the returns and weights of the selected assets.

### Portfolio Volatility
Measures the overall risk of the portfolio.

The calculation uses the covariance between asset returns, allowing the model to account for diversification rather than simply averaging the volatility of individual stocks.

### Portfolio Growth
Shows how the user's initial investment would have changed over the selected historical period based on the calculated daily portfolio returns.

### Risk vs Return
Compares each stock's annualised return with its annualised volatility.

This helps visualise the relationship between historical performance and risk across the selected investments.

### Correlation
Measures how closely the returns of two assets move together.

Correlation ranges from -1 to +1:

- +1 indicates that the assets move very closely together
- 0 indicates little linear relationship
- -1 indicates that the assets tend to move in opposite directions

Lower correlation between assets can provide greater diversification benefits.

### Correlation Matrix
Displays the correlation between every pair of selected stocks, making it easier to identify which assets move similarly and where diversification may exist.
-------------------------------------
## Portfolios

The default portfolio uses:

- Apple (AAPL)
- Microsoft (MSFT)
- NVIDIA (NVDA)
- Amazon (AMZN)
- Alphabet (GOOGL)

The application can also analyse other supported equities, for example:

- NAB (NAB.AX)
- Commonwealth Bank (CBA.AX)
- ANZ (ANZ.AX)
- Westpac (WBC.AX)

## Portfolio Construction

The current version uses an equal-weight portfolio, meaning each selected asset receives the same allocation.

Portfolio volatility measures the overall risk of the portfolio. It also considers how the selected stocks move in relation to each other, which helps show the effect of diversification.

## Disclaimer

This project is for analytical purposes only. It uses historical market data, and past performance does not guarantee future results.