# -*- coding: latin-1 -*-
#@author: Nicolas
from math import *

p1 = 130e3
p2 = 11e3

pm = (p1+p2) / 2

t = -log((((1-exp(-1)) * (pm - p1)) - pm + p1) / (p1 - pm))

print(t)