#!/usr/bin/python3
"""Player Class"""

from Item_class import Item
from abc import abstractmethod


class Player:
    """"""

    __MAX_ITEMS = 6

    @abstractmethod
    def attack(self): ...

    def buy(self, item: Item):
        if type(item) is not Item:
            raise TypeError("item must be an Item object")
        if item.price > self.gold:
            raise BaseException("Not Enough Gold!!!")

    @abstractmethod
    def move(self): ...

    @abstractmethod
    def get_short_name(self): ...
