#!/usr/bin/python3
"""Player Class"""

from abc import abstractmethod


class Player:
    """"""

    MAX_ITEMS = 6

    @abstractmethod
    def attack(self): ...

    @abstractmethod
    def buy(self): ...

    @abstractmethod
    def move(self): ...

    @abstractmethod
    def get_short_name(self): ...
