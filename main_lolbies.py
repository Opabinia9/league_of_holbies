#!/usr/bin/env python3


Map = __import__("map").Map
Summoner = __import__("summoner").Summoner

lucian = Summoner("Lucian", 800, 500)
warwick = Summoner("Warwick", 740, 550)
nami = Summoner("Nami", 830, 460)
velkoz = Summoner("Vel'koz", 620, 420)
caitlin = Summoner("Caitlin", 580, 380)
garen = Summoner("Garen", 640, 0)
renekton = Summoner("Renekton", 620, 0)
bard = Summoner("Bard", 600, 400)
shaco = Summoner("Shaco", 580, 440)
lulu = Summoner("Lulu", 580, 380)

blue_team = [lucian]
red_team = [garen]


ranked = Map("Summoner's Rift", blue_team, red_team)

print(ranked)
print(ranked.print_map())
