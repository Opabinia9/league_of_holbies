#!/usr/bin/python3
from Map import Map
import curses


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
    map = Map("kalid", {}, {}, 5)
    map.launch_game(stdscr)
except KeyboardInterrupt:
    winend()
    print("Game Exited, Bye ['_']")
except curses.error:
    x = curses.COLS
    y = curses.LINES
    winend()
    print("CURSES GO AHHHHH!")
    print(f"size is {x}x {y}y")
except BaseException as e:
    winend()
    raise e
