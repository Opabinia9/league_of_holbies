#!/usr/bin/python3
from abc import ABC, abstractmethod
from items import *

"""Player Class"""


class Player(ABC):
    """"""

    __MAX_ITEMS = 6

    def __init__(
        self,
        name,
        hp,
        mana,
        gold,
        inventory,
        attack_score,
        attack_range=1,
        row=0,
        column=0,
    ):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.mana = mana
        self.gold = gold
        self.inventory = inventory
        self.attack_score = attack_score
        self.attack_range = attack_range
        self.row = row
        self.column = column

    @abstractmethod
    def attack(self): ...

    def buy(self, item: Item):
        if type(item) is not Item:
            raise TypeError("item must be an Item object")
        if item.price > self.gold:
            raise BaseException("Not Enough Gold!!!")
        if len(self.inventory) >= self.__MAX_ITEMS:
            raise ValueError("Not enough space in inventory")

        self.gold = self.gold - item.price
        self.inventory.append(self.item)

    @abstractmethod
    def move(self): ...

    def get_short_name(self):
        return self.name[: Square().size].capitalize()

    """Name of user/champion"""

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    """Champion Team"""

    @property
    def team(self):
        return self.__team

    @team.setter
    def team(self, team):
        self.__team = team

    """Hp of user/champion"""

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, hp):
        self.__hp = hp

    @property
    def max_hp(self):
        return self.__maxhp

    @max_hp.setter
    def max_hp(self, hp):
        self.__maxhp = hp

    """Mana of user/champion"""

    @property
    def mana(self):
        return self.__mana

    @mana.setter
    def mana(self, mana):
        self.__mana = mana

    """Current gold"""

    @property
    def gold(self):
        return self.__gold

    @gold.setter
    def gold(self, gold):
        if type(gold) is not int:
            raise TypeError("Gold must be int")
        if gold < 0:
            raise ValueError("Gold cannot be negative")
        self.__gold = gold

    """Inventory status"""

    @property
    def inventory(self):
        return self.__inventory

    @inventory.setter
    def inventory(self, inventory):
        if not type(list):
            raise TypeError("Not List")
        if len(inventory) > self.__MAX_ITEMS:
            raise ValueError("Cannot have more than 6 items at a time")
            """Drop on ground maybe"""
        self.__inventory = inventory

    @property
    def attack_score(self):
        return self.__attack_score

    @attack_score.setter
    def attack_score(self, attack_score):
        if type(attack_score) is not int:
            raise TypeError("Attack score should be an integer")
        self.__attack_score = attack_score

    @property
    def attack_range(self):
        return self.__attack_range

    @attack_range.setter
    def attack_range(self, attack_range):
        if type(attack_range) is not int:
            raise TypeError("Attack range should be an integer")
        if attack_range < 1:
            raise ValueError("Attack range should be at least 1")
        self.__attack_range = attack_range

    def __str__(self):
        return self.name

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, row):
        self.__row = row

    @property
    def column(self):
        return self.__column

    @column.setter
    def column(self, column):
        self.__column = column
