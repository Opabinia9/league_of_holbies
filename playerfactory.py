#!/usr/bin/python3
Player = __import__("Player").Player
from sub_player import *


def PlayerFactory(player):
    players = {
        "Yasuo": Yasuo,
        "Yurnero": Yurnero,
        "Ashe": Ashe,
        "MoghulKhan": MoghulKhan,
        "Gangplank": Gangplank,
        "Teemo": Teemo,
        "Meepo": Meepo,
        "Pudge": Pudge,
        "MissFortune": MissFortune,
        "Barathrum": Barathrum,
    }

    if not isinstance(player, str):
        raise TypeError("player name must be string.")

    if player not in players:
        raise ValueError("player not found")

    return [players][player]()
