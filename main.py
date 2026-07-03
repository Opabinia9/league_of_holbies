#!/usr/bin/python3
from Map import Map
import curses
import sys
import traceback


def winend():
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)
curses.noecho()


try:
    map = Map("kalid", stdscr, {}, {}, int(sys.argv[1]))
    map.launch_game()
except KeyboardInterrupt:
    x = curses.COLS
    y = curses.LINES
    winend()
    print("Game Exited, Bye ['_']")
    print("CURSES GO GRRRRRRRRR!")
    print(f"size is {x}x {y}y")
except curses.error:
    x = curses.COLS
    y = curses.LINES
    winend()
    print("CURSES GO AHHHHH!")
    print(f"size is {x}x {y}y")
    traceback.print_exc()
except BaseException as e:
    winend()
    raise e
