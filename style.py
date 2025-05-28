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
}

QMenuBar::item:selected { 
    background: #3399ff; 
    color: white;         
}

QMenuBar::item:pressed {
    background: #1a73e8;
    color: white;
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
    background-color: #2b2b2b;
    color: #e0e0e0;
}

QMenuBar::item {
    background: transparent;
    color: #e0e0e0;
    padding: 5px 15px;
}

QMenuBar::item:selected { 
    background: #3399ff; 
    color: black;         
}

QMenuBar::item:pressed {
    background: #1a73e8;
    color: black;
}
"""
