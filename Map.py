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

    # def __str__(self):
    #     map_name = f"Map Name: {self.name}"
    #     border = f"*" * len(map_name)
    #     str = border + "\n" + map_name + "\n"
    #     str += f"\tBlue Team:" + "\n"
    #     for summoner in self.blue:
    #         str += "\t" * 2 + f"{summoner}" + "\n"
    #     str += f"\tRed Team:" + "\n"
    #     for summoner in self.red:
    #         str += "\t" * 2 + f"{summoner}" + "\n"
    #     str += border + "\n"
    #     return str

    def render_dash(self, y, x, stdscr):
        map_name = f"{self.name}"
        border = "*" * len(map_name)
        stdscr.addstr(y, x, border)
        current_y = y + 1
        stdscr.addstr(current_y, x, map_name)
        current_y += 1
        stdscr.addstr(current_y, x + 4, "Blue Team:")
        current_y += 1
        for summoner in self.blue:
            player = self.__get_player(summoner)
            stdscr.addstr(current_y, x + 8, f"{summoner}: HP: {player.hp}")
            current_y += 1
        stdscr.addstr(current_y, x + 4, "Red Team:")
        current_y += 1
        for summoner in self.red:
            player = self.__get_player(summoner)
            stdscr.addstr(current_y, x + 8, f"{summoner}: HP: {player.hp}")
            current_y += 1
        stdscr.addstr(current_y, x, border)
        width = len(border)
        height = current_y - y + 1

        return width, height

    @property
    def squares(self):
        return self.__squares

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    # def print_map(self):
    #     out, occupied = "", "   "
    #     border = "|---"
    #     space = f"|   "
    #     out += f"-" * (4 * self.size + 1) + "\n"
    #     for row in range(self.size):
    #         out += "|"
    #         for i in range(self.size):
    #             out += self.__squares[row][i].top() + "|"
    #         out += "\n|"
    #         for j in range(self.size):
    #             out += self.__squares[row][j].mid() + "|"
    #         out += "\n|"
    #         for k in range(self.size):
    #             out += self.__squares[row][k].bot() + "|"
    #         out += "\n"
    #         out += f"-" * (4 * self.size + 1) + "\n"
    #     return out

    def print_map(self, stdscr):
        map_x, map_y = 0, 0
        for y, row in enumerate(self.__squares):
            for x, square in enumerate(row):
                square.render(y, x, stdscr)
        map_x = self.size * (Square().size + 2)
        map_y = self.size * (Square().size + 2)
        return map_x, map_y

    def launch_game(self, stdscr):
        # print(f"welcome to {self.name}")
        while True:
            stdscr.clear()
            #           stdscr.addstr(self.print_map())
            map_x, map_y = self.print_map(stdscr)
            px = 1
            py = map_y + 1
            dash_x = map_x + 4
            dash_y = 1
            self.render_dash(dash_y, dash_x, stdscr)
            command = self.__prompt(py, px, f"{self.name} >> ", stdscr)
            time.sleep(1)
            args = command.split()
            try:
                match args[0]:
                    case "add":
                        self.__add(*args[1:])
                    case "buy":
                        self.__buy(*args[1:])
                    case "move":
                        self.__move(*args[1:])
                    case "attack":
                        self.__attack(*args[1:])
                    case "help":
                        self.__help()
                    case _:
                        raise ValueError(f"Undefined command: {args[0]}")
            except BaseException as err:
                pass
        #         print(f"Error: {err}")
        stdscr.refresh()

    def __help(self):
        ...
        # print("Available commands:")
        # print("help")

    def __add(self, team, player_name):
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
                self.__squares[player.row][player.column].incoming(player)
            case "blue":
                if len(self.blue) >= self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                player.row = self.size - 1
                player.column = 0
                self.blue[player_name] = player
                self.__squares[player.row][player.column].incoming(player)
        # print(f"Team Red: {self.red}\nTeam Blue: {self.blue}")

    def __buy(self, item_name, player_name):
        player = self.__get_player(player_name)
        if player is None:
            raise ValueError(f"Inactive player ({player_name}) cannot buy item")
        item = ItemFactory(item_name)
        player.buy(item)

    def __attack(self, from_plyr, to_plyr):
        attacker = self.__get_player(from_plyr)
        defender = self.__get_player(to_plyr)
        distance = (
            (defender.row - attacker.row) ** 2
            + (defender.column - attacker.column) ** 2
        ) ** 0.5
        if attacker.attack_range < distance:
            pass
        else:
            defender.hp -= attacker.attack_score

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
                if chr == "KEY_UP":
                    while chr == "KEY_UP":
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
        stdscr.addstr(p_y + 1, 1, command)
        stdscr.refresh()
        return command


class Square:
    def __init__(self, size=4):
        self.__size = size
        self.players = []

    @property
    def size(self):
        return self.__size

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

    def render(self, y, x, stdscr):
        square_y = y * (self.__size + 1)
        square_x = x * (self.__size + 1)
        stdscr.addstr(square_y, square_x, f"-" * (self.__size + 2))
        for i in range(1, self.__size + 1):
            player = self.players[i - 1] if i - 1 < len(self.players) else None
            stdscr.addstr(
                square_y + i,
                square_x,
                f"|"
                + (
                    f" " * self.__size
                    if player is None
                    else f"{player.get_short_name():^{self.size}}"[0 : self.size]
                )
                + f"|",
            )
        stdscr.addstr(square_y + self.__size + 1, square_x, f"-" * (self.__size + 2))
        return self.size + 2, self.size + 2

    def is_full(self):
        return len(self.players) == self.__size
