# -*- coding: latin-1 -*-
#@author: Nicolas
"""
Code visant à calculer la réponse à l'équation x=a*(1-e**x) avec une
erreur notée epsilon, où a est un nombre réel.
"""

from math import exp #On importe seulement la fonction exponentielle

a,epsilon=(input('Veuillez entrez la valeur de a et de epsilon désirées,\
séparées par une virgule et un espace:').split(', '))
a,epsilon=float(a),float(epsilon)

x = a 
"""On donne à x une valeur supérieure à celle qu'on recherche, puisque 
a est multiplié par un nombre plus petit que 1"""
erreur = x - a * (1 - exp(-x)) 
#L'erreur est définie comme la différence entre #y=x et y=a*(1-exp(-x))
numeroIteration=1
print(str(numeroIteration)+'. x:',x,'erreur:',erreur)
#On affiche la première estimation, où x=a

while erreur > epsilon: 
    """On répète les calculs jusqu'à ce que notre approximation soit plus 
    précise que l'erreur tolérée"""
    x = a * (1 - exp(-x)) 
    """On calcule un nouveau x, qui est toujours supérieur à la vraie 
    valeur de x"""
    erreur = x - a * (1 - exp(-x)) 
    #On calcule une nouvelle erreur, avec la même définition que l'ancienne
    numeroIteration += 1
    print(str(numeroIteration)+'. x:',x,'erreur:',erreur) 
    """On affiche le résultat et le nombre de fois que les calculs ont été effectués"""