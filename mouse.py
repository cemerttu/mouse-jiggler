#!/usr/bin/env python3
"""
Mouse Jiggler Bot
-----------------
Nudges the mouse cursor every few seconds so your computer doesn't go idle.

Install:   pip install pyautogui
Run:       python mouse_jiggler.py
Options:   python mouse_jiggler.py --interval 30 --distance 5 --duration 3600
Stop:      Press Ctrl+C in the terminal
           (or slam the mouse into a screen corner - pyautogui's failsafe)
"""

import argparse
import random
import time

import pyautogui

pyautogui.FAILSAFE = True  # move mouse to a corner to abort


def jiggle(distance: int) -> None:
    """Move the cursor a few pixels in a random direction, then move it back."""
    dx = random.choice([-1, 1]) * random.randint(1, distance)
    dy = random.choice([-1, 1]) * random.randint(1, distance)
    pyautogui.moveRel(dx, dy, duration=0.15)
    pyautogui.moveRel(-dx, -dy, duration=0.15)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple mouse jiggler bot")
    parser.add_argument("--interval", type=float, default=1,
                        help="Seconds between jiggles (default: 1)")
    parser.add_argument("--distance", type=int, default=15,
                        help="Max pixels to move each jiggle (default: 15)")
    parser.add_argument("--duration", type=float, default=0,
                        help="Total run time in seconds; 0 = run until stopped (default: 0)")
    args = parser.parse_args()

    print(f"Mouse jiggler started: every {args.interval}s, up to {args.distance}px.")
    print("Press Ctrl+C to stop.\n")

    start = time.time()
    count = 0

    try:
        while True:
            if args.duration and (time.time() - start) >= args.duration:
                print("Duration reached. Stopping.")
                break

            jiggle(args.distance)
            count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Jiggle #{count}")

            # Sleep in small steps so Ctrl+C responds quickly
            end = time.time() + args.interval
            while time.time() < end:
                time.sleep(0.5)

    except KeyboardInterrupt:
        print(f"\nStopped by user after {count} jiggles.")
    except pyautogui.FailSafeException:
        print(f"\nFailsafe triggered (mouse in corner). Stopped after {count} jiggles.")


if __name__ == "__main__":
    main()