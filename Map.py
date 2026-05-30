#!/usr/bin/env python3
"""Module: Map."""

import Player
from playerfactory import PlayerFactory
from itemfactory import ItemFactory
import curses
import time


class Map:
    """Class: Map.

    Map class for LOH game, contains main runner for game and
    consoles screen output and input
    """

    __COUNT = 0
    __ALLOWED_TEAMS = ("blue", "red")
    __PLAYER_PER_TEAM = 2

    def __init__(
        self,
        name: str,
        blue: dict | None = None,
        red: dict | None = None,
        size: int = 8,
    ) -> None:
        """"""
        if Map.__COUNT >= 1:
            raise ValueError("Only One Map is Allowed")
        Map.__COUNT += 1
        self.name = name
        if blue is not None:
            self.blue = blue
        else:
            self.blue = {}
        if red is not None:
            self.red = red
        else:
            self.red = {}
        self.size = size
        self.squares = []
        for _row in range(self.size):
            col = []
            for _column in range(self.size):
                col.append(Square())
            self.squares.append(col)

    def __del__(self) -> None:
        """"""
        Map.__COUNT = 0

    def render_dash(self, y: int, x: int, stdscr: curses.window) -> tuple:
        """"""
        max_y, max_x = stdscr.getmaxyx()
        map_name = f"{self.name}"
        border = "*" * (max_x - x - 9)
        stdscr.addstr(y, x, border)
        current_x = x + 4
        current_y = y + 1
        stdscr.addstr(current_y, current_x, map_name)
        current_y += 2
        current_x += 4
        for team in self.__ALLOWED_TEAMS:
            stdscr.addstr(current_y, current_x, f"{team} Team:")
            current_y += 1
            team_dict = getattr(self, team)
            for summoner in team_dict:
                player = team_dict[summoner]
                stdscr.addstr(current_y, current_x + 8, f"{summoner}: HP: {player.hp}")
                current_y += 1
        # stdscr.addstr(current_y, x + 4, "Red Team:")
        current_y += 1
        # for summoner in self.red:
        #     player = self.red[summoner]
        #     stdscr.addstr(current_y, x + 8, f"{summoner}: HP: {player.hp}")
        #     current_y += 1
        stdscr.addstr(current_y, x, border)
        width = len(border)
        height = current_y - y + 1
        for i in range(height):
            stdscr.addstr(y + i, x, "*")
            stdscr.addstr(y + i, max_x - 9, "*")
        return width, height

    def print_map(self, stdscr: curses.window) -> tuple:
        """"""
        map_x, map_y = 0, 0
        for y, row in enumerate(self.squares):
            for x, square in enumerate(row):
                square.render(y, x, stdscr)
        map_x = self.size * (Square().size + 1) + 5
        map_y = self.size * (Square().size + 1) + 1
        return map_x, map_y

    def launch_game(self, stdscr: curses.window) -> None:
        """"""
        self.__screen_size(stdscr)
        while True:
            stdscr.clear()  # This is commented out so it doesnt clear prompt outputs
            map_x, map_y = self.print_map(stdscr)
            dash_x = map_x
            dash_y = 1
            xdelta, ydelta = self.render_dash(dash_y, dash_x, stdscr)
            py = dash_y + ydelta + 1
            px = dash_x
            command = self.__prompt(py, px, f"{self.name} >> ", stdscr)
            time.sleep(1)  # Only For testing Purposes
            args = command.split()
            try:
                match args[0]:
                    case "add":
                        self.__add(*args[1:], stdscr=stdscr)
                    case "buy":
                        self.__buy(*args[1:])
                    case "move":
                        self.__move(*args[1:])
                    case "attack":
                        self.__attack(*args[1:])
                    case "help":
                        self.__help(stdscr, py + 1, px)
                    case _:
                        raise ValueError(f"Undefined command: {args[0]}")
            except BaseException as err:
                stdscr.addstr(py + 1, px, f"Error: {err}\n")
                stdscr.refresh()

    def __help(self, stdscr: curses.window, p_y: int, p_x: int) -> None:
        # TODO: Update to match valid commands
        stdscr.addstr(p_y, p_x, "Available commands:\n")
        stdscr.addstr(p_y + 1, p_x, "help\n")
        stdscr.refresh()

    def __add(self, team: str, player_name: str, stdscr: curses.window) -> None:
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
                player.row = 0
                player.column = self.size - 1
                self.red[player_name] = player
                self.squares[player.row][player.column].incoming(player)
            case "blue":
                if len(self.blue) >= self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                player.row = self.size - 1
                player.column = 0
                self.blue[player_name] = player
                self.squares[player.row][player.column].incoming(player)
        # TODO: add px, py for better control and reliablity
        stdscr.addstr(f"Team Red: {self.red}\nTeam Blue: {self.blue}")

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
        distance = (
            (defender.row - attacker.row) ** 2
            + (defender.column - attacker.column) ** 2
        ) ** 0.5
        if attacker.attack_range < distance:
            pass
        else:
            defender.hp -= attacker.attack_score

    def __move(self, direction: str, player_name: str) -> None:
        player = self.__get_player(player_name)
        if player is None:
            raise ValueError("Player not found")

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

    def __get_player(self, player_name: str) -> Player.Player | None:
        if player_name in self.blue:
            return self.blue[player_name]
        if player_name in self.red:
            return self.red[player_name]
        return None

    def __prompt(self, p_y: int, p_x: int, prompt: str, stdscr: curses.window) -> str:
        chr = ""
        left = ""
        command = ""
        stdscr.addstr(p_y, p_x, (" " * curses.LINES))
        stdscr.addstr(p_y, p_x, prompt)
        p_x += len(prompt)
        type_limit = p_x
        while chr != "\n":
            chr = stdscr.getkey(p_y, p_x - 1)
            while chr in ["KEY_RIGHT", "KEY_LEFT", "KEY_UP", "KEY_BACKSPACE"]:
                if chr == "KEY_RIGHT":
                    while chr == "KEY_RIGHT":
                        if left != "":
                            command = command + left[:1]
                            left = left[1:]
                            p_x += 1
                        chr = stdscr.getkey(p_y, p_x - 1)
                if chr == "KEY_LEFT":
                    while chr == "KEY_LEFT":
                        if p_x > type_limit:
                            left = command[-1:] + left
                            command = command[:-1]
                            p_x -= 1
                        chr = stdscr.getkey(p_y, p_x - 1)
                # TODO: Add coomand History
                if chr == "KEY_UP":
                    while chr == "KEY_UP":
                        chr = stdscr.getkey(p_y, p_x - 1)
                if chr == "KEY_DOWN":
                    while chr == "KEY_DOWN":
                        chr = stdscr.getkey(p_y, p_x - 1)
                if chr == "KEY_BACKSPACE":
                    while chr == "KEY_BACKSPACE":
                        if p_x > type_limit:
                            command = command[:-1]
                            p_x -= 1
                            if left != "":
                                stdscr.addstr(p_y, p_x - 1, " " * (curses.LINES - 1))
                                stdscr.addstr(p_y, p_x - 1, left)
                            else:
                                stdscr.addstr(p_y, p_x - 1, " ")
                        chr = stdscr.getkey(p_y, p_x - 1)
                if chr == "KEY_DC":
                    while chr == "KEY_DC":
                        if left != "":
                            left = left[1:]
                            if left != "":
                                stdscr.addstr(p_y, p_x - 1, " " * (curses.LINES - 1))
                                stdscr.addstr(p_y, p_x - 1, left)
                        chr = stdscr.getkey(p_y, p_x - 1)
            if p_x < ((curses.COLS) - 1):
                p_x += 1
                if chr != "\n":
                    if left != "":
                        stdscr.addstr(p_y, p_x - 1, " " * (curses.LINES - 1))
                        stdscr.addstr(p_y, p_x - 1, left)
                    stdscr.addstr(p_y, p_x - 2, chr)
                command = command + chr
        if left != "":
            command = command[:-1]
            command = command + left
            command += "\n"
        stdscr.addstr(p_y, p_x, "\n")
        stdscr.refresh()
        return command

    def __screen_size(self, stdscr: curses.window) -> None:
        min_width = 21
        min_hight = 27
        while curses.LINES < min_hight or curses.COLS < min_width:
            stdscr.clear()
            curses.update_lines_cols()
            stdscr.addstr(0, 0, f"Min size is {min_hight}px x {min_width}px")
            stdscr.addstr(1, 0, f"Current Size is {curses.LINES}px x {curses.COLS}px")
            stdscr.refresh()

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


class Square:
    """"""

    def __init__(self, size: int = 6) -> None:
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

    def incoming(self, player: Player.Player) -> None:
        """"""
        self.players.append(player)

    def outgoing(self, player: Player.Player) -> None:
        """"""
        self.players.remove(player)

    def render(self, y: int, x: int, stdscr: curses.window) -> tuple:
        """"""
        square_y = y * (self.__size + 1)
        square_x = x * (self.__size + 1)
        stdscr.addstr(square_y, square_x, "-" * (self.__size + 2))
        for i in range(1, self.__size + 1):
            player = self.players[i - 1] if i - 1 < len(self.players) else None
            stdscr.addstr(
                square_y + i,
                square_x,
                "|"
                + (
                    " " * self.__size
                    if player is None
                    else f"{player.get_short_name():^{self.size}}"[0 : self.size]
                )
                + "|",
            )
        stdscr.addstr(square_y + self.__size + 1, square_x, "-" * (self.__size + 2))
        return self.size + 2, self.size + 2

    def is_full(self) -> bool:
        """"""
        return len(self.players) == self.__size
