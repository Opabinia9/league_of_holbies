#!/usr/bin/env python3


class Summoner:

    def __init__(self, name, hp, mana):
        self.name = name
        self.hp = hp
        self.mana = mana

    def q_spell(self):
        pass

    def w_spell(self):
        pass

    def e_spell(self):
        pass

    def r_spell(self):
        pass

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def mana(self):
        return self.__mana

    @mana.setter
    def mana(self, mana):
        self.__mana = mana

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, hp):
        self.__hp = hp

    def __str__(self):
        hpstr = "HP:"
        return f"Name:{self.name:<8}\tHP:{self.hp:<8}\tMana:{self.mana:<8}\tTeam:{self.team:<8}\n"

    @property
    def team(self):
        return self.__team

    @team.setter
    def team(self, team):
        self.__team = team
