#!/usr/bin/python3
Item = __import__('items').Item

def ItemFactory(item):
    items = {
        "DoranBlade": DoranBlade,
        "DoranShield": DoranShield,
        "DoranBow": DoranBow,
        "AmplifyTomb": AmplifyTomb,
        "BFSword": BFSword,
        "ChainVest": ChainVest,
        "Pickaxe": Pickaxe,
        "GuardianAngel": GuardianAngel,
        "SteelSigil": SteelSigil,
        "Actualizer": Actualizer,
        "DivineRapier": DivineRapier,
        "ArchangelsStaff": ArchangelsStaff,
        "WarmogsArmor": WarmogsArmor,
        "Thornmail": Thornmail,
    }

    if not isinstance(item, str):
        raise TypeError("Item should be a string.")

    if item not in items:
        raise ValueError("Item not found.")
    
    return items[item]()
