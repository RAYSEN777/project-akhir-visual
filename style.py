light_style = """
QWidget {
    background-color: #f9f9f9;
    color: #222222;
}

QLabel {
    font-weight: 600;
    color: #333333;
    margin-right: 10px;
}

QComboBox, QLineEdit {
    background-color: white;
    border: 1.2px solid #cccccc;
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 100px;
    color: #222222;
    transition: border-color 0.3s ease, background-color 0.3s ease;
}

QComboBox:hover, QLineEdit:hover {
    border-color: #3399ff;
    background-color: #e6f0ff;
}

QComboBox:focus, QLineEdit:focus {
    border-color: #2962ff;
    background-color: #d6e4ff;
    outline: none;
    box-shadow: 0 0 8px rgba(41, 98, 255, 0.5);
}

QPushButton {
    background-color: #2962ff;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 700;
    min-width: 130px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(41, 98, 255, 0.3);
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

QPushButton:hover {
    background-color: #0039cb;
    box-shadow: 0 6px 16px rgba(0, 56, 203, 0.6);
}

QPushButton:pressed {
    background-color: #002a8a;
    box-shadow: 0 2px 6px rgba(0, 42, 138, 0.4);
}

QPushButton:disabled {
    background-color: #b0b0b0;
    color: #666666;
    cursor: default;
    box-shadow: none;
}

QScrollBar:vertical {
    background: #e0e0e0;
    width: 12px;
    margin: 16px 0 16px 0;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #a0a0a0;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #3399ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QMenuBar {
    background-color: #ffffff;
    color: #222222;
    border-bottom: 1px solid #cccccc;
}

QMenuBar::item {
    background: transparent;
    color: #222222;
    padding: 5px 15px;
    border-radius: 4px;
    margin: 2px;
    transition: background-color 0.2s ease, color 0.2s ease;
}

QMenuBar::item:hover {
    background-color: #4CAF50;  
    color: white;
    border-radius: 6px;
}

QMenuBar::item:selected { 
    background: #e3f2fd; 
    color: #1976d2;         
}

QMenuBar::item:pressed {
    background: #1976d2;
    color: white;
}

QTableWidget {
    background-color: white;
    border: 1px solid #cccccc;
    border-radius: 8px;
    gridline-color: #e0e0e0;
    selection-background-color: #e3f2fd;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #f0f0f0;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}

QTableWidget::item:hover {
    background-color: #f5f5f5;
}

QHeaderView::section {
    background-color: #f8f9fa;
    color: #333333;
    font-weight: 600;
    padding: 10px 8px;
    border: 1px solid #e0e0e0;
    border-radius: 0px;
}

QHeaderView::section:hover {
    background-color: #e9ecef;
}

QStatusBar {
    color: #495057;
    border-top: 1px solid #dee2e6;
    padding: 2px;
}
"""

dark_style = """
QWidget {
    background-color: #121212;
    color: #e0e0e0;
}

QLabel {
    font-weight: 600;
    margin-right: 10px;
    color: #eeeeee;
}

QComboBox, QLineEdit {
    background-color: #1e1e1e;
    border: 1.5px solid #444444;
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 100px;
    color: #dddddd;
}

QComboBox:hover, QLineEdit:hover {
    border-color: #3399ff;
}

QComboBox:focus, QLineEdit:focus {
    border-color: #2962ff;
    outline: none;
    background-color: #2a2a2a;
}

QPushButton {
    background-color: #2962ff;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 700;
    min-width: 130px;
    transition: background-color 0.3s ease;
    cursor: pointer;
}

QPushButton:hover {
    background-color: #0039cb;
}

QPushButton:pressed {
    background-color: #002a8a;
}

QScrollBar:vertical {
    background: #222222;
    width: 12px;
    margin: 16px 0 16px 0;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #555555;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #3399ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QMenuBar {
    background-color: #1e1e1e;
    color: #e0e0e0;
    border-bottom: 1px solid #333333;
}

QMenuBar::item {
    background: transparent;
    color: #e0e0e0;
    padding: 5px 15px;
    border-radius: 4px;
    margin: 2px;
    transition: background-color 0.2s ease, color 0.2s ease;
}

QMenuBar::item:hover {
    background-color: #FF6B35;
    color: white;
    border-radius: 6px;
}

QMenuBar::item:selected { 
    background: #2d2d30; 
    color: #64b5f6;         
}

QMenuBar::item:pressed {
    background: #1976d2;
    color: white;
}

QTableWidget {
    background-color: #1e1e1e;
    border: 1px solid #444444;
    border-radius: 8px;
    gridline-color: #333333;
    selection-background-color: #1a237e;
    color: #e0e0e0;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #2a2a2a;
    background-color: #1e1e1e;
}

QTableWidget::item:selected {
    background-color: #1a237e;
    color: #ffffff;
}

QTableWidget::item:hover {
    background-color: #2a2a2a;
}

QTableWidget::item:alternate {
    background-color: #252525;
}

QHeaderView::section {
    background-color: #2d2d30;
    color: #e0e0e0;
    font-weight: 600;
    padding: 10px 8px;
    border: 1px solid #444444;
    border-radius: 0px;
}

QHeaderView::section:hover {
    background-color: #3d3d40;
}

QListWidget {
    background-color: #1e1e1e;
    border: 1px solid #444444;
    border-radius: 8px;
    color: #e0e0e0;
}

QListWidget::item {
    padding: 6px;
    border-bottom: 1px solid #2a2a2a;
}

QListWidget::item:selected {
    background-color: #1a237e;
    color: white;
}

QListWidget::item:hover {
    background-color: #2a2a2a;
}

QDialog {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QDialogButtonBox QPushButton {
    min-width: 80px;
    padding: 6px 12px;
}

QStatusBar {
    color: #495057;
    border-top: 1px solid #dee2e6;
    padding: 2px;
}
"""

light_currency_card_style = """
CurrencyCard QLabel#rankLabel {
    color: #6c757d;
    min-width: 30px;
}

CurrencyCard QLabel#weakCurrency {
    color: #dc3545;
}

CurrencyCard QLabel#strongCurrency {
    color: #28a745;
}

CurrencyCard QLabel#currencyName {
    color: #6c757d;
}

CurrencyCard QLabel#rateLabel {
    color: #333333;
}

CurrencyCard QLabel#usdLabel {
    color: #6c757d;
}
"""

dark_currency_card_style = """
CurrencyCard QLabel#rankLabel {
    color: #9ca3af;
    min-width: 30px;
}

CurrencyCard QLabel#weakCurrency {
    color: #f87171;
}

CurrencyCard QLabel#strongCurrency {
    color: #34d399;
}

CurrencyCard QLabel#currencyName {
    color: #9ca3af;
}

CurrencyCard QLabel#rateLabel {
    color: #e0e0e0;
}

CurrencyCard QLabel#usdLabel {
    color: #9ca3af;
}
"""