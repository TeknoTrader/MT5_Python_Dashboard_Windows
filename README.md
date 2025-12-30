# 💹 MT5 Trading Dashboard Pro

A **Python-based GUI dashboard** for MetaTrader 5, demonstrating how to use the MT5 Python API for algorithmic trading and automated strategy development.

This project serves as a **practical reference** for traders and developers looking to integrate MT5 with Python, providing reusable code snippets for order execution, position management, and real-time data handling.

---

## 🎯 Purpose

This dashboard is primarily a **learning tool and code library** that demonstrates:

- How to connect to MT5 via Python API
- Real-time position monitoring and management
- Order execution with proper error handling
- Building trading GUIs with PyQt5
- Integrating risk management (SL/TP) in automated systems

**Use Case:** Extract functions from this codebase to build your own algorithmic trading strategies, automated execution systems, or custom trading tools.

---

## ✨ Features

### Core Functionality
- **MT5 API Integration** - Direct connection to MetaTrader 5 terminal
- **Real-time Position Tracking** - Auto-updating position table with P&L
- **Quick Trade Execution** - One-click BUY/SELL with customizable parameters
- **Risk Management** - Built-in Stop Loss and Take Profit in pips
- **Position Management** - Individual and mass position closing

### Technical Demonstration
- **Event-driven GUI** with PyQt5
- **Threaded auto-refresh** (QTimer) for non-blocking updates
- **MT5 Python API** usage examples (connection, orders, positions)
- **Error handling patterns** for production-ready code
- **Clean architecture** suitable for extension

---

## 🛠️ Built With

- **Python 3.8+** - Core language
- **PyQt5** - Desktop GUI framework
- **MetaTrader5** - Official MT5 Python API
- **NumPy** - Numerical operations (MT5 dependency)

---

## 📦 Installation & Usage

### Option 1: Download Executable (Windows)

1. Download the latest release from [Releases](https://github.com/yourusername/mt5-trading-dashboard/releases)
2. Extract the ZIP file
3. Run `MT5_Dashboard.exe`

### Option 2: Run from Source

```bash
# Clone repository
git clone https://github.com/yourusername/mt5-trading-dashboard.git
cd mt5-trading-dashboard

# Install dependencies
pip install -r requirements.txt

# Run application
python mt5_trading_dashboard.py
```

### Option 3: Build Your Own Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build (use the provided script)
build_fixed.bat

# Or manually
pyinstaller --onedir --windowed --name "MT5_Dashboard" --hidden-import=numpy.core.multiarray --clean mt5_trading_dashboard.py
```

For detailed build instructions, see [BUILD_EXE_GUIDE.md](BUILD_EXE_GUIDE.md) and [DISTRIBUTION_GUIDE.md](DISTRIBUTION_GUIDE.md).

---

## 🧑‍💻 For Algorithmic Traders

### Extracting Code for Your Strategy

This codebase provides ready-to-use functions you can integrate into your automated trading systems:

#### **Connection & Authentication**
```python
# From: connect_mt5() method
import MetaTrader5 as mt5

mt5.initialize()
mt5.login(account, password, server)
account_info = mt5.account_info()
```

#### **Order Execution**
```python
# From: open_trade() method
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": volume,
    "type": mt5.ORDER_TYPE_BUY,  # or ORDER_TYPE_SELL
    "price": price,
    "sl": stop_loss_price,
    "tp": take_profit_price,
    "deviation": 20,
    "magic": 234000,
    "comment": "Automated Strategy",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}
result = mt5.order_send(request)
```

#### **Position Monitoring**
```python
# From: update_positions() method
positions = mt5.positions_get()
for pos in positions:
    print(f"Ticket: {pos.ticket}, Profit: {pos.profit}")
```

#### **Position Closing**
```python
# From: close_position() method
position = mt5.positions_get(ticket=ticket)[0]
close_request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": position.symbol,
    "volume": position.volume,
    "type": mt5.ORDER_TYPE_SELL if position.type == 0 else mt5.ORDER_TYPE_BUY,
    "position": ticket,
    "price": close_price,
}
result = mt5.order_send(close_request)
```

### Integration Ideas

- **Automated Strategy Execution** - Replace GUI buttons with signal generation logic
- **Backtesting Framework** - Adapt order execution for historical simulation
- **Risk Management Module** - Extract SL/TP calculation functions
- **Portfolio Manager** - Use position tracking for multi-symbol strategies
- **Alert System** - Add email/Telegram notifications to position updates
- **Data Pipeline** - Extend for real-time market data collection

---

## 📁 Project Structure

```
mt5-trading-dashboard/
├── mt5_trading_dashboard.py      # Main application (extractable functions)
├── requirements.txt               # Python dependencies
├── build_fixed.bat                # Automated build script
├── README.md                      # This file
├── BUILD_EXE_GUIDE.md            # Compilation guide
├── DISTRIBUTION_GUIDE.md         # Distribution guide
└── LICENSE                        # MIT License
```

---

## ⚠️ Disclaimer

**Educational and Research Purposes Only**

This software is provided as a **learning resource** for understanding MT5 API integration and algorithmic trading concepts. 

- No trading advice is provided
- Test thoroughly on demo accounts before live use
- Trading involves significant risk of loss
- Author assumes no responsibility for trading losses
- Use at your own risk

Always implement proper risk management and never trade with money you cannot afford to lose.

---

## 🤝 Contributing

Contributions welcome! This project benefits from community improvements:

- Report bugs via [Issues](../../issues)
- Submit feature requests or API usage examples
- Improve documentation
- Share your algorithmic trading implementations

---

## 📜 License

MIT License - Free to use, modify, and distribute with attribution.

---

## 👤 Author

**Nicola Chimenti**  
💼 Business Analyst & MQL Developer
🎓 Graduated in Business Management  

**Connect:**
- 🌐 [MQL5 Profile](https://www.mql5.com/it/users/teknotrader/seller#!category=2)  
- 🔗 [LinkedIn](https://www.linkedin.com/in/nicolachimenti)  
- 💻 [GitHub](https://github.com/TeknoTrader)  
- 📧 Email: assistenza@nicolachimenti.com

---

## 🙏 Acknowledgments

- **MetaQuotes** for the MT5 Python API
- **PyQt5** community for GUI framework
- **Python trading community** for algorithmic trading resources

---

**VAT Code**: 02674000464  
**Company**: Tekno Trader  
**© 2024 Nicola Chimenti. All rights reserved.**
