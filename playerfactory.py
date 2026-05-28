#!/usr/bin/python3
Player = __import__("Player").Player

"""class SamPlayer(Player):
    def __init__(self):
        super().__init__("Sam", 100, 20, 20, 2000, ["gold"], 10)"""

def PlayerFactory(player):
    players = {
        "Yasuo": Yasuo()
        "Yurnero": Yurnero()
        "Ashe": Ashe()
        "MoghulKhan": MoghulKhan()
        "Gangplank": Gangplank()
        "Teemo": Teemo()
        "Meepo": Meepo()
        "Pudge": Pudge()
        "MissFortune": MissFortune()
        "Barathrum": Barathrum()
    }

    if not isinstance(player, str):
        raise TypeError("player name must be string.")

    if player not in players:
        raise ValueError("player not found")

    return players[player]()

"""if __name__ == "__main__":
    samcharacter = PlayerFactory("Sam")
    print(samcharacter)"""
