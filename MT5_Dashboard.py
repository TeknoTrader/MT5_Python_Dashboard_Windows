import sys
import MetaTrader5 as mt5
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QTableWidget, QTableWidgetItem, QGroupBox,
                             QFormLayout, QMessageBox, QHeaderView)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor


class MT5TradingDashboard(QMainWindow):
    """
    MT5 Trading Dashboard - A professional GUI for MetaTrader 5 trading

    Features:
    - Real-time connection to MT5 terminal
    - Quick trade execution (Buy/Sell)
    - Position monitoring with auto-refresh
    - Profit/Loss tracking
    - Mass position closing
    """

    def __init__(self):
        super().__init__()
        self.connected = False
        self.initUI()

        # Timer for auto-updating positions
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_positions)

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle('MT5 Trading Dashboard Pro')
        self.setGeometry(100, 100, 1200, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # LEFT SIDEBAR - Connection
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 1)

        # CENTER - Trading Panel
        trading_panel = self.create_trading_panel()
        main_layout.addWidget(trading_panel, 2)

        # RIGHT - Positions Panel
        positions_panel = self.create_positions_panel()
        main_layout.addWidget(positions_panel, 2)

        # Apply modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
        """)

    def create_sidebar(self):
        """Create connection sidebar"""
        group = QGroupBox("⚙️ MT5 Connection")
        layout = QVBoxLayout()

        # Status indicator
        self.status_label = QLabel("🔴 NOT CONNECTED")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "background-color: #ffcccc; padding: 10px; border-radius: 5px; font-weight: bold;")
        layout.addWidget(self.status_label)

        # Account information display
        self.account_info = QLabel("")
        self.account_info.setStyleSheet("background-color: white; padding: 10px; border-radius: 5px;")
        self.account_info.hide()
        layout.addWidget(self.account_info)

        # Connection form
        form_layout = QFormLayout()
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("12345678")
        form_layout.addRow("Account:", self.account_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("••••••••")
        form_layout.addRow("Password:", self.password_input)

        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("BrokerName-Demo")
        form_layout.addRow("Server:", self.server_input)

        layout.addLayout(form_layout)

        # Connection buttons
        btn_connect = QPushButton("🔌 CONNECT")
        btn_connect.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_connect.clicked.connect(self.connect_mt5)
        layout.addWidget(btn_connect)

        btn_disconnect = QPushButton("🔌 DISCONNECT")
        btn_disconnect.setStyleSheet("background-color: #757575; color: white;")
        btn_disconnect.clicked.connect(self.disconnect_mt5)
        layout.addWidget(btn_disconnect)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def create_trading_panel(self):
        """Create trading panel"""
        group = QGroupBox("💹 Trading Panel")
        layout = QVBoxLayout()

        # Trading form
        form_layout = QFormLayout()
        self.symbol_input = QLineEdit("EURUSD")
        form_layout.addRow("Symbol:", self.symbol_input)

        self.lot_input = QLineEdit("0.1")
        form_layout.addRow("Lot Size:", self.lot_input)

        self.sl_input = QLineEdit("0")
        form_layout.addRow("Stop Loss (pips):", self.sl_input)

        self.tp_input = QLineEdit("0")
        form_layout.addRow("Take Profit (pips):", self.tp_input)

        self.comment_input = QLineEdit("Dashboard Trade")
        form_layout.addRow("Comment:", self.comment_input)

        layout.addLayout(form_layout)

        # BUY/SELL buttons
        btn_layout = QHBoxLayout()

        btn_buy = QPushButton("🟢 BUY")
        btn_buy.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 20px;")
        btn_buy.clicked.connect(lambda: self.open_trade('buy'))
        btn_layout.addWidget(btn_buy)

        btn_sell = QPushButton("🔴 SELL")
        btn_sell.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 20px;")
        btn_sell.clicked.connect(lambda: self.open_trade('sell'))
        btn_layout.addWidget(btn_sell)

        layout.addLayout(btn_layout)
        layout.addStretch()

        group.setLayout(layout)
        return group

    def create_positions_panel(self):
        """Create positions monitoring panel"""
        group = QGroupBox("📊 Open Positions")
        layout = QVBoxLayout()

        # Total profit display
        self.total_profit_label = QLabel("Total Profit: $0.00")
        self.total_profit_label.setAlignment(Qt.AlignCenter)
        self.total_profit_label.setStyleSheet(
            "background-color: #e3f2fd; padding: 10px; border-radius: 5px; font-size: 14px; font-weight: bold;")
        layout.addWidget(self.total_profit_label)

        # Refresh button
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setStyleSheet("background-color: #2196F3; color: white;")
        btn_refresh.clicked.connect(self.update_positions)
        layout.addWidget(btn_refresh)

        # Positions table
        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(6)
        self.positions_table.setHorizontalHeaderLabels(['Ticket', 'Symbol', 'Type', 'Lots', 'Profit', 'Action'])
        self.positions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.positions_table)

        # Close all button
        btn_close_all = QPushButton("⚠️ CLOSE ALL POSITIONS")
        btn_close_all.setStyleSheet("background-color: #ff9800; color: white; font-weight: bold;")
        btn_close_all.clicked.connect(self.close_all_positions)
        layout.addWidget(btn_close_all)

        group.setLayout(layout)
        return group

    def connect_mt5(self):
        """Connect to MT5 terminal"""
        account = self.account_input.text()
        password = self.password_input.text()
        server = self.server_input.text()

        if not account or not password or not server:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        if not mt5.initialize():
            QMessageBox.critical(self, "Error", f"MT5 initialization failed: {mt5.last_error()}")
            return

        authorized = mt5.login(int(account), password=password, server=server)

        if authorized:
            self.connected = True
            self.status_label.setText("🟢 CONNECTED")
            self.status_label.setStyleSheet(
                "background-color: #ccffcc; padding: 10px; border-radius: 5px; font-weight: bold;")

            account_info = mt5.account_info()
            if account_info:
                info_text = f"Balance: {account_info.balance:.2f} {account_info.currency}\n"
                info_text += f"Equity: {account_info.equity:.2f} {account_info.currency}\n"
                info_text += f"Margin: {account_info.margin:.2f} {account_info.currency}"
                self.account_info.setText(info_text)
                self.account_info.show()

            QMessageBox.information(self, "Success", "✅ Successfully connected to MT5!")
            self.update_positions()
            self.timer.start(3000)  # Update every 3 seconds
        else:
            QMessageBox.critical(self, "Error", f"Login failed: {mt5.last_error()}")

    def disconnect_mt5(self):
        """Disconnect from MT5 terminal"""
        mt5.shutdown()
        self.connected = False
        self.status_label.setText("🔴 NOT CONNECTED")
        self.status_label.setStyleSheet(
            "background-color: #ffcccc; padding: 10px; border-radius: 5px; font-weight: bold;")
        self.account_info.hide()
        self.timer.stop()
        self.positions_table.setRowCount(0)
        QMessageBox.information(self, "Info", "Disconnected from MT5")

    def open_trade(self, trade_type):
        """Open a new trade (buy or sell)"""
        if not self.connected:
            QMessageBox.warning(self, "Error", "You are not connected to MT5!")
            return

        try:
            symbol = self.symbol_input.text()
            volume = float(self.lot_input.text())
            sl = float(self.sl_input.text())
            tp = float(self.tp_input.text())
            comment = self.comment_input.text()

            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                QMessageBox.critical(self, "Error", f"Symbol {symbol} not found")
                return

            if not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    QMessageBox.critical(self, "Error", f"Failed to select {symbol}")
                    return

            point = symbol_info.point
            tick = mt5.symbol_info_tick(symbol)

            if trade_type == 'buy':
                order_type = mt5.ORDER_TYPE_BUY
                price = tick.ask
                sl_price = price - sl * point * 10 if sl > 0 else 0
                tp_price = price + tp * point * 10 if tp > 0 else 0
            else:
                order_type = mt5.ORDER_TYPE_SELL
                price = tick.bid
                sl_price = price + sl * point * 10 if sl > 0 else 0
                tp_price = price - tp * point * 10 if tp > 0 else 0

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "sl": sl_price,
                "tp": tp_price,
                "deviation": 20,
                "magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)

            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                QMessageBox.information(self, "Success",
                                        f"✅ {trade_type.upper()} order executed!\n"
                                        f"Ticket: {result.order}\n"
                                        f"Volume: {result.volume}\n"
                                        f"Price: {result.price}")
                self.update_positions()
            else:
                error_msg = result.comment if result else mt5.last_error()
                QMessageBox.critical(self, "Error", f"Order failed: {error_msg}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def update_positions(self):
        """Update positions table with current open positions"""
        if not self.connected:
            return

        positions = mt5.positions_get()

        self.positions_table.setRowCount(0)

        if positions is None or len(positions) == 0:
            self.total_profit_label.setText("Total Profit: $0.00")
            self.total_profit_label.setStyleSheet(
                "background-color: #e3f2fd; padding: 10px; border-radius: 5px; font-size: 14px; font-weight: bold;")
            return

        total_profit = 0

        for i, pos in enumerate(positions):
            self.positions_table.insertRow(i)

            # Ticket
            self.positions_table.setItem(i, 0, QTableWidgetItem(str(pos.ticket)))

            # Symbol
            self.positions_table.setItem(i, 1, QTableWidgetItem(pos.symbol))

            # Type
            trade_type = "BUY" if pos.type == 0 else "SELL"
            self.positions_table.setItem(i, 2, QTableWidgetItem(trade_type))

            # Lots
            self.positions_table.setItem(i, 3, QTableWidgetItem(f"{pos.volume:.2f}"))

            # Profit
            profit_item = QTableWidgetItem(f"${pos.profit:.2f}")
            if pos.profit >= 0:
                profit_item.setForeground(QColor(0, 128, 0))
            else:
                profit_item.setForeground(QColor(255, 0, 0))
            self.positions_table.setItem(i, 4, profit_item)

            # Close button
            btn_close = QPushButton("❌ Close")
            btn_close.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
            btn_close.clicked.connect(lambda checked, ticket=pos.ticket: self.close_position(ticket))
            self.positions_table.setCellWidget(i, 5, btn_close)

            total_profit += pos.profit

        # Update total profit display
        profit_text = f"Total Profit: ${total_profit:.2f}"
        if total_profit >= 0:
            self.total_profit_label.setStyleSheet(
                "background-color: #c8e6c9; padding: 10px; border-radius: 5px; font-size: 14px; font-weight: bold; color: #2e7d32;")
        else:
            self.total_profit_label.setStyleSheet(
                "background-color: #ffcdd2; padding: 10px; border-radius: 5px; font-size: 14px; font-weight: bold; color: #c62828;")
        self.total_profit_label.setText(profit_text)

    def close_position(self, ticket):
        """Close a specific position by ticket number"""
        reply = QMessageBox.question(self, 'Confirm',
                                     f'Do you want to close position #{ticket}?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.No:
            return

        try:
            positions = mt5.positions_get(ticket=ticket)
            if not positions:
                QMessageBox.warning(self, "Error", f"Position #{ticket} not found")
                return

            pos = positions[0]
            close_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
            tick = mt5.symbol_info_tick(pos.symbol)
            close_price = tick.bid if pos.type == 0 else tick.ask

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": close_type,
                "position": ticket,
                "price": close_price,
                "deviation": 20,
                "magic": 234000,
                "comment": f"Close {ticket}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)

            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                QMessageBox.information(self, "Success",
                                        f"✅ Position #{ticket} closed!\nProfit: ${pos.profit:.2f}")
                self.update_positions()
            else:
                error_msg = result.comment if result else mt5.last_error()
                QMessageBox.critical(self, "Error", f"Failed to close: {error_msg}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def close_all_positions(self):
        """Close all open positions"""
        positions = mt5.positions_get()
        if not positions or len(positions) == 0:
            QMessageBox.information(self, "Info", "No positions to close")
            return

        reply = QMessageBox.question(self, 'Confirm',
                                     f'Do you want to close ALL {len(positions)} positions?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.No:
            return

        closed = 0
        failed = 0

        for pos in positions:
            try:
                close_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
                tick = mt5.symbol_info_tick(pos.symbol)
                close_price = tick.bid if pos.type == 0 else tick.ask

                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": pos.symbol,
                    "volume": pos.volume,
                    "type": close_type,
                    "position": pos.ticket,
                    "price": close_price,
                    "deviation": 20,
                    "magic": 234000,
                    "comment": f"Close All {pos.ticket}",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }

                result = mt5.order_send(request)
                if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                    closed += 1
                else:
                    failed += 1
            except:
                failed += 1

        msg = f"✅ {closed} positions closed"
        if failed > 0:
            msg += f"\n⚠️ {failed} positions failed to close"

        QMessageBox.information(self, "Result", msg)
        self.update_positions()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    window = MT5TradingDashboard()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
