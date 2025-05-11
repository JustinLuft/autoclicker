import tkinter as tk
from tkinter import ttk
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
import threading
import time
import keyboard as kb

mouse = MouseController()
keyboard = KeyboardController()
clicking = False
hotkey = None

def click_loop(rate, click_type, key):
    global clicking
    delay = 1 / rate
    while clicking:
        click_type = click_type.strip().lower()
        if click_type == "left click":
            mouse.click(Button.left)
        elif click_type == "right click":
            mouse.click(Button.right)
        elif click_type == "keyboard":
            if len(key) == 1:
                keyboard.press(key)
                keyboard.release(key)
            else:
                try:
                    special_key = getattr(Key, key.lower())
                    keyboard.press(special_key)
                    keyboard.release(special_key)
                except AttributeError:
                    status_label.config(text=f"Invalid key: {key}")
        time.sleep(delay)

def toggle_clicking(rate, click_type, key):
    global clicking
    clicking = not clicking
    if clicking:
        status_label.config(text="Clicking...")
        threading.Thread(target=click_loop, args=(rate, click_type, key), daemon=True).start()
    else:
        status_label.config(text="Stopped.")

def start_hotkey_listener():
    global hotkey
    try:
        rate = float(rate_entry.get())
        click_type = click_option.get()
        key = key_entry.get() if click_type.lower() == "keyboard" else None
        if click_type.lower() == "keyboard" and not key:
            status_label.config(text="Please enter a key.")
            return

        if hotkey:
            kb.remove_hotkey(hotkey)

        hotkey_str = hotkey_entry.get()
        if not hotkey_str:
            status_label.config(text="Enter a hotkey.")
            return

        hotkey = kb.add_hotkey(hotkey_str, toggle_clicking, args=(rate, click_type, key))
        status_label.config(text=f"Hotkey '{hotkey_str}' set. Press to toggle.")
    except ValueError:
        status_label.config(text="Invalid rate.")

root = tk.Tk()
root.title("Auto Clicker")

tk.Label(root, text="Clicks per second:").grid(row=0, column=0)
rate_entry = tk.Entry(root)
rate_entry.grid(row=0, column=1)
rate_entry.insert(0, "5")

tk.Label(root, text="Click Type:").grid(row=1, column=0)
click_option = ttk.Combobox(root, values=["Left Click", "Right Click", "Keyboard"])
click_option.current(0)
click_option.grid(row=1, column=1)

tk.Label(root, text="Key (if keyboard):").grid(row=2, column=0)
key_entry = tk.Entry(root)
key_entry.grid(row=2, column=1)
tk.Label(root, text="(Use 'space', 'enter', etc. for special keys)").grid(row=2, column=2)

tk.Label(root, text="Toggle Hotkey (e.g., F6):").grid(row=3, column=0)
hotkey_entry = tk.Entry(root)
hotkey_entry.grid(row=3, column=1)

set_hotkey_btn = tk.Button(root, text="Set Hotkey", command=start_hotkey_listener)
set_hotkey_btn.grid(row=4, column=0, columnspan=2)

status_label = tk.Label(root, text="Idle")
status_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
