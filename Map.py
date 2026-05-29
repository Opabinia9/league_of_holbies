# import curses
#!/usr/bin/env python3


from playerfactory import PlayerFactory
from itemfactory import ItemFactory
import curses
import time


class Map:
    __COUNT = 0
    __ALLOWED_TEAMS = ("blue", "red")
    __PLAYER_PER_TEAM = 2

    def __init__(self, name, blue={}, red={}, size=8):
        if Map.__COUNT >= 1:
            raise ValueError("Only One Map is Allowed")
        Map.__COUNT += 1
        self.name = name
        if blue is not None:
            self.blue = blue
        if red is not None:
            self.red = red
        self.size = size
        self.__squares = []
        for row in range(self.size):
            col = []
            for column in range(self.size):
                col.append(Square())
            self.__squares.append(col)

    def __del__(self):
        Map.__COUNT = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def red(self):
        return self.__red

    @red.setter
    def red(self, players):
        if not isinstance(players, dict):
            raise TypeError("Players Must be a Dictionary.")
        self.__red = {}

    @property
    def blue(self):
        return self.__blue

    @blue.setter
    def blue(self, players):
        if not isinstance(players, dict):
            raise TypeError("Players Must be a Dictionary.")
        self.__blue = {}

    def __str__(self):
        map_name = f"Map Name: {self.name}"
        border = f"*" * len(map_name)
        str = border + "\n" + map_name + "\n"
        str += f"\tBlue Team:" + "\n"
        for summoner in self.blue:
            str += "\t" * 2 + f"{summoner}" + "\n"
        str += f"\tRed Team:" + "\n"
        for summoner in self.red:
            str += "\t" * 2 + f"{summoner}" + "\n"
        str += border + "\n"
        return str

    @property
    def squares(self):
        return self.__squares

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    def print_map(self):
        out, occupied = "", "   "
        border = "|---"
        space = f"|   "
        out += f"-" * (4 * self.size + 1) + "\n"
        for row in range(self.size):
            out += "|"
            for i in range(self.size):
                out += self.__squares[row][i].top() + "|"
            out += "\n|"
            for j in range(self.size):
                out += self.__squares[row][j].mid() + "|"
            out += "\n|"
            for k in range(self.size):
                out += self.__squares[row][k].bot() + "|"
            out += "\n"
            out += f"-" * (4 * self.size + 1) + "\n"
        return out

    def launch_game(self, stdscr):
        self.__screen_size(stdscr)
        while True:
            # stdscr.clear() # This is commented out so it doesnt clear prompt outputs
            stdscr.addstr(0, 0, f"welcome to {self.name}\n")
            stdscr.addstr(1, 0, self.print_map())
            # TODO: Set Gen py dinamicaly based on map, px is fine at 0
            px = 0
            py = 22
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
                    case "help":
                        self.__help(stdscr, py + 1, px)
                    case _:
                        raise ValueError(f"Undefined command: {args[0]}")
            except BaseException as err:
                stdscr.addstr(py + 1, px, f"Error: {err}\n")
                stdscr.refresh()

    def __help(self, stdscr, p_y, p_x):
        # TODO: Update to match valid commands
        stdscr.addstr(p_y, p_x, "Available commands:\n")
        stdscr.addstr(p_y + 1, p_x, "help\n")
        stdscr.refresh()

    def __add(self, team, player_name, stdscr):
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
                player.row = self.size - 1
                player.column = 0
                self.red[player_name] = player
                self.__squares[player.row][player.column].incoming(player)
            case "blue":
                if len(self.blue) >= self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                player.row = 0
                player.column = self.size - 1
                self.blue[player_name] = player
                self.__squares[player.row][player.column].incoming(player)
        # TODO: add px, py for better control and reliablity
        stdscr.addstr(f"Team Red: {self.red}\nTeam Blue: {self.blue}")

    def __buy(self, item_name, player_name):
        player = self.__get_player(player_name)
        if player is None:
            raise ValueError(f"Inactive player ({player_name}) cannot buy item")
        item = ItemFactory(item_name)
        player.buy(item)

    def __move(self, direction, player_name):
        player = self.__get_player(player_name)
        if player is None:
            raise ValueError("Player not found")

        current_square = self.__squares[player.row][player.column]
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

        target_square = self.__squares[target_row][target_column]
        if target_square.is_full():
            raise ValueError("Target square is full")

        current_square.outgoing(player)
        target_square.incoming(player)
        player.row = target_row
        player.column = target_column

    def __get_player(self, player_name):
        if player_name in self.blue:
            return self.blue[player_name]
        if player_name in self.red:
            return self.red[player_name]
        return None

    def __prompt(self, p_y, p_x, prompt, stdscr):
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

    def __screen_size(self, stdscr):
        min_width = 21
        min_hight = 27
        while curses.LINES < min_hight or curses.COLS < min_width:
            stdscr.clear()
            curses.update_lines_cols()
            stdscr.addstr(0, 0, f"Min size is {min_hight}px x {min_width}px")
            stdscr.addstr(1, 0, f"Current Size is {curses.LINES}px x {curses.COLS}px")
            stdscr.refresh()


class Square:
    def __init__(self, size=3):
        self.__size = size
        self.players = []

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, players):
        self.__players = players

    def incoming(self, player):
        self.players.append(player)

    def outgoing(self, player):
        self.players.remove(player)

    def top(self):
        if len(self.players) == self.__size:
            return self.players[self.__size - 1].get_short_name()
        return f" " * self.__size

    def mid(self):
        if len(self.players) > 0:
            return self.players[0].get_short_name()
        return f" " * self.__size

    def bot(self):
        if len(self.players) == 2:
            return self.players[1].get_short_name()
        return f" " * self.__size

    def is_full(self):
        return len(self.players) == self.__size
