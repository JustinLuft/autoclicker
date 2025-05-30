# AutoClicker

A simple and customizable GUI-based auto-clicker built with Python. This tool allows you to automate mouse clicks or keyboard presses at specific intervals and positions.

## Features

- ⏱️ Set click intervals (hours, minutes, seconds, milliseconds)
- 🔁 Infinite or fixed number of repetitions
- 🖱️ Mouse click (left/right) or keyboard key press
- 🎯 Click at current or custom screen coordinates
- 🧠 Start/stop using a global hotkey
- 🖼️ Clean and easy-to-use graphical interface (Tkinter)

## Requirements

- Python 3.7+
- Dependencies:
  - `pynput`
  - `keyboard`

You can install the dependencies using pip:

```bash
pip install pynput keyboard
```

## Getting Started

1. **Clone or download this repository.**
2. **Navigate to the project folder and run:**

```bash
python AutoClicker.py
```

3. **Configure the settings in the GUI:**
   - Set interval and repeat options
   - Choose mouse or keyboard input
   - Specify click position (optional)

4. **Use the designated hotkey (`F6` by default) to start or stop clicking.**

## File Structure

- `AutoClicker.py` - Main GUI application
- `OldAutoClicker.py` - Legacy version of the clicker
- `hamster_icon.ico` - Application icon
- `.github/workflows/main.yml` - GitHub Actions CI configuration

## Notes

- Run the script with administrator privileges to ensure keyboard/mouse hooks function properly.
- The app uses global hotkeys, so it must remain in focus for consistent behavior across platforms.

## License

MIT License. Use freely with attribution.
