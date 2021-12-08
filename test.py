# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from myparser import *

auto = Automate.creationAutomate("exempleAutomate.txt")
det_auto = Automate.determinisation(auto)


print(det_auto)