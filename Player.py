#!/usr/bin/python3
"""Player Class"""

class Player:
    """"""

    __MAX_ITEMS = 6

    def __init__(self, name, hp, mana, gold, inventory, attack_score):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.gold = gold
        self.inventory = inventory
        self.attack_score = attack_score

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

    """Name of user/champion"""
    @property
    def name(self):
        return self.__name

    @name.setter(self, name):
        self.__name = name

    """Hp of user/champion"""
    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, hp):
        self.__hp = hp

    """Mana of user/champion"""
    @property
    def mana(self):
        return self.__mana

    @mana.setter
    def mana(self):
        self.__mana = mana

    """Current gold"""
    @property
    def gold(self):
        return self.__gold

    @gold.setter(self, gold):
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
        if inventory > MAX_ITEMS:
            raise ValueError("Cannot have more than 6 items at a time")
            """Drop on ground maybe"""
        self.__inventory = inventory

    @property
    def attack_score(self):
        return self.__attack_score

    @attack_score.setter(self, attack_score):
        if type(attack_score) is not int:
            raise TypeError:("Attack score should be an integer")
        self.__attack_score = attack_score

    def __str__(self):
        if self.__hp < 0:
            return f"{name} has been pwned"
        if self.__mana < mana: #placeholder, not 100% confident if logic is correct
            return "Not enough mana"
