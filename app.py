import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Investment Portfolio Analyser",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Investment Portfolio Analyser")

st.write(
    "Analyse the historical performance, risk and diversification "
    "of a custom equity portfolio."
)

st.caption(
    "Built with Python, pandas, NumPy, yfinance, Matplotlib and Streamlit."
)


# --------------------------------------------------
# USER INPUTS
# --------------------------------------------------

st.sidebar.header("Portfolio Settings")

ticker_input = st.sidebar.text_input(
    "Enter stock tickers separated by commas",
    "AAPL, MSFT, NVDA, AMZN, GOOGL"
)

start_date = st.sidebar.date_input(
    "Start date",
    value=pd.to_datetime("2024-01-01")
)

end_date = st.sidebar.date_input(
    "End date",
    value=pd.to_datetime("2026-01-01")
)

initial_investment = st.sidebar.number_input(
    "Initial investment ($)",
    min_value=1000,
    value=10000,
    step=1000
)

risk_free_rate = st.sidebar.number_input(
    "Risk-free rate (%)",
    min_value=0.0,
    value=4.0,
    step=0.25
) / 100


# Clean ticker input
tickers = [
    ticker.strip().upper()
    for ticker in ticker_input.split(",")
    if ticker.strip()
]


# --------------------------------------------------
# ANALYSE BUTTON
# --------------------------------------------------

