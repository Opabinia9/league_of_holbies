#!/usr/bin/python3

class doran_blade(item):
    def __init__(self):
        super().__init__("Doran", 450, 10, 0)

    def use(self, user):
        print(f"{user} is attacking with {self.name}")

class doran_shield(item):
    def __init__(self):
        super().__init__("Doran's Shield", 450, 0, 1)

    def use(self, user):
        print(f"{user} is blocking")

class doran_bow(item):
    def __init__(self):
        super().__init__("Doran's Bow", 400, 8, 0)

    def use(self, user):
        print(f"{user} attack is increasing")

class Amplify_Tomb(item):
    def __init__(self):
        super().__init__("Amplifying Tomb", 450, 20, 0)

    def use(self, user):
        print(f"{user} is using magic")

class B_F(item):
    def __init__(self):
        super().__init__("B.F Sword", 1300, 40, 0)

    def use(self, user):
        print(f"{user} is swinging the sword")

class Chain_Vest(item):
    def __init__(self):
        super().__init__("Chain Vest", 800, 0, 40)

    def use(self, user):
        print(f"{user} is defending")

class pickaxe(item):
    def __init__(self):
        super().__init__("Pickaxe", 875, 25, 0)

    def use(self, user):
        print(f"{user} is attacking")

class guardian_angel(item):
    def __init__(self):
        super().__init__("Guardian Angel", 3200, 55, 45)

    def use(self, user):
        print(f"{user} is attacking")

class steel_sigil(item):
    def __init__(self):
        super().__init__("Steel Sigil", 1100, 15, 30)

    def use(self, user):
        print(f"{user} is ???")

class Actualizer(item):
    def __init__(self):
    super().__init__("Actualizer", 2650, 90, 0)
    
    def use(self, user):
    print(f"{user} is attacking")
    
class Archangels_Staff(item):
    def __init__(self):
    super().__init__("Archangels Staff", 2900, 70, 0)
    
    def use(self, user):
    print(f"{user} is attacking with magic")
    
class Warmogs_armor(item):
    def __init__(self):
    super().__init__("Warmogs Armor", 3100, 0, 100)
    
    def use(self, user):
    print(f"{user} is blocking")

class Thornmail(item):
    def __init__(self):
    super().__init__("Thornmail", 2450, 0, 75)
    
    def use(self, user):
    print(f"{user} is blocking")
