# -*- coding: latin-1 -*-
#@author: Nicolas
"""
Modification du code Laboratoire2-codesQ4 qui permet de trouver la 
longueur d'onde o� la puissance spectrale d'une �toile est maximale,
avec a=5 et epsilon suffisamment petit.
"""

from math import exp 
#On importe seulement la fonction exponentielle du module math

x = 5 
"""On donne � x une valeur sup�rieure � celle qu'on recherche, puisque
a est multipli� par un nombre plus petit que 1, car on multiplie par 
(1 - e ** quelque chose)"""
erreur = x - 5 * (1 - exp(-x)) 
#L'erreur est d�finie comme la diff�rence entre y = x et y = a * (1 - exp(-x))

while erreur > 1e-8: 
    """On r�p�te les calculs jusqu'� ce que notre 
    approximation soit plus pr�cise que l'erreur tol�r�e"""
    x = 5 * (1 - exp(-x)) 
    """On calcule un nouveau x, qui est toujours sup�rieur � la 
    vraie valeur de x"""
    erreur = x - 5 * (1 - exp(-x)) 
    """On calcule une nouvelle erreur, avec la m�me
    d�finition que l'ancienne"""

b = 6.62607004e-34 * 299792458 / (x * 1.38064852e-23) 
"""On calcule la constante de Wein, utile pour le calcul de la 
longueur d'onde �mise par un corps noir"""
print('La constante de Wein est �gale �',b)
i = 1

while i != 0: 
    """La boucle cr�e ici est infinie, mais l'instruction break permet 
    d'arr�ter la boucle"""
    temperature = float(input('Temp�rature de l\'�toile \
dont on recherche la longueur d\'onde (en Kelvin):'))
    if temperature == 0: 
        """Le seul moyen d'arr�ter la boucle est de passer par 
        cette instruction break, et de donner au programme le z�ro
        absolu � calculer"""
        break
    lambdaMax = b / temperature
    """On trouve la longueur d'onde o� la puissance spectrale est maximale
    avec lambda=b/T"""
    print('La puissance spectrale de l\'�toile est maximale quand la \
longueur d\'onde de celle-ci est �gale �:',lambdaMax)