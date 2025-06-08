import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
import keyboard as kb

mouse = MouseController()
keyboard = KeyboardController()
clicking = False
click_thread = None
hotkey_registered = False

root = tk.Tk()
root.title("AutoClicker")
root.geometry("430x400")
root.resizable(False, False)

# === INTERVAL UI ===
frame1 = ttk.LabelFrame(root, text="Click Interval")
frame1.pack(padx=10, pady=5, fill="x")
for label, var in zip(["Hours", "Minutes", "Seconds", "Milliseconds"], range(4)):
    ttk.Label(frame1, text=label).grid(row=0, column=var, padx=5)
hours = tk.Spinbox(frame1, from_=0, to=999, width=5); hours.grid(row=1, column=0)
minutes = tk.Spinbox(frame1, from_=0, to=59, width=5); minutes.grid(row=1, column=1)
seconds = tk.Spinbox(frame1, from_=0, to=59, width=5); seconds.grid(row=1, column=2)
milliseconds = tk.Spinbox(frame1, from_=0, to=59, width=5); milliseconds.grid(row=1, column=3)


# === REPEAT UI ==
frame2 = ttk.LabelFrame(root, text="Repeat")
frame2.pack(padx=10, pady=5, fill="x")
repeat_type = tk.StringVar(value="infinite")
ttk.Radiobutton(frame2, text="Infinite", variable=repeat_type, value="infinite").grid(row=0, column=0, padx=5)
ttk.Radiobutton(frame2, text="Fixed", variable=repeat_type, value="fixed").grid(row=0, column=1, padx=5)
repeat_count = tk.Spinbox(frame2, from_=1, to=999999, width=8)
repeat_count.grid(row=0, column=2, padx=5)

# === CLICK OPTIONS UI ===
frame3 = ttk.LabelFrame(root, text="Click Options")
frame3.pack(padx=10, pady=5, fill="x")
ttk.Label(frame3, text="Type:").grid(row=0, column=0, padx=5, sticky="e")
input_method = ttk.Combobox(frame3, values=["Mouse Left", "Mouse Right", "Keyboard Key"], state="readonly", width=15)
input_method.current(0)
input_method.grid(row=0, column=1, padx=5)
ttk.Label(frame3, text="Key (if keyboard):").grid(row=1, column=0, padx=5, sticky="e")
key_entry = ttk.Entry(frame3, width=18)
key_entry.grid(row=1, column=1, padx=5)

# === POSITION UI ===
frame4 = ttk.LabelFrame(root, text="Click Position")
frame4.pack(padx=10, pady=5, fill="x")
position_type = tk.StringVar(value="current")
ttk.Radiobutton(frame4, text="Current Position", variable=position_type, value="current").grid(row=0, column=0, columnspan=2, sticky="w", padx=5)
ttk.Radiobutton(frame4, text="Custom Position (X/Y)", variable=position_type, value="custom").grid(row=1, column=0, sticky="w", padx=5)
pos_x = tk.Spinbox(frame4, from_=0, to=9999, width=6)
pos_y = tk.Spinbox(frame4, from_=0, to=9999, width=6)
pos_x.grid(row=1, column=1, padx=2, sticky="w")
pos_y.grid(row=1, column=2, padx=2, sticky="w")

# === HOTKEY UI ===
frame5 = ttk.LabelFrame(root, text="Hotkey")
frame5.pack(padx=10, pady=5, fill="x")
hotkey_input = ttk.Entry(frame5, width=20)
hotkey_input.grid(row=0, column=0, padx=5, pady=5)
def set_hotkey():
    global hotkey_registered
    combo = hotkey_input.get().strip()
    if not combo:
        messagebox.showwarning("Missing Hotkey", "Enter a valid hotkey.")
        return
    try:
        if hotkey_registered:
            kb.remove_all_hotkeys()
        kb.add_hotkey(combo, toggle_clicking)
        hotkey_registered = True
        messagebox.showinfo("Hotkey Set", f"Hotkey '{combo}' registered!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
ttk.Button(frame5, text="Set Hotkey", command=set_hotkey).grid(row=0, column=1, padx=5)

# === CALCULATE DELAY ===
def get_delay():
    try:
        h = int(hours.get())
        m = int(minutes.get())
        s = int(seconds.get())
        ms = float(milliseconds.get())
        return h * 3600 + m * 60 + s + ms
    except ValueError:
        return 1.0  # fallback default

# === CLICK LOGIC ===
def perform_click():
    global clicking
    delay = get_delay()
    input_type_val = input_method.get()
    key_val = key_entry.get()
    max_clicks = float('inf') if repeat_type.get() == "infinite" else int(repeat_count.get())
    count = 0

    while clicking and count < max_clicks:
        if position_type.get() == "custom":
            mouse.position = (int(pos_x.get()), int(pos_y.get()))

        if input_type_val == "Mouse Left":
            mouse.click(Button.left)
        elif input_type_val == "Mouse Right":
            mouse.click(Button.right)
        elif input_type_val == "Keyboard Key":
            if len(key_val) == 1:
                keyboard.press(key_val)
                keyboard.release(key_val)
            else:
                try:
                    key = getattr(Key, key_val.lower())
                    keyboard.press(key)
                    keyboard.release(key)
                except AttributeError:
                    pass
        count += 1
        time.sleep(delay)

# === START / STOP ===
def start_clicking():
    global clicking, click_thread
    if not clicking:
        clicking = True
        click_thread = threading.Thread(target=perform_click, daemon=True)
        click_thread.start()

def stop_clicking():
    global clicking
    clicking = False

def toggle_clicking():
    if clicking:
        stop_clicking()
    else:
        start_clicking()

root.mainloop()
