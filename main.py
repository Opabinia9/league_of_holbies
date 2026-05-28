#!/usr/bin/python3
from Map import Map
import curses

stdscr = curses.initscr()

curses.cbreak()
stdscr.keypad(True)
curses.noecho()

try:
    map = Map("kalid", {}, {}, 5)
    map.launch_game(stdscr)
except BaseException as e:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    raise e
