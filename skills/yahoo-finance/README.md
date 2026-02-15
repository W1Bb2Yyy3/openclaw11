# Yahoo Finance Skill

获取股票市场数据、公司信息和财务分析的综合工具。

## 功能特性

- 📈 实时股票价格和市场数据
- 📊 历史价格数据和技术指标
- 💰 公司财务报表和关键指标
- 🌐 市场指数和外汇汇率
- 🔍 投资组合跟踪和分析

## 安装

```bash
# 安装依赖
pip install -r requirements.txt
```

## 快速开始

### 获取股票价格

```python
from scripts.finance_helper import get_stock_price

# 获取 Apple 股票价格
data = get_stock_price('AAPL')
print(f"当前价格: ${data['price']}")
print(f"涨跌幅: {data['change_percent']:.2f}%")
```

### 获取历史数据

```python
from scripts.finance_helper import get_historical_data

# 获取过去一年的历史数据
hist = get_historical_data('AAPL', period='1y')
for day in hist['data'][-5:]:  # 最近5天
    print(f"{day['date']}: ${day['close']}")
```

### 获取市场指数

```python
from scripts.finance_helper import get_market_summary

indices = get_market_summary()
for name, data in indices.items():
    print(f"{name}: ${data['price']} ({data['change_percent']:+.2f}%)")
```

### 计算移动平均线

```python
from scripts.finance_helper import FinanceHelper

helper = FinanceHelper()
ma_data = helper.get_moving_average('AAPL', period=50)
print(f"50日移动平均: ${ma_data['ma50']}")
print(f"当前价格: ${ma_data['current_price']}")
```

### 跟踪投资组合

```python
from scripts.finance_helper import FinanceHelper

helper = FinanceHelper()
portfolio = {
    'AAPL': 10,
    'GOOGL': 5,
    'MSFT': 8
}
value = helper.get_portfolio_value(portfolio)
print(f"总价值: ${value['total_value']:,.2f}")
```

## 常用股票代码

### 美股
- AAPL - Apple
- GOOGL - Google (Alphabet)
- MSFT - Microsoft
- AMZN - Amazon
- TSLA - Tesla
- NVDA - NVIDIA

### ETF
- SPY - SPDR S&P 500 ETF
- QQQ - Invesco QQQ Trust (NASDAQ 100)
- IWM - iShares Russell 2000 ETF
- VTI - Vanguard Total Stock Market ETF

### 指数
- ^GSPC - S&P 500
- ^DJI - Dow Jones Industrial Average
- ^IXIC - NASDAQ Composite
- ^VIX - CBOE Volatility Index

### 外汇
- USDJPY=X - USD/JPY
- EURUSD=X - EUR/USD
- GBPUSD=X - GBP/USD

### 加密货币
- BTC-USD - Bitcoin
- ETH-USD - Ethereum

## 数据周期选项

- `1d` - 1天（盘中数据）
- `5d` - 5天
- `1mo` - 1个月
- `3mo` - 3个月
- `6mo` - 6个月
- `1y` - 1年
- `2y` - 2年
- `5y` - 5年
- `10y` - 10年
- `ytd` - 年初至今
- `max` - 最大可用数据

## 文件结构

```
yahoo-finance/
├── SKILL.md                 # 技能说明文档
├── README.md               # 使用指南
├── requirements.txt        # Python 依赖
└── scripts/
    └── finance_helper.py   # 主要功能实现
```

## 注意事项

1. **数据延迟**：免费版 Yahoo Finance 数据可能有 15-20 分钟延迟
2. **API 限制**：避免过于频繁的请求，以免被限制
3. **数据验证**：使用数据前请验证其完整性
4. **投资风险**：此工具仅提供数据，不构成投资建议

## 示例输出

### 股票价格查询

```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "price": 178.52,
  "change": 2.35,
  "change_percent": 1.33,
  "volume": 52345678,
  "market_cap": 2780000000000,
  "pe_ratio": 28.5,
  "eps": 6.16
}
```

### 历史数据

```json
{
  "symbol": "AAPL",
  "period": "1y",
  "data": [
    {
      "date": "2024-01-01",
      "open": 175.50,
      "high": 177.80,
      "low": 174.20,
      "close": 176.20,
      "volume": 50000000
    }
  ]
}
```

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT License
