#!/usr/bin/python3
Item = __import__('items').Item

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
