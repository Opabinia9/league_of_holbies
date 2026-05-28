#!/usr/bin/env python3


# Summoner = __import__("summoner").Summoner
from playerfactory import PlayerFactory


class Map:
    __COUNT = 0
    __ALLOWED_TEAMS = ("blue", "red")
    __PLAYER_PER_TEAM = 2
    print_symbol = "12345"
    champion_symbol = "C"

    def __init__(self, name, blue=[], red=[], size=8):
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
    def red(self, summoners):
        if not isinstance(summoners, list):
            raise TypeError("Summoners Must be a List.")
        self.__red = []
        for summoner in summoners:
            self.add_summoner(summoner, "red")

    @property
    def blue(self):
        return self.__blue

    @blue.setter
    def blue(self, summoners):
        if not isinstance(summoners, list):
            raise TypeError("Summoners Must be a List.")
        self.__blue = []
        for summoner in summoners:
            self.add_summoner(summoner, "blue")

    def add_summoner(self, summoner, team):
        if team not in Map.ALLOWED_TEAMS:
            raise ValueError("Team must be either blue or red.")
        if team == "red":
            if len(self.red) >= 5:
                raise ValueError("Red Team Must Have 5 Players.")
            summoner.team = "red"
            self.red.append(summoner)
        if team == "blue":
            if len(self.blue) >= 5:
                raise ValueError("Blue Team Must Have 5 Players.")
            summoner.team = "blue"
            self.blue.append(summoner)

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
        print(f"Welcome to {self.name}")
        while True:
            command = input(f"{self.name} >> ")
            args = command.split()
            match args[0]:
                case "add":
                    self.__add(*args[1:])
                case "help":
                    self.__help()
                case _:
                    print(f"Undefined command: {args[0]}")

    def __help(self):
        print("Available commands:")
        print("help")

    def __add(self, team, player_name):
        if type(team) is not str:
            raise TypeError("Team should be a string")
        if team not in self.__ALLOWED_TEAMS:
            raise ValueError("Invalid Team")
        match team:
            case "red":
                if len(self.red) > self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                self.red.append(player)
            case "blue":
                if len(self.blue) > self.__PLAYER_PER_TEAM:
                    raise ValueError("Team already full")
                player = PlayerFactory(player_name)
                self.blue.append(player)


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
