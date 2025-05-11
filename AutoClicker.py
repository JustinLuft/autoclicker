import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("AutoClicker")
root.geometry("430x480")
root.resizable(False, False)

def add_spacer(parent):
    ttk.Label(parent, text="").pack(pady=2)

# === Interval ===
frame1 = ttk.LabelFrame(root, text="Click Interval")
frame1.pack(padx=10, pady=5, fill="x")
for label, var in zip(["Hours", "Minutes", "Seconds", "Milliseconds"], range(4)):
    ttk.Label(frame1, text=label).grid(row=0, column=var, padx=5)
hours = tk.Spinbox(frame1, from_=0, to=999, width=5); hours.grid(row=1, column=0)
minutes = tk.Spinbox(frame1, from_=0, to=59, width=5); minutes.grid(row=1, column=1)
seconds = tk.Spinbox(frame1, from_=0, to=59, width=5); seconds.grid(row=1, column=2)
milliseconds = tk.Spinbox(
    frame1, from_=1.0, to=0.0, increment=-0.1, format="%.1f", width=6
)

# === Repeat ===
frame2 = ttk.LabelFrame(root, text="Repeat")
frame2.pack(padx=10, pady=5, fill="x")
repeat_type = tk.StringVar(value="infinite")
ttk.Radiobutton(frame2, text="Infinite", variable=repeat_type, value="infinite").grid(row=0, column=0, padx=5)
ttk.Radiobutton(frame2, text="Fixed", variable=repeat_type, value="fixed").grid(row=0, column=1, padx=5)
repeat_count = tk.Spinbox(frame2, from_=1, to=999999, width=8)
repeat_count.grid(row=0, column=2, padx=5)

# === Click Options ===
frame3 = ttk.LabelFrame(root, text="Click Options")
frame3.pack(padx=10, pady=5, fill="x")
ttk.Label(frame3, text="Type:").grid(row=0, column=0, padx=5, sticky="e")
input_method = ttk.Combobox(frame3, values=["Mouse Left", "Mouse Right", "Keyboard Key"], state="readonly", width=15)
input_method.current(0)
input_method.grid(row=0, column=1, padx=5)
ttk.Label(frame3, text="Key (if keyboard):").grid(row=1, column=0, padx=5, sticky="e")
key_entry = ttk.Entry(frame3, width=18)
key_entry.grid(row=1, column=1, padx=5)

# === Position ===
frame4 = ttk.LabelFrame(root, text="Click Position")
frame4.pack(padx=10, pady=5, fill="x")
position_type = tk.StringVar(value="current")
ttk.Radiobutton(frame4, text="Current Position", variable=position_type, value="current").grid(row=0, column=0, columnspan=2, sticky="w", padx=5)
ttk.Radiobutton(frame4, text="Custom Position (X/Y)", variable=position_type, value="custom").grid(row=1, column=0, sticky="w", padx=5)
pos_x = tk.Spinbox(frame4, from_=0, to=9999, width=6)
pos_y = tk.Spinbox(frame4, from_=0, to=9999, width=6)
pos_x.grid(row=1, column=1, padx=2, sticky="w")
pos_y.grid(row=1, column=2, padx=2, sticky="w")

# === Hotkey ===
frame5 = ttk.LabelFrame(root, text="Hotkey")
frame5.pack(padx=10, pady=5, fill="x")
hotkey_input = ttk.Entry(frame5, width=20)
hotkey_input.grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame5, text="Set Hotkey", command=lambda: print("Set hotkey")).grid(row=0, column=1, padx=5)

# === Toggle Button ===
toggle_btn = ttk.Button(root, text="Toggle Clicking", command=lambda: print("Toggled"))
toggle_btn.pack(pady=20)

root.mainloop()
