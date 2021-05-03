# -*- coding: latin-1 -*-
#@author: Nicolas
"""
Code visant � calculer la r�ponse � l'�quation x=a*(1-e**x) avec une
erreur not�e epsilon, o� a est un nombre r�el.
"""

from math import exp #On importe seulement la fonction exponentielle

a,epsilon=(input('Veuillez entrez la valeur de a et de epsilon d�sir�es,\
s�par�es par une virgule et un espace:').split(', '))
a,epsilon=float(a),float(epsilon)

x = a 
"""On donne � x une valeur sup�rieure � celle qu'on recherche, puisque 
a est multipli� par un nombre plus petit que 1"""
erreur = x - a * (1 - exp(-x)) 
#L'erreur est d�finie comme la diff�rence entre #y=x et y=a*(1-exp(-x))
numeroIteration=1
print(str(numeroIteration)+'. x:',x,'erreur:',erreur)
#On affiche la premi�re estimation, o� x=a

while erreur > epsilon: 
    """On r�p�te les calculs jusqu'� ce que notre approximation soit plus 
    pr�cise que l'erreur tol�r�e"""
    x = a * (1 - exp(-x)) 
    """On calcule un nouveau x, qui est toujours sup�rieur � la vraie 
    valeur de x"""
    erreur = x - a * (1 - exp(-x)) 
    #On calcule une nouvelle erreur, avec la m�me d�finition que l'ancienne
    numeroIteration += 1
    print(str(numeroIteration)+'. x:',x,'erreur:',erreur) 
    """On affiche le r�sultat et le nombre de fois que les calculs ont �t� effectu�s"""