#!/usr/bin/python3

from Player import Player


class Yasuo(Player):
    def __init__(self):
        super().__init__(
            name="Yasuo",
            hp=800,
            mana=0,
            gold=600,
            inventory=[],
            attack_score=100,
            attack_range=1,
        )

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class Yurnero(Player):
    def __init__(self):
        super().__init__("Yurnero", 800, 200, 600, [], 60)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class Ashe(Player):
    def __init__(self):
        super().__init__(
            name="Ashe",
            hp=200,
            mana=0,
            gold=600,
            inventory=[],
            attack_score=60,
            attack_range=3,
        )

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class MoghulKhan(Player):
    def __init__(self):
        super().__init__("Moghul Khan", 1200, 400, 600, [], 40)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class Gangplank(Player):
    def __init__(self):
        super().__init__("Gangplank", 900, 600, 600, [], 40)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class Teemo(Player):
    def __init__(self):
        super().__init__("Teemo", 500, 600, 600, [], 40)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class Meepo(Player):
    def __init__(self):
        super().__init__("Meepo", 1200, 0, 600, [], 40)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class Pudge(Player):
    def __init__(self):
        super().__init__("Pudge", 1200, 124, 600, [], 80)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("Beware of my hook")

    def get_short_name(self):
        return self.name[:3]


class MissFortune(Player):
    def __init__(self):
        super().__init__("Miss Fortune", 1200, 0, 600, [], 40)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("move")

    def get_short_name(self):
        return self.name[:3]


class Barathrum(Player):
    def __init__(self):
        super().__init__("Barathrum", 1200, 0, 600, [], 40)

    def attack(self):
        print(f"{self.name} is attacking with")

    def move(self):
        print("17%")

    def get_short_name(self):
        return self.name[:3]
