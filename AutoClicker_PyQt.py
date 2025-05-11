import sys
import time
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QRadioButton, QSpinBox, QComboBox, QGridLayout, QLineEdit, QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
import keyboard as kb

mouse = MouseController()
keyboard = KeyboardController()
clicking = False
click_thread = None

class CustomStepSpinBox(QDoubleSpinBox):
    def stepBy(self, steps):
        current = self.value()
        if current > 1:
            new_val = max(0, current + steps * 1)
        else:
            new_val = max(0, round(current + steps * 0.1, 3))
        self.setValue(new_val)

    def textFromValue(self, value):
        return f"{value:.3f}" if value < 1 else str(int(value))

class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Toggle Auto Clicker (Dark Mode)")
        self.setFixedSize(520, 460)
        self.setup_ui()

    def setup_ui(self):
        self.create_interval_box()
        self.create_repeat_box()
        self.create_click_options()
        self.create_position_box()
        self.create_hotkey_box()
        self.create_toggle_button()

        layout = QVBoxLayout()
        layout.addWidget(self.interval_group)
        layout.addWidget(self.repeat_group)
        layout.addWidget(self.options_group)
        layout.addWidget(self.position_group)
        layout.addWidget(self.hotkey_group)
        layout.addLayout(self.control_layout)
        self.setLayout(layout)

    def create_interval_box(self):
        self.interval_group = QGroupBox("Click Interval")
        layout = QGridLayout()
        self.hours = QSpinBox(); self.minutes = QSpinBox()
        self.seconds = QSpinBox(); self.milliseconds = CustomStepSpinBox()
        self.milliseconds.setDecimals(3)
        self.milliseconds.setSingleStep(1)
        self.milliseconds.setRange(0.0, 1000.0)
        self.milliseconds.setValue(60.0)
        layout.addWidget(QLabel("Hours"), 0, 1)
        layout.addWidget(QLabel("Minutes"), 0, 2)
        layout.addWidget(QLabel("Seconds"), 0, 3)
        layout.addWidget(QLabel("Milliseconds"), 0, 4)
        layout.addWidget(self.hours, 1, 1)
        layout.addWidget(self.minutes, 1, 2)
        layout.addWidget(self.seconds, 1, 3)
        layout.addWidget(self.milliseconds, 1, 4)
        self.interval_group.setLayout(layout)

    def create_repeat_box(self):
        self.repeat_group = QGroupBox("Click Repeat")
        layout = QHBoxLayout()
        self.infinite_repeat = QRadioButton("Infinite")
        self.infinite_repeat.setChecked(True)
        self.repeat_times = QSpinBox()
        layout.addWidget(self.infinite_repeat)
        layout.addWidget(QLabel("or"))
        layout.addWidget(self.repeat_times)
        layout.addWidget(QLabel("times"))
        self.repeat_group.setLayout(layout)

    def create_click_options(self):
        self.options_group = QGroupBox("Click Type")
        layout = QGridLayout()
        self.input_type = QComboBox()
        self.input_type.addItems(["Mouse Left", "Mouse Right", "Keyboard Key"])
        self.keyboard_key_input = QLineEdit()
        self.keyboard_key_input.setPlaceholderText("Enter key (e.g. a, space, enter)")
        layout.addWidget(QLabel("Input Method"), 0, 0)
        layout.addWidget(self.input_type, 0, 1)
        layout.addWidget(QLabel("Key (if keyboard):"), 1, 0)
        layout.addWidget(self.keyboard_key_input, 1, 1)
        self.options_group.setLayout(layout)

    def create_position_box(self):
        self.position_group = QGroupBox("Click Position")
        layout = QGridLayout()
        self.use_current = QRadioButton("Current Cursor Position")
        self.use_current.setChecked(True)
        self.use_custom = QRadioButton("Set Position (X/Y):")
        self.x_input = QSpinBox(); self.y_input = QSpinBox()
        layout.addWidget(self.use_current, 0, 0, 1, 2)
        layout.addWidget(self.use_custom, 1, 0)
        layout.addWidget(self.x_input, 1, 1)
        layout.addWidget(self.y_input, 1, 2)
        self.position_group.setLayout(layout)

    def create_hotkey_box(self):
        self.hotkey_group = QGroupBox("Toggle Hotkey")
        layout = QHBoxLayout()
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setPlaceholderText("e.g. F6, ctrl+alt+t")
        self.set_hotkey_btn = QPushButton("Set Hotkey")
        layout.addWidget(self.hotkey_input)
        layout.addWidget(self.set_hotkey_btn)
        self.set_hotkey_btn.clicked.connect(self.set_toggle_hotkey)
        self.hotkey_group.setLayout(layout)

    def create_toggle_button(self):
        self.control_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("Toggle Clicking")
        self.control_layout.addWidget(self.toggle_btn)
        self.toggle_btn.clicked.connect(self.toggle_clicking)

    def calculate_delay(self):
        ms = self.milliseconds.value()
        ms += self.seconds.value() * 1000
        ms += self.minutes.value() * 60 * 1000
        ms += self.hours.value() * 60 * 60 * 1000
        return ms / 1000

    def perform_click(self):
        input_mode = self.input_type.currentText()
        key_text = self.keyboard_key_input.text()
        click_count = float('inf') if self.infinite_repeat.isChecked() else self.repeat_times.value()
        delay = self.calculate_delay()
        count = 0

        while clicking and count < click_count:
            if not self.use_current.isChecked():
                mouse.position = (self.x_input.value(), self.y_input.value())

            if input_mode == "Mouse Left":
                mouse.click(Button.left)
            elif input_mode == "Mouse Right":
                mouse.click(Button.right)
            elif input_mode == "Keyboard Key":
                if len(key_text) == 1:
                    keyboard.press(key_text)
                    keyboard.release(key_text)
                else:
                    try:
                        key_obj = getattr(Key, key_text.lower())
                        keyboard.press(key_obj)
                        keyboard.release(key_obj)
                    except AttributeError:
                        pass
            count += 1
            time.sleep(delay)

    def start_clicking(self):
        global clicking, click_thread
        if not clicking:
            clicking = True
            click_thread = threading.Thread(target=self.perform_click, daemon=True)
            click_thread.start()

    def stop_clicking(self):
        global clicking
        clicking = False

    def toggle_clicking(self):
        if clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def set_toggle_hotkey(self):
        key_combo = self.hotkey_input.text().strip()
        if key_combo:
            kb.clear_all_hotkeys()
            kb.add_hotkey(key_combo, self.toggle_clicking)

def set_dark_palette(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Highlight, QColor(100, 100, 255))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_palette(app)
    window = AutoClicker()
    window.show()
    sys.exit(app.exec_())
