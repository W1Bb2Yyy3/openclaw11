---
name: yahoo-finance
description: Yahoo Finance integration for real-time stock market data, company information, financial metrics, and investment analysis. Use this skill when Codex needs to: (1) Get current stock prices and market data, (2) Retrieve company financial information and earnings reports, (3) Analyze stock performance and trends, (4) Get market news and updates, (5) Access historical price data for analysis.
---

# Yahoo Finance Integration

## Overview

This skill provides integration with Yahoo Finance data sources, enabling access to real-time and historical stock market data, company information, financial metrics, and market analysis tools. The skill handles data retrieval, caching, and formatting for easy consumption in financial applications.

## Core Capabilities

### 1. Real-Time Market Data
Access to live stock prices and market data:
- **Stock Quotes**: Current price, change, volume, market cap
- **Market Indices**: S&P 500, NASDAQ, DOW, and more
- **Currency Exchange**: Real-time forex rates
- **Cryptocurrency**: Major crypto prices and market data
- **Commodities**: Gold, oil, and other commodity prices

### 2. Company Information
Detailed company data and metrics:
- **Financial Statements**: Balance sheet, income statement, cash flow
- **Key Metrics**: P/E ratio, EPS, ROE, debt ratios
- **Earnings Data**: Quarterly/annual earnings reports
- **Dividend Information**: Yield, payout ratio, ex-dividend date
- **Analyst Ratings**: Buy/sell/hold recommendations

### 3. Historical Data
Access to historical price and volume data:
- **Price History**: Daily, weekly, monthly OHLCV data
- **Technical Indicators**: Moving averages, RSI, MACD, Bollinger Bands
- **Splits & Dividends**: Historical corporate actions
- **Earnings Calendar**: Upcoming earnings dates and estimates

### 4. Market News & Analysis
Latest financial news and market insights:
- **Stock News**: Company-specific news and announcements
- **Market News**: Economic indicators, policy changes
- **Analyst Reports**: Professional analysis and forecasts
- **Trending Stocks**: Most active and top movers

## Quick Start

### Installation
Ensure Python dependencies are installed:

```bash
pip install yfinance pandas numpy matplotlib
```

### Basic Usage
Get real-time stock data:

```python
import yfinance as yf

# Get current stock price
stock = yf.Ticker("AAPL")
info = stock.info
print(f"Current Price: {info['currentPrice']}")
print(f"Market Cap: {info['marketCap']}")

# Get historical data
hist = stock.history(period="1y")
print(hist.head())
```

### Examples by Use Case

#### Get Stock Price
```python
def get_stock_price(symbol):
    """Get current stock price"""
    ticker = yf.Ticker(symbol)
    return {
        'symbol': symbol,
        'price': ticker.info.get('currentPrice'),
        'change': ticker.info.get('currentPrice') - ticker.info.get('previousClose'),
        'change_percent': ((ticker.info.get('currentPrice') - ticker.info.get('previousClose')) / ticker.info.get('previousClose')) * 100
    }
```

#### Get Company Financials
```python
def get_financials(symbol):
    """Get company financial statements"""
    ticker = yf.Ticker(symbol)
    return {
        'income_statement': ticker.financials,
        'balance_sheet': ticker.balance_sheet,
        'cash_flow': ticker.cashflow,
        'quarterly_financials': ticker.quarterly_financials
    }
```

#### Get Historical Data
```python
def get_historical_data(symbol, period="1y"):
    """Get historical price data"""
    ticker = yf.Ticker(symbol)
    return ticker.history(period=period)
```

#### Get Market Indices
```python
def get_market_indices():
    """Get major market indices"""
    indices = ['^GSPC', '^DJI', '^IXIC', '^N225']
    data = {}
    for index in indices:
        ticker = yf.Ticker(index)
        data[index] = {
            'price': ticker.info.get('previousClose'),
            'change': ticker.info.get('regularMarketChange'),
            'change_percent': ticker.info.get('regularMarketChangePercent')
        }
    return data
```

## Data Formats

### Stock Quote Response
```json
{
  "symbol": "AAPL",
  "price": 178.52,
  "change": 2.35,
  "change_percent": 1.33,
  "volume": 52345678,
  "market_cap": 2780000000000,
  "pe_ratio": 28.5,
  "eps": 6.16
}
```

### Historical Data Response
```json
{
  "dates": ["2024-01-01", "2024-01-02"],
  "open": [175.50, 176.20],
  "high": [177.80, 178.50],
  "low": [174.20, 175.80],
  "close": [176.20, 178.52],
  "volume": [50000000, 52345678]
}
```

## API Parameters

### yfinance.Ticker Methods
- `info`: Company information and current data
- `history(period)`: Historical price data (period: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
- `financials`: Annual income statement
- `quarterly_financials`: Quarterly income statement
- `balance_sheet`: Annual balance sheet
- `quarterly_balance_sheet`: Quarterly balance sheet
- `cashflow`: Annual cash flow
- `quarterly_cashflow`: Quarterly cash flow
- `earnings`: Earnings data
- `recommendations`: Analyst recommendations

### Period Options
- `"1d"`: 1 day (intraday)
- `"5d"`: 5 days
- `"1mo"`: 1 month
- `"3mo"`: 3 months
- `"6mo"`: 6 months
- `"1y"`: 1 year
- `"2y"`: 2 years
- `"5y"`: 5 years
- `"10y"`: 10 years
- `"ytd"`: Year to date
- `"max"`: Maximum available

## Error Handling

The skill includes robust error handling:
- **Invalid Symbols**: Symbol validation and error messages
- **Data Availability**: Graceful handling of missing data
- **Rate Limits**: Built-in delays to respect API limits
- **Network Issues**: Retry mechanisms for failed requests

## Use Cases

### Investment Research
```python
# Compare multiple stocks
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
for symbol in symbols:
    data = get_stock_price(symbol)
    print(f"{symbol}: ${data['price']} ({data['change_percent']:.2f}%)")
```

### Portfolio Tracking
```python
def track_portfolio(portfolio):
    """Track portfolio performance"""
    total_value = 0
    for symbol, shares in portfolio.items():
        price = get_stock_price(symbol)['price']
        value = price * shares
        total_value += value
        print(f"{symbol}: {shares} shares × ${price:.2f} = ${value:.2f}")
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")
```

### Technical Analysis
```python
def calculate_moving_average(symbol, period=50):
    """Calculate moving average"""
    hist = get_historical_data(symbol, "1y")
    ma = hist['Close'].rolling(window=period).mean()
    return ma
```

## Resources

### Documentation
- `yfinance` GitHub: https://github.com/ranaroussi/yfinance
- Yahoo Finance: https://finance.yahoo.com/

### Common Symbols
- **Stocks**: AAPL, GOOGL, MSFT, AMZN, TSLA, NVDA
- **Indices**: ^GSPC (S&P 500), ^DJI (DOW), ^IXIC (NASDAQ)
- **ETFs**: SPY, QQQ, IWM, VTI
- **Forex**: USDJPY=X, EURUSD=X, GBPUSD=X
- **Crypto**: BTC-USD, ETH-USD

## Best Practices

1. **Cache Data**: Store frequently accessed data to reduce API calls
2. **Error Handling**: Always handle exceptions for invalid symbols
3. **Rate Limiting**: Respect API limits with appropriate delays
4. **Data Validation**: Verify data completeness before analysis
5. **Backfilling**: Use historical data for testing and analysis
