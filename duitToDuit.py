import sys
import sqlite3
import requests
import time
import csv
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox,
    QScrollArea, QMainWindow, QAction, QStackedWidget, QFontDialog, 
    QListWidget, QTableWidget, QTableWidgetItem, QHeaderView, QDialog,
    QDialogButtonBox, QStatusBar, QFileDialog, QFrame
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from style import light_style, dark_style

API_KEY = "df70c2e44c333d54929d40d3"

class DuitToDuit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Duit To Duit")
        self.resize(600, 400)

        self.setStyleSheet(light_style)

        self.all_currencies = []  
        self.currency_names = {}
        
        self.init_db()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.exchange_page = QWidget()
        self.currency_page = QWidget()
        self.database_page = QWidget()

        self.stack.addWidget(self.exchange_page)
        self.stack.addWidget(self.currency_page)
        self.stack.addWidget(self.database_page)

        self.init_menu()
        self.init_status_bar()
        self.init_exchange_page()
        self.init_currency_page()
        self.init_database_page()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_rate)
        self.timer.start(60000)

    def init_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.name_nim_label = QLabel("Teguh Dwi Julyanto - F1D022098")
        self.name_nim_label.setAlignment(Qt.AlignRight)

        self.status_bar.addPermanentWidget(self.name_nim_label)
    
    def init_db(self):
        self.conn = sqlite3.connect('Duit.db')
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS "Duit" (
                "id"	INTEGER,
                "namaNegara"	TEXT,
                "namaMataUang"	TEXT,
                "perbandinganDariDolar"	REAL,
                "waktu" INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
            )
        ''')
        self.conn.commit()

    def get_current_timestamp(self):
        return int(time.time())
    
    def format_timestamp(self, timestamp):
        if timestamp:
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"

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
        
        database_menu = menubar.addMenu("Database")
        view_db_action = QAction("Lihat Database", self)
        view_db_action.triggered.connect(self.show_database_page)
        add_currency_action = QAction("Tambah Mata Uang", self)
        add_currency_action.triggered.connect(self.show_add_currency_dialog)
        export_csv_action = QAction("Export ke CSV", self)
        export_csv_action.triggered.connect(self.export_to_csv)
        database_menu.addAction(view_db_action)
        database_menu.addAction(add_currency_action)
        database_menu.addSeparator() 
        database_menu.addAction(export_csv_action)

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

        self.currency_header = QLabel("Pilih menu di atas untuk melihat top mata uang.")
        self.currency_header.setFont(QFont("Arial", 16, QFont.Bold))
        self.currency_header.setAlignment(Qt.AlignCenter)
        self.currency_header.setStyleSheet("""
            QLabel {
                background-color: #007bff;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.currency_header)

        self.last_update_label = QLabel("")
        self.last_update_label.setAlignment(Qt.AlignCenter)
        self.last_update_label.setStyleSheet("color: #6c757d; margin: 5px;")
        layout.addWidget(self.last_update_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.currency_container = QWidget()
        self.currency_layout = QVBoxLayout(self.currency_container)
        self.currency_layout.setSpacing(5)
        self.currency_layout.addStretch()
        
        self.scroll_area.setWidget(self.currency_container)
        layout.addWidget(self.scroll_area)
        
        self.currency_page.setLayout(layout)
    
    def init_database_page(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("Database Mata Uang")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        button_layout = QHBoxLayout()
        self.btn_refresh_db = QPushButton("Refresh Data")
        self.btn_refresh_db.clicked.connect(self.refresh_database_table)
        self.btn_add_currency = QPushButton("Tambah Mata Uang")
        self.btn_add_currency.clicked.connect(self.show_add_currency_dialog)
        self.btn_delete_currency = QPushButton("Hapus Terpilih")
        self.btn_delete_currency.clicked.connect(self.delete_selected_currency)
        self.btn_export_csv = QPushButton("Export ke CSV")
        self.btn_export_csv.clicked.connect(self.export_to_csv)
        
        button_layout.addWidget(self.btn_refresh_db)
        button_layout.addWidget(self.btn_add_currency)
        button_layout.addWidget(self.btn_delete_currency)
        button_layout.addWidget(self.btn_export_csv)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.db_table = QTableWidget()
        self.db_table.setColumnCount(5) 
        self.db_table.setHorizontalHeaderLabels(["ID", "Nama Negara", "Nama Mata Uang", "Rate (USD)", "Waktu"])
        
        header = self.db_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.db_table)
        self.database_page.setLayout(layout)

    def export_to_csv(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Duit")
            count = cur.fetchone()[0]
            
            if count == 0:
                QMessageBox.information(self, "Export CSV", "Database kosong. Tidak ada data untuk diekspor.")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Database ke CSV",
                f"currency_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not file_path:
                return  

            cur.execute("SELECT * FROM Duit ORDER BY id")
            rows = cur.fetchall()

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(["ID", "Nama Negara", "Nama Mata Uang", "Rate (USD)", "Waktu"])

                for row in rows:
                    formatted_row = list(row)
                    if row[4]: 
                        formatted_row[4] = self.format_timestamp(row[4])
                    else:
                        formatted_row[4] = "N/A"
                    writer.writerow(formatted_row)
            
            QMessageBox.information(
                self, 
                "Export Berhasil", 
                f"Database berhasil diekspor ke:\n{file_path}\n\nTotal {count} data berhasil diekspor."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Export Error", 
                f"Gagal mengekspor database:\n{str(e)}"
            )

    def show_database_page(self):
        self.refresh_database_table()
        self.stack.setCurrentWidget(self.database_page)
    
    def refresh_database_table(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Duit ORDER BY id")
        rows = cur.fetchall()
        
        self.db_table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if j == 4:  
                    formatted_time = self.format_timestamp(value)
                    self.db_table.setItem(i, j, QTableWidgetItem(formatted_time))
                else:
                    self.db_table.setItem(i, j, QTableWidgetItem(str(value)))
    
    def show_add_currency_dialog(self):
        dialog = AddCurrencyDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data['negara'] or not data['mata_uang'] or not data['rate']:
                QMessageBox.warning(self, "Input Error", "Semua field harus diisi!")
                return
            try:
                rate = float(data['rate'])
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Rate harus berupa angka!")
                return
            
            self.insert_currency_to_db(data['negara'], data['mata_uang'], rate)
    
    def insert_currency_to_db(self, negara, mata_uang, rate):
        try:
            cur = self.conn.cursor()
            current_time = self.get_current_timestamp()  
            cur.execute("""
                INSERT INTO Duit (namaNegara, namaMataUang, perbandinganDariDolar, waktu) 
                VALUES (?, ?, ?, ?)
            """, (negara, mata_uang, rate, current_time))
            self.conn.commit()
            
            QMessageBox.information(self, "Berhasil", 
                f"Mata uang {mata_uang} dari {negara} berhasil ditambahkan ke database!")

            if self.stack.currentWidget() == self.database_page:
                self.refresh_database_table()
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Gagal menambahkan data: {e}")
    
    def delete_selected_currency(self):
        current_row = self.db_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Pilih Data", "Pilih mata uang yang ingin dihapus!")
            return
        
        id_item = self.db_table.item(current_row, 0)
        if not id_item:
            return
            
        currency_id = id_item.text()
        currency_name = self.db_table.item(current_row, 2).text()
        
        reply = QMessageBox.question(self, "Konfirmasi Hapus", 
            f"Apakah Anda yakin ingin menghapus {currency_name}?",
            QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                cur = self.conn.cursor()
                cur.execute("DELETE FROM Duit WHERE id = ?", (currency_id,))
                self.conn.commit()
                
                QMessageBox.information(self, "Berhasil", "Data berhasil dihapus!")
                self.refresh_database_table()
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Gagal menghapus data: {e}")

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
                self.currency_names = {code: name for code, name in self.all_currencies}
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
                
                self.show_conversion_result_with_options(from_cur, to_cur, amount, converted, rate)
            else:
                QMessageBox.warning(self, "API Error", "Gagal mengambil data nilai tukar.")
        except Exception as e:
            QMessageBox.warning(self, "Network Error", f"Kesalahan jaringan: {e}")
    
    def show_conversion_result_with_options(self, from_cur, to_cur, amount, converted, rate):
        msg = QMessageBox(self)
        msg.setWindowTitle("Conversion Result")
        msg.setText(f"{amount} {from_cur} = {converted:.2f} {to_cur}\n\nRate: 1 {from_cur} = {rate:.2f} {to_cur}")
        msg.setIcon(QMessageBox.Information)
        
        btn_ok = msg.addButton("OK", QMessageBox.AcceptRole)
        btn_add_from = msg.addButton(f"Tambah {from_cur} ke Database", QMessageBox.ActionRole)
        btn_add_to = msg.addButton(f"Tambah {to_cur} ke Database", QMessageBox.ActionRole)
        
        msg.exec_()
        
        if msg.clickedButton() == btn_add_from:
            self.add_currency_from_conversion(from_cur, 1.0)  
        elif msg.clickedButton() == btn_add_to:
            self.add_currency_from_conversion(to_cur, rate if from_cur == "USD" else self.get_usd_rate(to_cur))
    
    def get_usd_rate(self, currency_code):
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/USD/{currency_code}"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                return data["conversion_rate"]
        except Exception as e:
            print(f"Error getting USD rate: {e}")
        return 1.0
    
    def add_currency_from_conversion(self, currency_code, rate):
        currency_name = "Unknown Currency"
        country_name = "Unknown Country"
        
        for code, name in self.all_currencies:
            if code == currency_code:
                currency_name = name
                
                if " Dollar" in name:
                    country_name = name.replace(" Dollar", "")
                elif " Pound" in name:
                    country_name = name.replace(" Pound", "")
                elif " Euro" in name:
                    country_name = "European Union"
                elif " Yen" in name:
                    country_name = "Japan"
                elif " Yuan" in name or " Renminbi" in name:
                    country_name = "China"
                elif " Rupiah" in name:
                    country_name = "Indonesia"
                elif " Peso" in name:
                    country_name = name.replace(" Peso", "")
                else:
                    country_name = name.split()[0] if name.split() else "Unknown"
                break
        
        dialog = AddCurrencyDialog(self)
        dialog.country_input.setText(country_name)
        dialog.currency_input.setText(f"{currency_name} ({currency_code})")
        dialog.rate_input.setText(f"{rate:.2f}")
        
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data['negara'] or not data['mata_uang'] or not data['rate']:
                QMessageBox.warning(self, "Input Error", "Semua field harus diisi!")
                return
            
            try:
                rate_value = float(data['rate'])
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Rate harus berupa angka!")
                return
            
            if self.currency_exists_in_db(currency_code):
                reply = QMessageBox.question(self, "Mata Uang Sudah Ada", 
                    f"Mata uang {currency_code} sudah ada di database. Apakah ingin mengupdate rate-nya?",
                    QMessageBox.Yes | QMessageBox.No)
                
                if reply == QMessageBox.Yes:
                    self.update_currency_rate(currency_code, rate_value)
            else:
                self.insert_currency_to_db(data['negara'], data['mata_uang'], rate_value)
    
    def currency_exists_in_db(self, currency_code):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Duit WHERE namaMataUang LIKE ?", (f"%{currency_code}%",))
            count = cur.fetchone()[0]
            return count > 0
        except sqlite3.Error:
            return False
    
    def update_currency_rate(self, currency_code, new_rate):
        try:
            cur = self.conn.cursor()
            current_time = self.get_current_timestamp() 
            cur.execute("""
                UPDATE Duit 
                SET perbandinganDariDolar = ?, waktu = ?
                WHERE namaMataUang LIKE ?
            """, (new_rate, current_time, f"%{currency_code}%"))
            self.conn.commit()
            
            QMessageBox.information(self, "Berhasil", 
                f"Rate mata uang {currency_code} berhasil diupdate!")
            
            if self.stack.currentWidget() == self.database_page:
                self.refresh_database_table()
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Gagal mengupdate rate: {e}")

    def clear_currency_layout(self):
        while self.currency_layout.count() > 1:  
            child = self.currency_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_top_currencies(self, order="desc"):
        self.currency_header.setText("Mengambil data mata uang...")
        self.last_update_label.setText("")
        self.clear_currency_layout()

        self.stack.setCurrentWidget(self.currency_page)
        
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                rates = data["conversion_rates"]
                sorted_rates = sorted(rates.items(), key=lambda x: x[1], reverse=(order=="desc"))
                top_20 = sorted_rates[:20]

                title = "Terlemah" if order == "desc" else "Terkuat"
                self.currency_header.setText(f"Top 20 Mata Uang {title} terhadap USD")
 
                current_time = datetime.now().strftime("%d %B %Y, %H:%M:%S")
                self.last_update_label.setText(f"Terakhir diupdate: {current_time}")

                self.clear_currency_layout()

                is_weak = order == "desc"
                for rank, (code, rate) in enumerate(top_20, 1):
                    currency_name = self.currency_names.get(code, "")
                    card = CurrencyCard(rank, code, rate, currency_name, is_weak)
                    self.currency_layout.insertWidget(self.currency_layout.count() - 1, card)

                summary_frame = QFrame()
                summary_frame.setFrameStyle(QFrame.Box)
                summary_frame.setStyleSheet("""
                    QFrame {
                        background-color: #e3f2fd;
                        border: 2px solid #2196f3;
                        border-radius: 10px;
                        margin: 10px;
                        padding: 10px;
                    }
                """)
                
                summary_layout = QVBoxLayout(summary_frame)

                rates_values = [rate for _, rate in top_20]
                avg_rate = sum(rates_values) / len(rates_values)
                min_rate = min(rates_values)
                max_rate = max(rates_values)
                
                summary_text = f"""
                <b>Statistik:</b><br>
                • Rata-rata rate: {avg_rate:.4f}<br>
                • Rate terendah: {min_rate:.4f}<br>
                • Rate tertinggi: {max_rate:.4f}<br>
                • Total mata uang ditampilkan: {len(top_20)}
                """
                
                summary_label = QLabel(summary_text)
                summary_label.setWordWrap(True)
                summary_layout.addWidget(summary_label)
                
                self.currency_layout.insertWidget(self.currency_layout.count() - 1, summary_frame)
 
                note_label = QLabel("""
                <i>Catatan: Rate menunjukkan berapa unit mata uang yang diperlukan untuk membeli 1 USD.<br>
                """)
                note_label.setWordWrap(True)
                note_label.setStyleSheet("""
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px;
                """)
                self.currency_layout.insertWidget(self.currency_layout.count() - 1, note_label)
                
            else:
                self.currency_header.setText("Gagal mengambil data nilai tukar")
                error_label = QLabel("Terjadi kesalahan saat mengambil data dari API. Silakan coba lagi nanti.")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: #dc3545; padding: 20px;")
                self.currency_layout.insertWidget(0, error_label)
                
        except Exception as e:
            self.currency_header.setText("Kesalahan Jaringan")
            error_label = QLabel(f"Kesalahan jaringan: {str(e)}\n\nPastikan koneksi internet Anda stabil dan coba lagi.")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("color: #dc3545; padding: 20px;")
            error_label.setWordWrap(True)
            self.currency_layout.insertWidget(0, error_label)
    
    def closeEvent(self, event):
        if hasattr(self, 'conn'):
            self.conn.close()
        event.accept()

class AddCurrencyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Mata Uang ke Database")
        self.setModal(True)
        self.resize(400, 200)
        
        layout = QVBoxLayout()
        
        country_layout = QHBoxLayout()
        country_layout.addWidget(QLabel("Nama Negara:"))
        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("Contoh: Indonesia")
        country_layout.addWidget(self.country_input)
        layout.addLayout(country_layout)
        
        currency_layout = QHBoxLayout()
        currency_layout.addWidget(QLabel("Nama Mata Uang:"))
        self.currency_input = QLineEdit()
        self.currency_input.setPlaceholderText("Contoh: Rupiah (IDR)")
        currency_layout.addWidget(self.currency_input)
        layout.addLayout(currency_layout)
        
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Rate terhadap USD:"))
        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("Contoh: 15000 (1 USD = 15000 IDR)")
        rate_layout.addWidget(self.rate_input)
        layout.addLayout(rate_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            'negara': self.country_input.text().strip(),
            'mata_uang': self.currency_input.text().strip(),
            'rate': self.rate_input.text().strip()
        }

class CurrencyCard(QFrame):
    def __init__(self, rank, code, rate, currency_name="", is_weak=True):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)
        self.setFixedHeight(80)

        self.setup_styling()
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)

        rank_label = QLabel(f"{rank}")
        rank_label.setFont(QFont("Arial", 14, QFont.Bold))
        rank_label.setObjectName("rankLabel")
        rank_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(rank_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        code_label = QLabel(code)
        code_label.setFont(QFont("Arial", 12, QFont.Bold))
        code_label.setObjectName("weakCurrency" if is_weak else "strongCurrency")
        info_layout.addWidget(code_label)

        if currency_name and currency_name != code:
            name_label = QLabel(currency_name[:25] + "..." if len(currency_name) > 25 else currency_name)
            name_label.setFont(QFont("Arial", 9))
            name_label.setObjectName("currencyName")
            info_layout.addWidget(name_label)
        else:
            info_layout.addStretch()
            
        layout.addLayout(info_layout)
        layout.addStretch()

        rate_layout = QVBoxLayout()
        rate_layout.setSpacing(2)
        
        rate_label = QLabel(f"{rate:.4f}")
        rate_label.setFont(QFont("Arial", 11, QFont.Bold))
        rate_label.setAlignment(Qt.AlignRight)
        rate_label.setObjectName("rateLabel")
        rate_layout.addWidget(rate_label)
        
        usd_label = QLabel("per USD")
        usd_label.setFont(QFont("Arial", 8))
        usd_label.setObjectName("usdLabel")
        usd_label.setAlignment(Qt.AlignRight)
        rate_layout.addWidget(usd_label)
        
        layout.addLayout(rate_layout)
        self.setLayout(layout)

    def setup_styling(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DuitToDuit()
    window.show()
    sys.exit(app.exec_())