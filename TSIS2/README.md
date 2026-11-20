# TSIS 2 — Paint Application

A Pygame paint program with freehand drawing, shape tools, adjustable outlines,
flood fill, text, and timestamped PNG export.

## Run

From this folder, install the requirement and launch the app:

```bash
python3 -m pip install -r requirements.txt
python3 paint.py
```

`pygame-ce` provides the `pygame` module and includes prebuilt wheels for recent
Python versions on macOS. The app uses only Pygame and Python's standard library.

## Tools

Click a toolbar button or use the shortcut shown beside the tool. Drag to draw;
the line tool previews before release. Click a color swatch to select a color.
Brush sizes 2, 5, and 10 px apply to pencil, eraser, lines, and shape outlines.
Flood fill uses exact RGBA color matching. Text is typed after selecting Text and
clicking the canvas; Enter commits it and Escape cancels it.

| Shortcut | Tool |
| --- | --- |
| P | Pencil |
| L | Line |
| R | Rectangle |
| C | Circle |
| E | Eraser |
| K | Color picker |
| F | Flood fill |
| T | Text |
| Q | Square |
| W | Right triangle |
| Y | Equilateral triangle |
| H | Rhombus |
| 1 / 2 / 3 | Brush size |
| Ctrl+S | Save PNG |

Saves are created in this folder with a date and time in the filename.
