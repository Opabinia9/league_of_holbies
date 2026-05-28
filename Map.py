#!/usr/bin/env python3


# Summoner = __import__("summoner").Summoner
from playerfactory import PlayerFactory
from itemfactory import ItemFactory


class Map:
    __COUNT = 0
    __ALLOWED_TEAMS = ("blue", "red")
    __PLAYER_PER_TEAM = 2
    print_symbol = "12345"
    champion_symbol = "C"

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
        for y in range(self.size):
            for x in range(self.size):
                self.__squares.append(square(x, y, self.size))

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
        out = ""
        out += "-" * (self.size + 4) + "\n"
        for y in range(self.size):
            out += "| "
            for x in range(self.size):
                sq = None
                for s in self.__squares:
                    if s.coordinates[0] == x and s.coordinates[1] == y:
                        sq = s
                        break

                out += Map.print_symbol
                if x == self.size - 1:
                    out += " |"

            if y != self.size - 1:
                out += "\n"
        out += "\n" + "-" * (self.size + 4) + "\n"

        return out

    def launch_game(self):
        print(f"welcome to {self.name}")
        while True:
            command = input(f"{self.name} >> ")
            args = command.split()
            try:
                match args[0]:
                    case "add":
                        self.__add(*args[1:])
                    case "buy":
                        self.__buy(*args[1:])
                    case "help":
                        self.__help()
                    case _:
                        raise ValueError(f"Undefined command: {args[0]}")
            except BaseException as err:
                print(f"Error: {err}")

    def __help(self):
        print("Available commands:")
        print("help")

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
                self.red[player_name] = player
            case "blue":
                if len(self.blue) >= self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                self.blue[player_name] = player
        print("New player added")
        print(f"Team Red: {self.red}\nTeam Blue: {self.blue}")

    def __buy(self, item_name, player_name):
        player = self.__get_player(player_name)
        if player is None:
            raise ValueError(f"Inactive player ({player_name}) cannot buy item")
        item = ItemFactory(item_name)
        player.buy(item)

    def __get_player(self, player_name):
        if player_name in self.blue:
            return self.blue[player_name]
        if player_name in self.red:
            return self.red[player_name]
        return None


class square:
    def __init__(self, x, y, size=4):
        self.coordinates = [x, y, size]

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, y):
        if y > self.size:
            raise ValueError("there is no space for your space!")
        self.__row = y

    @property
    def column(self):
        return self.__column

    @column.setter
    def column(self, x):
        if x > self.size:
            raise ValueError("there is no space for your space!")
        self.__column = x
