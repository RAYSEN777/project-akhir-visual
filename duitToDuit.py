import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox,
    QScrollArea, QMainWindow, QAction, QStackedWidget,  QFontDialog, QListWidget
)
from PyQt5.QtCore import QTimer
from style import light_style, dark_style

API_KEY = "df70c2e44c333d54929d40d3"

class CurrencyNotifier(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Exchange Rate Notifier")
        self.resize(500, 300)

        self.setStyleSheet(light_style)

        self.all_currencies = []  

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.exchange_page = QWidget()
        self.currency_page = QWidget()

        self.stack.addWidget(self.exchange_page)
        self.stack.addWidget(self.currency_page)

        self.init_menu()
        self.init_exchange_page()
        self.init_currency_page()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_rate)
        self.timer.start(60000)

    def init_menu(self):
        menubar = self.menuBar()

        exchange_menu = menubar.addMenu("Exchange")
        exchange_action = QAction("Exchange Uang", self)
        exchange_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.exchange_page))
        check_action = QAction("Check Rate Sekarang", self)
        check_action.triggered.connect(self.check_rate)
        exchange_menu.addAction(exchange_action)
        exchange_menu.addAction(check_action)

        data_menu = menubar.addMenu("Data Mata Uang")
        strongest_action = QAction("Top 20 Terlemah", self)
        weakest_action = QAction("Top 20 Terkuat", self)
        strongest_action.triggered.connect(lambda: self.show_top_currencies(order="desc"))
        weakest_action.triggered.connect(lambda: self.show_top_currencies(order="asc"))
        data_menu.addAction(strongest_action)
        data_menu.addAction(weakest_action)

        view_menu = menubar.addMenu("View")
        self.dark_mode_action = QAction("Dark Mode", self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)

        font_action = QAction("Pilih Font...", self)  
        font_action.triggered.connect(self.chooseFont)  
        view_menu.addAction(font_action)

    def init_exchange_page(self):
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Cari Mata Uang:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik kode atau nama mata uang...")
        self.search_input.textChanged.connect(self.filter_currencies)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.search_results = QListWidget()
        self.search_results.setMaximumHeight(150)
        layout.addWidget(self.search_results)

        btn_layout = QHBoxLayout()
        self.btn_set_from = QPushButton("Set as From")
        self.btn_set_to = QPushButton("Set as To")
        btn_layout.addWidget(self.btn_set_from)
        btn_layout.addWidget(self.btn_set_to)
        layout.addLayout(btn_layout)

        self.btn_set_from.clicked.connect(self.set_from_currency)
        self.btn_set_to.clicked.connect(self.set_to_currency)

        from_layout = QHBoxLayout()
        from_layout.addWidget(QLabel("From:"))
        self.from_currency = QComboBox()
        from_layout.addWidget(self.from_currency)
        layout.addLayout(from_layout)

        to_layout = QHBoxLayout()
        to_layout.addWidget(QLabel("To:"))
        self.to_currency = QComboBox()
        to_layout.addWidget(self.to_currency)
        layout.addLayout(to_layout)

        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("Amount"))
        self.threshold_input = QLineEdit()
        amount_layout.addWidget(self.threshold_input)
        layout.addLayout(amount_layout)

        self.btn_check = QPushButton("Check Rate Now")
        self.btn_check.clicked.connect(self.check_rate)
        layout.addWidget(self.btn_check)

        self.exchange_page.setLayout(layout)
        self.load_currencies()
    
    def init_currency_page(self):
        layout = QVBoxLayout()
        self.top_label = QLabel("Pilih menu di atas untuk melihat top mata uang.")
        self.top_label.setWordWrap(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.top_label)

        layout.addWidget(scroll_area)
        self.currency_page.setLayout(layout)

    def toggle_dark_mode(self, checked):
        if checked:
            self.setStyleSheet(dark_style)
        else:
            self.setStyleSheet(light_style)

    def chooseFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.setFont(font)
            for child in self.findChildren(QWidget):
                child.setFont(font)

    def load_currencies(self):
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/codes"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                self.all_currencies = data["supported_codes"]
                codes = [f"{code} - {name}" for code, name in self.all_currencies]
                self.from_currency.addItems(codes)
                self.to_currency.addItems(codes)
                self.from_currency.setCurrentText("USD - United States Dollar")
                self.to_currency.setCurrentText("IDR - Indonesian Rupiah")
            else:
                QMessageBox.warning(self, "Error", "Gagal mengambil daftar mata uang")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Kesalahan jaringan: {e}")

    def filter_currencies(self, text):
        text = text.lower()
        self.search_results.clear()
        if not text:
            return
        filtered = [f"{code} - {name}" for code, name in self.all_currencies if text in code.lower() or text in name.lower()]
        self.search_results.addItems(filtered)

    def set_from_currency(self):
        selected = self.search_results.currentItem()
        if selected:
            self.from_currency.setCurrentText(selected.text())

    def set_to_currency(self):
        selected = self.search_results.currentItem()
        if selected:
            self.to_currency.setCurrentText(selected.text())

    def check_rate(self):
        from_cur_full = self.from_currency.currentText()  
        to_cur_full = self.to_currency.currentText()      
        
        from_cur = from_cur_full.split(" - ")[0]  
        to_cur = to_cur_full.split(" - ")[0]      
        
        amount_text = self.threshold_input.text().strip()
        if not amount_text:
            QMessageBox.warning(self, "Input Error", "Masukkan jumlah uang yang ingin dikonversi.")
            return
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Jumlah uang harus angka.")
            return

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_cur}/{to_cur}"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                rate = data["conversion_rate"]
                converted = amount * rate
                QMessageBox.information(self, "Conversion Result",
                    f"{amount} {from_cur} = {converted:.4f} {to_cur}")
            else:
                QMessageBox.warning(self, "API Error", "Gagal mengambil data nilai tukar.")
        except Exception as e:
            QMessageBox.warning(self, "Network Error", f"Kesalahan jaringan: {e}")

    def show_top_currencies(self, order="desc"):
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                rates = data["conversion_rates"]
                sorted_rates = sorted(rates.items(), key=lambda x: x[1], reverse=(order=="desc"))
                top_20 = sorted_rates[:20]
                title = "Terlemah" if order == "desc" else "Terkuat"
                text = f"<b>Top 20 Mata Uang {title.capitalize()} terhadap USD:</b><br><br>"
                for code, rate in top_20:
                    text += f"{code}: {rate:.4f}<br>"
                self.top_label.setText(text)
                self.stack.setCurrentWidget(self.currency_page)
            else:
                self.top_label.setText("Gagal mengambil data nilai tukar.")
        except Exception as e:
            self.top_label.setText(f"Kesalahan jaringan: {e}")
        self.stack.setCurrentWidget(self.currency_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyNotifier()
    window.show()
    sys.exit(app.exec_())
