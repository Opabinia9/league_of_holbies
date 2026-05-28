#!/usr/bin/python3
from abc import ABC, abstractmethod

class Item(ABC):

    def __init__(self, name, price, attack_bonus, defense_bonus):
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.price = price
        self.name = name

    @abstractmethod
    def use(self):
        ...

    @property    
    def attack_bonus(self):
        return self.__attack_bonus

    @attack_bonus.setter
    def attack_bonus(self, attack_bonus):
        if not isinstance(attack_bonus, int):
            raise TypeError("Attack bonus should be an integer.")

        self.__attack_bonus = attack_bonus

    @property
    def defense_bonus(self):
        return self.__defense_bonus

    @defense_bonus.setter
    def defense_bonus(self, defense_bonus):
        if not isinstance(defense_bonus, int):
            raise TypeError("Defense bonus should be an integer.")
        self.__defense_bonus = defense_bonus

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if not isinstance(price, int):
            raise TypeError("Price should be an integer.")
        if price <= 0:
            raise ValueError("Price should be positive.")
        self.__price = price

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name should be a string")
        if name == "":
            name = "Itama Ben Gvir's double sided anal plug"
        else:
            self.__name = name

    def __str__(self):
        return f"This is a {self.name}, attack: {self.attack_bonus}, defense: {self.defense_bonus}, price:{self.price}"


class SwordItem(Item):
    def __init__(self):
        super().__init__(10, 0, 42, "Seal clubber")

    def use():
        print(f"Using my Sword")


def ItemFactory(item):
    items = {
        "Sword": SwordItem,
        #"Shield": ShieldItem,
    }

    if not isinstance(item, str):
        raise TypeError("Item should be a string.")

    if item not in items:
        raise ValueError("Item not found.")
    
    return items[item]()


if __name__ == "__main__":
    sword = ItemFactory("Sword")

    print(sword)
