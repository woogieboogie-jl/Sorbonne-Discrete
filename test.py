# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from myparser import *

auto0 = Automate.creationAutomate("exempleAutomate0.txt")
auto1 = Automate.creationAutomate("exempleAutomate1.txt")
autostar = Automate.etoile(auto1)
autodeter = Automate.determinisation(auto1)
autoComplet = Automate(autodeter,"a,b")
autoComplementaire = Automate.complementaire(autoComplet)
autoIntersection = Automate.intersection(auto0,auto1)
autoUnion = Automate.union(auto0,auto1)
autoEtoile = Automate.etoile(auto0)

print(auto0)
print(auto1)
print("============================\n")
print(autodeter)
print(autoComplet)
print(autoComplementaire)
print("============================\n")
print(autoIntersection)
print(autoUnion)
print("============================\n")
print(autoEtoile)
