import sys
import json
import time
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QRadioButton, QSpinBox, QComboBox, QGridLayout
)
from PyQt5.QtCore import Qt
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import keyboard as kb

mouse = MouseController()
keyboard = KeyboardController()
clicking = False
click_thread = None

class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Auto Clicker")
        self.setFixedSize(500, 400)

        self.create_interval_box()
        self.create_repeat_box()
        self.create_click_options()
        self.create_position_box()
        self.create_control_buttons()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.interval_group)
        main_layout.addWidget(self.repeat_group)
        main_layout.addWidget(self.options_group)
        main_layout.addWidget(self.position_group)
        main_layout.addLayout(self.control_layout)

        self.setLayout(main_layout)

    def create_interval_box(self):
        self.interval_group = QGroupBox("Click Interval")
        layout = QGridLayout()
        self.hours = QSpinBox(); self.minutes = QSpinBox()
        self.seconds = QSpinBox(); self.milliseconds = QSpinBox()
        layout.addWidget(QLabel("hours"), 0, 1)
        layout.addWidget(QLabel("minutes"), 0, 2)
        layout.addWidget(QLabel("seconds"), 0, 3)
        layout.addWidget(QLabel("milliseconds"), 0, 4)
        layout.addWidget(self.hours, 1, 1)
        layout.addWidget(self.minutes, 1, 2)
        layout.addWidget(self.seconds, 1, 3)
        layout.addWidget(self.milliseconds, 1, 4)
        self.interval_group.setLayout(layout)

    def create_repeat_box(self):
        self.repeat_group = QGroupBox("Click Repeat")
        layout = QHBoxLayout()
        self.infinite_repeat = QRadioButton("Infinite (Until stopped)")
        self.infinite_repeat.setChecked(True)
        self.repeat_times = QSpinBox()
        layout.addWidget(self.infinite_repeat)
        layout.addWidget(QLabel("or"))
        layout.addWidget(self.repeat_times)
        layout.addWidget(QLabel("Times"))
        self.repeat_group.setLayout(layout)

    def create_click_options(self):
        self.options_group = QGroupBox("Click Options")
        layout = QHBoxLayout()
        self.mouse_button = QComboBox()
        self.mouse_button.addItems(["Left", "Right"])
        self.click_type = QComboBox()
        self.click_type.addItems(["Single", "Double"])
        layout.addWidget(QLabel("Mouse Button"))
        layout.addWidget(self.mouse_button)
        layout.addWidget(QLabel("Click Type"))
        layout.addWidget(self.click_type)
        self.options_group.setLayout(layout)

    def create_position_box(self):
        self.position_group = QGroupBox("Click Position")
        layout = QGridLayout()
        self.use_current = QRadioButton("Current Cursor Position")
        self.use_current.setChecked(True)
        self.use_custom = QRadioButton("X/Y:")
        self.x_input = QSpinBox(); self.y_input = QSpinBox()
        self.pick_btn = QPushButton("Pick Location")
        layout.addWidget(self.use_current, 0, 0, 1, 2)
        layout.addWidget(self.use_custom, 1, 0)
        layout.addWidget(self.x_input, 1, 1)
        layout.addWidget(self.y_input, 1, 2)
        layout.addWidget(self.pick_btn, 1, 3)
        self.position_group.setLayout(layout)

    def create_control_buttons(self):
        self.control_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start (F6)")
        self.stop_btn = QPushButton("Stop (F7)")
        self.toggle_btn = QPushButton("Toggle (F8)")
        self.control_layout.addWidget(self.start_btn)
        self.control_layout.addWidget(self.stop_btn)
        self.control_layout.addWidget(self.toggle_btn)

        self.start_btn.clicked.connect(self.start_clicking)
        self.stop_btn.clicked.connect(self.stop_clicking)
        self.toggle_btn.clicked.connect(self.toggle_clicking)
        kb.add_hotkey("F6", self.start_clicking)
        kb.add_hotkey("F7", self.stop_clicking)
        kb.add_hotkey("F8", self.toggle_clicking)

    def calculate_delay(self):
        ms = self.milliseconds.value()
        ms += self.seconds.value() * 1000
        ms += self.minutes.value() * 60 * 1000
        ms += self.hours.value() * 60 * 60 * 1000
        return ms / 1000

    def perform_click(self):
        btn = Button.left if self.mouse_button.currentText() == "Left" else Button.right
        click_count = float('inf') if self.infinite_repeat.isChecked() else self.repeat_times.value()
        delay = self.calculate_delay()
        count = 0

        while clicking and count < click_count:
            if not self.use_current.isChecked():
                mouse.position = (self.x_input.value(), self.y_input.value())
            mouse.click(btn)
            if self.click_type.currentText() == "Double":
                time.sleep(0.05)
                mouse.click(btn)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClicker()
    window.show()
    sys.exit(app.exec_())