if st.sidebar.button("Analyse Portfolio"):

    if len(tickers) < 2:
        st.error("Please enter at least two stock tickers.")
        st.stop()

    if start_date >= end_date:
        st.error("The start date must be before the end date.")
        st.stop()


    # --------------------------------------------------
    # DOWNLOAD DATA
    # --------------------------------------------------

    with st.spinner("Downloading market data..."):

        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False
        )


    if data.empty:
        st.error("No market data was found.")
        st.stop()


    # --------------------------------------------------
    # CLOSING PRICES
    # --------------------------------------------------

    closing_prices = data["Close"]

    if isinstance(closing_prices, pd.Series):
        closing_prices = closing_prices.to_frame()

    # Remove stocks that did not return usable data
    closing_prices = closing_prices.dropna(
        axis=1,
        how="all"
    )

    available_tickers = list(closing_prices.columns)

    if len(available_tickers) < 2:
        st.error(
            "Not enough valid stock data was returned. "
            "Check the ticker symbols."
        )
        st.stop()


    # --------------------------------------------------
    # RETURNS
    # --------------------------------------------------

    daily_returns = (
        closing_prices
        .pct_change()
        .dropna()
    )


    # --------------------------------------------------
    # INDIVIDUAL STOCK METRICS
    # --------------------------------------------------

    annual_returns = daily_returns.mean() * 252

    annual_volatility = (
        daily_returns.std()
        * np.sqrt(252)
    )

    sharpe_ratio = (
        annual_returns - risk_free_rate
    ) / annual_volatility


    # Maximum drawdown

    cumulative_returns = (
        1 + daily_returns
    ).cumprod()

    running_max = cumulative_returns.cummax()

    drawdown = (
        cumulative_returns
        / running_max
    ) - 1

    max_drawdown = drawdown.min()


    # --------------------------------------------------
    # SUMMARY TABLE
    # --------------------------------------------------

    summary = pd.DataFrame({
        "Annual Return": annual_returns,
        "Annual Volatility": annual_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown": max_drawdown
    })


    # --------------------------------------------------
    # PORTFOLIO WEIGHTS
    # --------------------------------------------------

    weights = pd.Series(
        1 / len(available_tickers),
        index=available_tickers
    )

    allocation = weights.rename("Weight").to_frame()

    allocation["Weight"] = (
        allocation["Weight"]
        .map("{:.1%}".format)
    )
    # --------------------------------------------------
    # PORTFOLIO METRICS
    # --------------------------------------------------

    portfolio_return = (
        annual_returns * weights
    ).sum()

    covariance_matrix = (
        daily_returns.cov()
        * 252
    )

    portfolio_variance = weights.dot(
        covariance_matrix.dot(weights)
    )

    portfolio_volatility = np.sqrt(
        portfolio_variance
    )

    portfolio_sharpe = (
        portfolio_return
        - risk_free_rate
    ) / portfolio_volatility


    # Portfolio daily returns

    portfolio_daily_returns = (
        daily_returns.dot(weights)
    )


    # Growth of investment

    portfolio_growth = (
        (1 + portfolio_daily_returns)
        .cumprod()
        * initial_investment
    )


    # CAGR

    years = (
        portfolio_growth.index[-1]
        - portfolio_growth.index[0]
    ).days / 365.25

    portfolio_cagr = (
        portfolio_growth.iloc[-1]
        / initial_investment
    ) ** (1 / years) - 1


    # Portfolio maximum drawdown

    portfolio_running_max = (
        portfolio_growth.cummax()
    )

    portfolio_drawdown = (
        portfolio_growth
        / portfolio_running_max
    ) - 1

    portfolio_max_drawdown = (
        portfolio_drawdown.min()
    )


    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    st.subheader("Portfolio Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Annualised Return",
        f"{portfolio_return:.2%}"
    )

    col2.metric(
        "Annualised Volatility",
        f"{portfolio_volatility:.2%}"
    )

    col3.metric(
        "Sharpe Ratio",
        f"{portfolio_sharpe:.2f}"
    )

    col4.metric(
        "Maximum Drawdown",
        f"{portfolio_max_drawdown:.2%}"
    )

    st.subheader("Portfolio Allocation")
    
    st.dataframe(
    allocation,
    use_container_width=True
    )

    st.subheader("Portfolio Growth")

    fig_growth, ax_growth = plt.subplots(figsize=(10, 5))

    ax_growth.plot(
        portfolio_growth.index,
        portfolio_growth
    )

    ax_growth.set_title(
        f"Growth of ${initial_investment:,.0f} Investment"
    )

    ax_growth.set_xlabel("Date")
    ax_growth.set_ylabel("Portfolio Value ($)")

    ax_growth.set_xlim(
        portfolio_growth.index.min(),
        portfolio_growth.index.max()
    )

    ax_growth.grid(True)

    plt.tight_layout()

    st.pyplot(fig_growth)


    st.subheader("Individual Stock Analysis")

    display_summary = summary.copy()

    display_summary["Annual Return"] = (
        display_summary["Annual Return"]
        .map("{:.2%}".format)
    )

    display_summary["Annual Volatility"] = (
        display_summary["Annual Volatility"]
        .map("{:.2%}".format)
    )

    display_summary["Sharpe Ratio"] = (
        display_summary["Sharpe Ratio"]
        .map("{:.2f}".format)
    )

    display_summary["Maximum Drawdown"] = (
        display_summary["Maximum Drawdown"]
        .map("{:.2%}".format)
    )

    st.dataframe(
        display_summary,
        use_container_width=True
    )

    # --------------------------------------------------
    # RISK VS RETURN CHART
    # --------------------------------------------------

    st.subheader("Risk vs Return")

    fig1, ax1 = plt.subplots(figsize=(8, 5))

    ax1.scatter(
        annual_volatility,
        annual_returns
    )

    for ticker in available_tickers:
        ax1.annotate(
            ticker,
            (
                annual_volatility[ticker],
                annual_returns[ticker]
            )
        )

    ax1.set_title("Annualised Risk vs Return")
    ax1.set_xlabel("Annualised Volatility")
    ax1.set_ylabel("Annualised Return")
    ax1.grid(True)

    st.pyplot(fig1)


    # --------------------------------------------------
    # CORRELATION HEATMAP
    # --------------------------------------------------

    st.subheader("Asset Correlations")

    correlation_matrix = daily_returns.corr()

    fig2, ax2 = plt.subplots(figsize=(8, 5))

    image = ax2.imshow(
        correlation_matrix,
        cmap="coolwarm",
        interpolation="nearest"
    )

    for i in range(len(correlation_matrix.index)):
        for j in range(len(correlation_matrix.columns)):
            ax2.text(
                j,
                i,
                f"{correlation_matrix.iloc[i, j]:.2f}",
                ha="center",
                va="center"
            )

    ax2.set_xticks(
        range(len(correlation_matrix.columns))
    )

    ax2.set_xticklabels(
        correlation_matrix.columns,
        rotation=45
    )

    ax2.set_yticks(
        range(len(correlation_matrix.index))
    )

    ax2.set_yticklabels(
        correlation_matrix.index
    )

    ax2.set_title("Stock Return Correlation Matrix")

    fig2.colorbar(
        image,
        ax=ax2,
        label="Correlation"
    )

    st.pyplot(fig2)

    st.caption(
        "Historical analysis only. Past performance "
        "does not guarantee future results."
    )