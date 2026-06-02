#!/usr/bin/env python3
"""Module: Map."""

from typing import Self

from Player import Player
from playerfactory import PlayerFactory
from itemfactory import ItemFactory
import curses
import time
import math


class Map:
    """Class: Map.

    Map class for LOH game, contains main runner for game and
    consoles screen output and input
    """

    __COUNT = 0
    __ALLOWED_TEAMS = ("blue", "red")
    __PLAYER_PER_TEAM = 2
    __instance = None

    @classmethod
    def get_instance(cls) -> Self:
        """"""
        if cls.__instance is None:
            raise ValueError("Map has not been created")
        return cls.__instance

    def __init__(
        self,
        name: str,
        stdscr: curses.window,
        blue: dict | None = None,
        red: dict | None = None,
        size: int = 10,
    ) -> None:
        """"""
        if Map.__COUNT >= 1:
            raise ValueError("Only One Map is Allowed")
        self.__chatboxdisplay = ""
        self.left = 0
        Map.__COUNT += 1
        self.name = name
        self.stdscr = stdscr
        if blue is not None:
            self.blue = blue
        else:
            self.blue = {}
        if red is not None:
            self.red = red
        else:
            self.red = {}
        self.size = 2 * size

        self.squares = []
        for _row in range(self.size):
            col = []
            for _column in range(self.size):
                col.append(Square(math.floor((curses.LINES - 2) / 20)))
            self.squares.append(col)

        self.red_spawn = [0, self.size - 1]
        self.blue_spawn = [self.size - 1, 0]
        self.typing = False
        self.command_buffer = ""
        self.hist_reset = 0
        self._console_history = []
        self.console_gap = 1
        Map.__instance = self
        self.cursor_pos = 3
        self.__chatbox_start = 0
        self.idx = 0
        self.recent_chat = ""

    def __del__(self) -> None:
        """"""
        Map.__COUNT = 0

    def render_dash(self, y: int, x: int, dash_win: curses.window) -> tuple:
        """"""
        max_x = dash_win.getmaxyx()[1]
        map_name = f"{self.name}"
        border = "*" * (max_x - x - 9)
        dash_win.addstr(y, x, border)
        current_x = x + 4
        current_y = y + 1
        dash_win.addstr(current_y, current_x, map_name)
        current_y += 2
        current_x += 4
        for team in self.__ALLOWED_TEAMS:
            dash_win.addstr(current_y, current_x, f"{team} Team:")
            current_y += 1
            team_dict = getattr(self, team)
            for summoner in team_dict:
                player = team_dict[summoner]
                dash_win.addstr(
                    current_y,
                    current_x + 8,
                    f"{summoner}: Max HP: {player.max_hp} Current HP: {player.hp}",
                )
                current_y += 1
        current_y += 1
        dash_win.addstr(current_y, x, border)
        width = len(border)
        height = current_y - y + 1
        for i in range(height):
            dash_win.addstr(y + i, x, "*")
            dash_win.addstr(y + i, max_x - 9, "*")
        return width, height

    def print_map(self, map_win: curses.window) -> tuple:
        """"""
        map_x, map_y = 0, 0
        for y, row in enumerate(self.squares):
            for x, square in enumerate(row):
                square.render(y, x, map_win)
        map_x = self.size * (Square().size + 1) + 5
        map_y = self.size * (Square().size + 1) + 1
        self.refresh_ui()
        return map_x, map_y

    def launch_game(self) -> None:
        """"""
        self.__screen_size(self.stdscr)
        self.map_win, self.dash_win, self.prompt_win = self.__setup_pads(
            *self.__get_win_sizes()
        )
        curses.curs_set(0)
        while True:
            curses.update_lines_cols()
            self.__resize_pads(*self.__get_win_sizes())
            self.map_win.clear()
            self.dash_win.clear()
            self.print_map(self.map_win)
            self.render_dash(0, 0, self.dash_win)
            self.refresh_ui()
            key = self.prompt_win.getkey()
            try:
                if not self.typing:
                    self._handle_game_input(key)
                else:
                    self._handle_chat_input(key)
            except Exception as err:
                self.console_print(f"Error: {err}")
            self.render_console()

    def _handle_game_input(self, key: str) -> None:
        if key == "\n":
            self.typing = True
            self.idx = 0
            self.cursor_pos = len(self.command_buffer)
            self.hist_reset = 0
            try:
                curses.curs_set(1)
            except curses.error:
                pass
            self.render_console()
        elif key == "w":
            for player in self.red:
                self.safe_run(self.__move, "up", player)
        elif key == "s":
            for player in self.red:
                self.safe_run(self.__move, "down", player)
        elif key == "a":
            for player in self.red:
                self.safe_run(self.__move, "left", player)
        elif key == "d":
            for player in self.red:
                self.safe_run(self.__move, "right", player)
        elif key == "KEY_UP":
            for player in self.blue:
                self.safe_run(self.__move, "up", player)
        elif key == "KEY_DOWN":
            for player in self.blue:
                self.safe_run(self.__move, "down", player)
        elif key == "KEY_LEFT":
            for player in self.blue:
                self.safe_run(self.__move, "left", player)
        elif key == "KEY_RIGHT":
            for player in self.blue:
                self.safe_run(self.__move, "right", player)

    def _handle_chat_input(self, key: str) -> None:
        if key == "\x1b":
            self.typing = False
            self.command_buffer = ""
            try:
                curses.curs_set(0)
            except curses.error:
                pass
        elif key == "\n":
            self.__execute_console(self.command_buffer)
            self.command_buffer = ""
            self.typing = False
            try:
                curses.curs_set(0)
            except curses.error:
                pass
        elif key == "KEY_BACKSPACE":
            if self.cursor_pos > 0:
                self.command_buffer = (
                    self.command_buffer[: self.cursor_pos - 1]
                    + self.command_buffer[self.cursor_pos :]
                )
                self.cursor_pos -= 1
        elif key == "KEY_DC":
            if self.cursor_pos < len(self.command_buffer):
                self.command_buffer = (
                    self.command_buffer[: self.cursor_pos]
                    + self.command_buffer[self.cursor_pos + 1 :]
                )
        elif key == "KEY_RESIZE":
            pass
        elif key == "KEY_UP":
            if self.idx == 0 and self.hist_reset == 0:
                self.recent_chat = self.command_buffer
                self.hist_reset = 1
            self.idx += 1
            if self.idx == 0 and self.hist_reset == 1:
                self.command_buffer = self.recent_chat
                self.hist_reset = 0
            else:
                try:
                    self.command_buffer = self.console_history[
                        (len(self.console_history) - (self.idx))
                    ]
                except:
                    pass

        elif key == "KEY_DOWN":
            if self.idx == 0 and self.hist_reset == 0:
                self.recent_chat = self.command_buffer
                self.hist_reset = 1
            else:
                self.idx = 0
                self.hist_reset = 0
            self.command_buffer = self.recent_chat

        elif key == "KEY_RIGHT":
            self.cursor_pos += 1
        elif key == "KEY_LEFT":
            self.cursor_pos -= 1
        else:
            self.command_buffer = (
                self.command_buffer[: self.cursor_pos]
                + key
                + self.command_buffer[self.cursor_pos :]
            )
            self.cursor_pos += 1

    def __help(self, prompt_win: curses.window, p_y: int, p_x: int) -> None:
        # TODO: Update to match valid commands
        self.console_print("Commands: add buy move attack help")
        prompt_win.addstr(p_y + 1, p_x, "help\n")
        self.refresh_ui()

    def __add(self, team: str, player_name: str) -> None:
        if type(team) is not str:
            raise TypeError("Team should be a string")
        if team not in self.__ALLOWED_TEAMS:
            raise ValueError("Invalid Team")
        if self.__get_player(player_name) is not None:
            raise ValueError(f"{player_name} already selected")
        match team:
            case "red":
                if len(self.red) >= self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                player.row = self.red_spawn[0]
                player.column = self.red_spawn[1]
                self.red[player_name] = player
                player.team = team
                self.squares[player.row][player.column].incoming(player)
            case "blue":
                if len(self.blue) >= self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                player.row = self.blue_spawn[0]
                player.column = self.blue_spawn[1]
                self.blue[player_name] = player
                player.team = team
                self.squares[player.row][player.column].incoming(player)
        # TODO: add px, py for better control and reliablity
        self.console_print(f"{player_name} joined {team}")

    def __buy(self, item_name: str, player_name: str) -> None:
        player = self.__get_player(player_name)
        if player is None:
            raise ValueError(f"Inactive player ({player_name}) cannot buy item")
        item = ItemFactory(item_name)
        player.buy(item)

    def __attack(self, from_plyr: str, to_plyr: str) -> None:
        attacker = self.__get_player(from_plyr)
        if attacker is None:
            raise ValueError(f"{from_plyr} is not selected")
        defender = self.__get_player(to_plyr)
        if defender is None:
            raise ValueError(f"{to_plyr} is not selected")
        if defender.hp <= 0:
            raise ValueError(f"{to_plyr} is already dead")
        if attacker.hp <= 0 or attacker.team == defender.team:
            raise ValueError("Action Unavailable")
        distance = (
            (defender.row - attacker.row) ** 2
            + (defender.column - attacker.column) ** 2
        ) ** 0.5
        if attacker.attack_range < distance:
            pass
        else:
            defender.hp -= attacker.attack_score
        if defender.hp <= 0:
            defender.hp = 0
            defender.respawn()

    def __move(self, direction: str, player_name: str) -> None:
        player = self.__get_player(player_name)
        if player is None:
            raise ValueError("Player not found")
        if player.hp <= 0:
            raise ValueError("Action Unavailable")

        current_square = self.squares[player.row][player.column]
        target_row = player.row
        target_column = player.column

        match direction:
            case "up":
                target_row -= 1
            case "down":
                target_row += 1
            case "left":
                target_column -= 1
            case "right":
                target_column += 1
            case _:
                raise ValueError("Valid directions are: up, down, left and right")

        if (
            target_row < 0
            or target_row >= self.size
            or target_column < 0
            or target_column >= self.size
        ):
            raise ValueError("Player must stay on the map")

        target_square = self.squares[target_row][target_column]
        if target_square.is_full():
            raise ValueError("Target square is full")

        current_square.outgoing(player)
        target_square.incoming(player)
        player.row = target_row
        player.column = target_column

    def __get_player(self, player_name: str) -> Player | None:
        if player_name in self.blue:
            return self.blue[player_name]
        if player_name in self.red:
            return self.red[player_name]
        return None

    def __screen_size(self, stdscr: curses.window) -> None:
        h1, w1, h2, w2, h3, w3 = self.__get_win_sizes()
        min_width = w1 + (w2 if w2 > w3 else w3)
        min_height = h1 if h1 > (h2 + h3) else (h2 + h3)
        while curses.LINES < min_height or curses.COLS < min_width:
            stdscr.clear()
            curses.update_lines_cols()
            stdscr.addstr(
                0, 0, f"Min size width: {min_width}px, height: {min_height}px"
            )
            stdscr.addstr(
                1, 0, f"Current Size width: {curses.COLS}px, height: {curses.LINES}px"
            )
            stdscr.refresh()

    def __get_win_sizes(self) -> tuple:
        offset_from_title_y = 3
        offset_from_title_y += (self.__PLAYER_PER_TEAM * 3) * len(
            self.__ALLOWED_TEAMS
        ) + 1
        dash_width = 80

        dash_h = offset_from_title_y + 1

        prompt_h = curses.LINES - dash_h
        map_h, map_w = self.stdscr.getmaxyx()
        map_w -= dash_width

        return map_h, map_w, dash_h, dash_width, prompt_h, dash_width

    def __setup_pads(
        self,
        map_h: int,
        map_w: int,
        dash_h: int,
        dash_w: int,
        prompt_h: int,
        prompt_w: int,
    ) -> tuple:
        if map_h <= 0:
            raise ValueError("map_h cannot be 0")
        if map_w <= 0:
            raise ValueError("map_w cannot be 0")
        if dash_h <= 0:
            raise ValueError(f"dash_h cannot be {dash_h}")
        if dash_w <= 0:
            raise ValueError(f"dash_w cannot be {dash_w}")
        if prompt_h <= 0:
            raise ValueError("prompt_h cannot be 0")
        if prompt_w <= 0:
            raise ValueError("prompt_w cannot be 0")
        map_win = curses.newpad(map_h, map_w)
        dash_win = curses.newpad(dash_h, dash_w)
        prompt_win = curses.newpad(prompt_h, prompt_w)
        map_win.keypad(True)
        dash_win.keypad(True)
        prompt_win.keypad(True)
        self.stdscr.keypad(True)
        return map_win, dash_win, prompt_win

    def __resize_pads(
        self,
        map_h: int,
        map_w: int,
        dash_h: int,
        dash_w: int,
        prompt_h: int,
        prompt_w: int,
    ) -> tuple:
        if map_h <= 0:
            raise ValueError("map_h cannot be 0")
        if map_w <= 0:
            raise ValueError("map_w cannot be 0")
        if dash_h <= 0:
            raise ValueError(f"dash_h cannot be {dash_h}")
        if dash_w <= 0:
            raise ValueError(f"dash_w cannot be {dash_w}")
        if prompt_h <= 0:
            raise ValueError("prompt_h cannot be 0")
        if prompt_w <= 0:
            raise ValueError("prompt_w cannot be 0")
        self.map_win.resize(map_h, map_w)
        self.dash_win.resize(dash_h, dash_w)
        self.prompt_win.resize(prompt_h, prompt_w)
        return self.map_win, self.dash_win, self.prompt_win

    def console_print(self, msg: str) -> None:
        self.console_history.append(str(msg))

    def render_console(self) -> None:
        self.prompt_win.clear()

        ph, pw = self.prompt_win.getmaxyx()
        input_y = ph - 1

        visible_rows = max(0, input_y - self.console_gap)

        history = self.console_history[-visible_rows:]

        start_y = input_y - self.console_gap - len(history) - 1

        if self.typing:
            width = 50
            cursor_idx = len(self.command_buffer) + self.left
            start = max(0, cursor_idx - width + 1)
            end = start + width
            self.__chatboxdisplay = self.command_buffer[start:end]
            self.prompt_win.addstr(input_y - 1, 0, ">> " + self.__chatboxdisplay)
            self.__chatbox_start = start

        for line in history:
            if start_y >= 0:
                self.prompt_win.addstr(start_y, 0, f">> {line[: pw - 1]}")
            start_y += 1

        self.refresh_ui()

    def __execute_console(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        try:
            args = text.split()
            cmd = args[0]
            if cmd == "add":
                self.__add(*args[1:])
            elif cmd == "buy":
                self.__buy(*args[1:])
            elif cmd == "move":
                self.__move(*args[1:])
            elif cmd == "attack":
                self.__attack(*args[1:])
            elif cmd == "help":
                self.console_print("Commands: add buy move attack help")
            else:
                self.console_print(f"{text}")
        except Exception as err:
            self.console_print(f"[Command Error] {err}")

    def refresh_ui(self, keu: str = "") -> None:
        """Refresh all UI panes in correct order."""
        my, mx, dy, dx, py, px = self.__get_win_sizes()
        ### DRAW TO INTERNAL BUFFER ###
        self.map_win.noutrefresh(0, 0, 0, 0, my, mx)  # map (top-left)
        self.dash_win.noutrefresh(
            0, 0, 0, mx + 1, dy, curses.COLS - 1
        )  # dashboard (top-right)
        self.prompt_win.noutrefresh(
            0, 0, dy + 1, mx + 1, curses.LINES - 1, curses.COLS - 1
        )  # console (bottom full width)

        ### DRAW TO SCREEN ###
        if self.typing:
            self.prompt_win.move(py - 2, 3 + self.cursor_pos)
        curses.doupdate()

    def __fullprint(self, pad: curses.window, chr: str) -> None:
        for i in range(pad.getmaxyx()[0]):
            for n in range(pad.getmaxyx()[1] - 1):
                pad.addstr(i, n, chr)

    def __win_print(
        self, map_win: curses.window, dash_win: curses.window, prompt_win: curses.window
    ) -> None:
        my, mx, dy, dx, py, px = self.__get_win_sizes()
        self.__fullprint(map_win, "M")
        self.refresh_ui()
        self.__fullprint(dash_win, "D")
        self.refresh_ui()
        self.__fullprint(prompt_win, "P")
        self.refresh_ui()

    @property
    def map_win(self) -> curses.window:
        """"""
        return self.__map_win

    @map_win.setter
    def map_win(self, map_win: curses.window) -> None:
        if not isinstance(map_win, curses.window):
            raise ValueError("map_win must a window object")
        self.__map_win = map_win

    @property
    def dash_win(self) -> curses.window:
        """"""
        return self.__dash_win

    @dash_win.setter
    def dash_win(self, dash_win: curses.window) -> None:
        if not isinstance(dash_win, curses.window):
            raise ValueError("dash_win must a window object")
        self.__dash_win = dash_win

    @property
    def prompt_win(self) -> curses.window:
        """"""
        return self.__prompt_win

    @prompt_win.setter
    def prompt_win(self, prompt_win: curses.window) -> None:
        if not isinstance(prompt_win, curses.window):
            raise ValueError("prompt_win must a window object")
        self.__prompt_win = prompt_win

    @property
    def squares(self) -> list:
        """"""
        return self.__squares

    @squares.setter
    def squares(self, matrix: list) -> None:
        if not isinstance(matrix, list):
            raise TypeError("Squares must be a list layout grid")
        self.__squares = matrix

    @property
    def red(self) -> dict:
        """"""
        return self.__red

    @red.setter
    def red(self, players: dict) -> None:
        if not isinstance(players, dict):
            raise TypeError("Players Must be a Dictionary.")
        self.__red = players

    @property
    def blue(self) -> dict:
        """"""
        return self.__blue

    @blue.setter
    def blue(self, players: dict) -> None:
        if not isinstance(players, dict):
            raise TypeError("Players Must be a Dictionary.")
        self.__blue = players

    @property
    def stdscr(self) -> curses.window:
        """"""
        return self.__stdscr

    @stdscr.setter
    def stdscr(self, stdscr: curses.window) -> None:
        if not isinstance(stdscr, curses.window):
            raise TypeError("stdscr must be a curses window")
        self.__stdscr = stdscr

    def safe_run(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as err:
            self.console_print(f"{str(err)}")

    @property
    def cursor_pos(self):
        return self.__cursor_pos

    @cursor_pos.setter
    def cursor_pos(self, pos):
        self.__cursor_pos = max(0, min(pos, len(self.command_buffer)))

    @property
    def idx(self):
        return self.__idx

    @idx.setter
    def idx(self, idx: int):
        if idx < 0:
            self.__idx = 0
        elif abs(idx) > len(self.console_history) and idx != 0:
            self.__idx = 0
        else:
            self.__idx = idx

    @property
    def console_history(self):
        return self._console_history

    @console_history.setter
    def console_history(self, command: str):
        self._console_history.append(command)

    @property
    def recent_chat(self):
        return self.__recent_chat

    @recent_chat.setter
    def recent_chat(self, text_input: str):
        self.__recent_chat = text_input

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left: int):
        self.__left = left


class Square:
    """"""

    def __init__(self, size: int = 3) -> None:
        """"""
        self.__size = size
        self.players = []

    @property
    def size(self) -> int:
        """"""
        return self.__size

    @property
    def players(self) -> list:
        """"""
        return self.__players

    @players.setter
    def players(self, players: list) -> None:
        self.__players = players

    def incoming(self, player: Player) -> None:
        """"""
        self.players.append(player)

    def outgoing(self, player: Player) -> None:
        """"""
        self.players.remove(player)

    def render(self, y: int, x: int, stdscr: curses.window) -> tuple:
        height = self.__size
        width = height * 3

        square_y = y * (height + 1)
        square_x = x * (width + 1)

        stdscr.addstr(square_y, square_x, "-" * (width + 2))

        for i in range(1, height + 1):
            player = self.players[i - 1] if i - 1 < len(self.players) else None

            content = (
                " " * width
                if player is None
                else f"{player.get_short_name():^{width}}"[:width]
            )

            stdscr.addstr(square_y + i, square_x, "|" + content + "|")

            stdscr.addstr(square_y + height + 1, square_x, "-" * (width + 2))

        return width + 2, height + 2

    def is_full(self) -> bool:
        """"""
        return len(self.players) == self.__size
