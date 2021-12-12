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

print(autostar)