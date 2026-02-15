"""
Yahoo Finance Helper Module
Provides utility functions for stock market data retrieval and analysis
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class FinanceHelper:
    """Helper class for Yahoo Finance data operations"""
    
    def __init__(self):
        """Initialize FinanceHelper"""
        self.cache = {}
    
    def get_stock_price(self, symbol: str) -> Dict:
        """
        Get current stock price and basic information
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary with stock price information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', 'N/A'),
                'price': info.get('currentPrice', info.get('regularMarketPrice')),
                'previous_close': info.get('previousClose'),
                'change': info.get('currentPrice', info.get('regularMarketPrice')) - info.get('previousClose', 0),
                'change_percent': ((info.get('currentPrice', info.get('regularMarketPrice')) - 
                                   info.get('previousClose', info.get('currentPrice', 1))) / 
                                  info.get('previousClose', info.get('currentPrice', 1))) * 100,
                'volume': info.get('volume'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'eps': info.get('trailingEps'),
                'dividend_yield': info.get('dividendYield') * 100 if info.get('dividendYield') else 0,
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'symbol': symbol,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_historical_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> Dict:
        """
        Get historical price data
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 5m, 15m, 1h, 1d, 1wk, 1mo)
            
        Returns:
            Dictionary with historical data
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            # Convert to list format
            data = {
                'symbol': symbol,
                'period': period,
                'interval': interval,
                'data': []
            }
            
            for date, row in hist.iterrows():
                data['data'].append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']) if pd.notna(row['Open']) else None,
                    'high': float(row['High']) if pd.notna(row['High']) else None,
                    'low': float(row['Low']) if pd.notna(row['Low']) else None,
                    'close': float(row['Close']) if pd.notna(row['Close']) else None,
                    'volume': int(row['Volume']) if pd.notna(row['Volume']) else 0
                })
            
            return data
            
        except Exception as e:
            return {
                'symbol': symbol,
                'error': str(e)
            }
    
    def get_financials(self, symbol: str) -> Dict:
        """
        Get company financial statements
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with financial statements
        """
        try:
            ticker = yf.Ticker(symbol)
            
            return {
                'symbol': symbol,
                'income_statement': self._df_to_dict(ticker.financials),
                'quarterly_income': self._df_to_dict(ticker.quarterly_financials),
                'balance_sheet': self._df_to_dict(ticker.balance_sheet),
                'quarterly_balance': self._df_to_dict(ticker.quarterly_balance_sheet),
                'cash_flow': self._df_to_dict(ticker.cashflow),
                'quarterly_cashflow': self._df_to_dict(ticker.quarterly_cashflow)
            }
        except Exception as e:
            return {
                'symbol': symbol,
                'error': str(e)
            }
    
    def get_market_indices(self) -> Dict:
        """
        Get major market indices data
        
        Returns:
            Dictionary with market indices information
        """
        indices = {
            'S&P 500': '^GSPC',
            'DOW Jones': '^DJI',
            'NASDAQ': '^IXIC',
            'Russell 2000': '^RUT',
            'VIX': '^VIX'
        }
        
        result = {}
        for name, symbol in indices.items():
            data = self.get_stock_price(symbol)
            if 'error' not in data:
                result[name] = {
                    'symbol': symbol,
                    'price': data['price'],
                    'change': data['change'],
                    'change_percent': data['change_percent']
                }
        
        return result
    
    def get_portfolio_value(self, portfolio: Dict[str, int]) -> Dict:
        """
        Calculate portfolio value
        
        Args:
            portfolio: Dictionary of {symbol: shares}
            
        Returns:
            Dictionary with portfolio information
        """
        total_value = 0
        holdings = []
        
        for symbol, shares in portfolio.items():
            stock_data = self.get_stock_price(symbol)
            if 'error' not in stock_data:
                value = stock_data['price'] * shares
                total_value += value
                holdings.append({
                    'symbol': symbol,
                    'company': stock_data['company_name'],
                    'shares': shares,
                    'price': stock_data['price'],
                    'value': value,
                    'change_percent': stock_data['change_percent']
                })
        
        return {
            'holdings': holdings,
            'total_value': total_value,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_moving_average(self, symbol: str, period: int = 50, days: int = 252) -> Dict:
        """
        Calculate moving average
        
        Args:
            symbol: Stock ticker symbol
            period: Moving average period (e.g., 50, 200)
            days: Number of days of historical data to use
            
        Returns:
            Dictionary with moving average data
        """
        try:
            hist_data = self.get_historical_data(symbol, period=f"{days}d")
            
            if 'error' in hist_data:
                return hist_data
            
            df = pd.DataFrame(hist_data['data'])
            df['date'] = pd.to_datetime(df['date'])
            
            # Calculate moving average
            df[f'MA{period}'] = df['close'].rolling(window=period).mean()
            
            # Get latest values
            latest = df.iloc[-1]
            current_price = latest['close']
            ma_value = latest[f'MA{period}']
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                f'ma{period}': ma_value,
                'above_ma': current_price > ma_value,
                'percent_diff': ((current_price - ma_value) / ma_value) * 100 if ma_value else 0
            }
            
        except Exception as e:
            return {
                'symbol': symbol,
                'error': str(e)
            }
    
    def get_top_movers(self, market: str = "us", count: int = 10) -> Dict:
        """
        Get top gainers and losers
        
        Args:
            market: Market (us, etc.)
            count: Number of stocks to return
            
        Returns:
            Dictionary with top movers
        """
        # Note: yfinance doesn't directly provide top movers
        # This would typically use a different API or web scraping
        # For now, return a placeholder
        
        return {
            'gainers': [],
            'losers': [],
            'note': 'Top movers data requires additional API access'
        }
    
    def search_stocks(self, query: str) -> List[Dict]:
        """
        Search for stocks by name or symbol
        
        Args:
            query: Search query (company name or symbol)
            
        Returns:
            List of matching stocks
        """
        # Note: yfinance doesn't have a built-in search function
        # This would require additional API or web scraping
        # For now, return a placeholder
        
        return [
            {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'type': 'Equity'
            }
        ]
    
    def _df_to_dict(self, df: pd.DataFrame) -> Dict:
        """Convert DataFrame to dictionary"""
        if df is None or df.empty:
            return {}
        
        result = {}
        for column in df.columns:
            result[column] = {}
            for index, value in df[column].items():
                if pd.notna(value):
                    result[column][index.strftime('%Y-%m-%d')] = float(value)
        
        return result


# Convenience functions
def get_stock_price(symbol: str) -> Dict:
    """Quick function to get stock price"""
    helper = FinanceHelper()
    return helper.get_stock_price(symbol)


def get_historical_data(symbol: str, period: str = "1y") -> Dict:
    """Quick function to get historical data"""
    helper = FinanceHelper()
    return helper.get_historical_data(symbol, period)


def get_market_summary() -> Dict:
    """Quick function to get market summary"""
    helper = FinanceHelper()
    return helper.get_market_indices()


if __name__ == "__main__":
    # Test the module
    print("Testing Yahoo Finance Helper")
    
    # Test stock price
    print("\nApple Stock Price:")
    print(get_stock_price('AAPL'))
    
    # Test market indices
    print("\nMarket Indices:")
    print(get_market_summary())
    
    # Test historical data
    print("\nApple Historical Data (Last Month):")
    hist = get_historical_data('AAPL', '1mo')
    print(f"Data points: {len(hist.get('data', []))}")
