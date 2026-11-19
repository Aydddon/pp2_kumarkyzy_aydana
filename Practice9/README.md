# Practice 09: Pygame Games

Three small Pygame exercises: a Mickey-inspired digital clock, a keyboard
music player, and a moving ball. Python 3.9+ and Pygame are required.

## Setup

```bash
python -m pip install -r requirements.txt
```

Run each game from the `Practice9` directory:

```bash
python mickeys_clock/main.py
python music_player/main.py
python moving_ball/main.py
```

## Mickey's Clock

Shows the current minute and second. The right glove points to minutes; the
left glove points to seconds. Hands redraw once per second. The face and hands
are drawn in Pygame, so no external image asset is needed.

## Music Player

Place `.wav`, `.ogg`, or `.mp3` files in `music_player/music/`. The player
loads them in alphabetical order and displays the current track and elapsed
time. Controls: **P** play/resume, **S** stop, **N** next, **B** previous,
**Q** quit. Track duration is displayed when the audio backend can read it.

## Moving Ball

Arrow keys move the 25-pixel-radius red ball by 20 pixels per key press. Moves
that would put any part of the ball outside the window are ignored.

## GitHub

From the repository root, after reviewing the files:

```bash
git add Practice9
git commit -m "Add Practice 09 Pygame games"
git push origin main
```
