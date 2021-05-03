# -*- coding: latin-1 -*-
#@author: Nicolas
"""
Modification du code Laboratoire2-codesQ4 qui permet de trouver la 
longueur d'onde où la puissance spectrale d'une étoile est maximale,
avec a=5 et epsilon suffisamment petit.
"""

from math import exp 
#On importe seulement la fonction exponentielle du module math

x = 5 
"""On donne à x une valeur supérieure à celle qu'on recherche, puisque
a est multiplié par un nombre plus petit que 1, car on multiplie par 
(1 - e ** quelque chose)"""
erreur = x - 5 * (1 - exp(-x)) 
#L'erreur est définie comme la différence entre y = x et y = a * (1 - exp(-x))

while erreur > 1e-8: 
    """On répète les calculs jusqu'à ce que notre 
    approximation soit plus précise que l'erreur tolérée"""
    x = 5 * (1 - exp(-x)) 
    """On calcule un nouveau x, qui est toujours supérieur à la 
    vraie valeur de x"""
    erreur = x - 5 * (1 - exp(-x)) 
    """On calcule une nouvelle erreur, avec la même
    définition que l'ancienne"""

b = 6.62607004e-34 * 299792458 / (x * 1.38064852e-23) 
"""On calcule la constante de Wein, utile pour le calcul de la 
longueur d'onde émise par un corps noir"""
print('La constante de Wein est égale à',b)
i = 1

while i != 0: 
    """La boucle crée ici est infinie, mais l'instruction break permet 
    d'arrêter la boucle"""
    temperature = float(input('Température de l\'étoile \
dont on recherche la longueur d\'onde (en Kelvin):'))
    if temperature == 0: 
        """Le seul moyen d'arrêter la boucle est de passer par 
        cette instruction break, et de donner au programme le zéro
        absolu à calculer"""
        break
    lambdaMax = b / temperature
    """On trouve la longueur d'onde où la puissance spectrale est maximale
    avec lambda=b/T"""
    print('La puissance spectrale de l\'étoile est maximale quand la \
longueur d\'onde de celle-ci est égale à:',lambdaMax)