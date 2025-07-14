# 📈 Stock Market Analysis

## 📌 Overview

This project performs a comprehensive analysis of Brazilian stock market data using the `yfinance` API and IBOVESPA data. It explores historical prices, dividend performance, and investment strategies based on dividend yield. The analysis helps evaluate whether investing in high-yield dividend stocks provides superior returns compared to a diversified portfolio.

---

## 📂 Project Structure

### 1. 📥 Data Collection
- Uses the `yfinance` library to retrieve historical data, dividends, balance sheets, and other financials from PETR4.SA and other top IBOV stocks.
- Loads external CSV data (`IBOVDia`) to determine the top 10 stocks by market participation.

### 2. 📊 Exploratory Analysis
- Analyzes daily returns and volatility of top-performing stocks.
- Evaluates the impact of negative return days on future returns.
- Visualizes return distributions using `seaborn.histplot`.

### 3. 📉 Investment Strategy Simulation
- Compares two portfolio strategies:
  - **Global Portfolio**: Equal allocation to the top 10 IBOV stocks.
  - **High Dividend Portfolio**: Invests annually in the 3 stocks with the highest Dividend Yield (DY).
- Calculates cumulative returns over the years and visualizes them using `matplotlib`.

### 4. 💰 Dividend Yield (DY) Analysis
- Aggregates dividends by year and calculates DY per stock.
- Combines with annual return data to simulate reinvestment strategies.
- Evaluates whether selecting high DY stocks leads to better performance.

---

## ✅ Key Takeaways
- The analysis shows that the Global Portfolio (diversified across 10 top IBOV stocks) yielded better long-term returns than the strategy based on high dividend yield.
- Historical data suggests that buying stocks after a loss day does not consistently produce gains.

---

## 📎 Requirements

- Python 3.x
- Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `yfinance`

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn yfinance
