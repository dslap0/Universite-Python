# -*- coding: latin-1 -*-
#@author: Nicolas
"""
Ce code sert à calculer les zéros d'une équation polynomiale de degré 2
"""

a,b,c = 2,5,2 #coefficients
r = b**2-4*a*c #r est le terme sous la racine carrée
rr = r**0.5 #rr est la racine carrée de r
x1 = str((-b+rr) / (2*a)) #premiere racine
x2 = str((-b-rr) / (2*a)) #deuxieme racine
print('premiere racine='+x1)
print('deuxieme racine='+x2)