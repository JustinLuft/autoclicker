import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
import keyboard as kb

mouse = MouseController()
keyboard = KeyboardController()
clicking = False
click_thread = None
hotkey_registered = False

def perform_click():
    input_type = input_method.get()
    key_text = key_entry.get()
    repeat = float('inf') if repeat_type.get() == "infinite" else int(repeat_count.get())
    delay = (int(hours.get()) * 3600 +
             int(minutes.get()) * 60 +
             int(seconds.get()) +
             float(milliseconds.get()) / 1000)
    count = 0

    while clicking and count < repeat:
        if position_type.get() == "custom":
            x, y = int(pos_x.get()), int(pos_y.get())
            mouse.position = (x, y)

        if input_type == "Mouse Left":
            mouse.click(Button.left)
        elif input_type == "Mouse Right":
            mouse.click(Button.right)
        elif input_type == "Keyboard Key":
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
        messagebox.showerror("Error", f"Could not set hotkey:\n{str(e)}")

# GUI
root = tk.Tk()
root.title("AutoClicker")
root.geometry("400x450")

# Interval
frame1 = ttk.LabelFrame(root, text="Click Interval")
frame1.pack(padx=10, pady=5, fill="x")
hours = tk.Spinbox(frame1, from_=0, to=999, width=5); hours.insert(0, "0")
minutes = tk.Spinbox(frame1, from_=0, to=59, width=5); minutes.insert(0, "0")
seconds = tk.Spinbox(frame1, from_=0, to=59, width=5); seconds.insert(0, "0")
milliseconds = tk.Entry(frame1, width=7); milliseconds.insert(0, "60")
ttk.Label(frame1, text="Hours").grid(row=0, column=0)
hours.grid(row=1, column=0)
ttk.Label(frame1, text="Minutes").grid(row=0, column=1)
minutes.grid(row=1, column=1)
ttk.Label(frame1, text="Seconds").grid(row=0, column=2)
seconds.grid(row=1, column=2)
ttk.Label(frame1, text="Milliseconds").grid(row=0, column=3)
milliseconds.grid(row=1, column=3)

# Repeat
frame2 = ttk.LabelFrame(root, text="Repeat")
frame2.pack(padx=10, pady=5, fill="x")
repeat_type = tk.StringVar(value="infinite")
tk.Radiobutton(frame2, text="Infinite", variable=repeat_type, value="infinite").pack(side="left")
tk.Radiobutton(frame2, text="Fixed", variable=repeat_type, value="fixed").pack(side="left")
repeat_count = tk.Spinbox(frame2, from_=1, to=999999, width=10)
repeat_count.pack(side="left")

# Click Options
frame3 = ttk.LabelFrame(root, text="Click Options")
frame3.pack(padx=10, pady=5, fill="x")
input_method = ttk.Combobox(frame3, values=["Mouse Left", "Mouse Right", "Keyboard Key"])
input_method.current(0)
key_entry = tk.Entry(frame3)
ttk.Label(frame3, text="Type").grid(row=0, column=0)
input_method.grid(row=0, column=1)
ttk.Label(frame3, text="Key (if keyboard):").grid(row=1, column=0)
key_entry.grid(row=1, column=1)

# Position
frame4 = ttk.LabelFrame(root, text="Click Position")
frame4.pack(padx=10, pady=5, fill="x")
position_type = tk.StringVar(value="current")
tk.Radiobutton(frame4, text="Current Position", variable=position_type, value="current").pack(anchor="w")
tk.Radiobutton(frame4, text="Custom Position (X/Y)", variable=position_type, value="custom").pack(anchor="w")
pos_x = tk.Spinbox(frame4, from_=0, to=9999, width=7)
pos_y = tk.Spinbox(frame4, from_=0, to=9999, width=7)
pos_x.pack(side="left", padx=(10, 0))
pos_y.pack(side="left", padx=(5, 0))

# Hotkey
frame5 = ttk.LabelFrame(root, text="Hotkey")
frame5.pack(padx=10, pady=5, fill="x")
hotkey_input = tk.Entry(frame5)
hotkey_input.pack(side="left", padx=5)
tk.Button(frame5, text="Set Hotkey", command=set_hotkey).pack(side="left")

# Toggle button
tk.Button(root, text="Toggle Clicking", command=toggle_clicking, bg="green", fg="white").pack(pady=20)

root.mainloop()
