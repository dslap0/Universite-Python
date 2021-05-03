# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'int�grale d'une certaine fonction selon la 
m�thode de Simpson et un certain nombre de pas, puis trouve la valeur 
de la pente de la droite de r�gression lin�aire qui sera affich�e sur 
un graphique. Dans ce code, la fonction est : 
3x / (2 * (x + 1) ** (1 / 2))"""

import numpy as np

def fct(x):
    """Cette fonction calcule les valeurs de y associ�es � la fonction
    f(x) = 3 * x / 2 * (x + 1) ** (1 / 2).
    x : valeurs d'abscisses donn�es � la fonction
    """
    y = 3 * x / (2 * np.sqrt(x + 1))
    
    return y

def intSimpson(fct, inf, sup, npt, integraleExacte):
    """Cette fonction sert � calculer l'int�grale de la fonction donn�e
    en argument avec la m�thode de Simpson, en s'assurant que le nombre
    de pas soit conforme.
    
    fct : Fonction � int�gr�e, d�finie plus t�t
    inf : Borne inf�rieure de l'int�grale
    sup : Borne sup�rieure de l'int�grale
    npt : Nombre d'�l�ments � int�grer
    integraleExacte : Valeur exacte de l'int�gale
    """
    if npt % 2 == 0:
        # On v�rifie la valeur de npt et on la change si n�cessaire
        npt += 1
    
    x = np.linspace(inf, sup, npt)
    y = fct(x)

    pas = (sup - inf) / (npt - 1)
    # On trouve le pas entre chaque �l�ment de x
    
    integrale = pas / 3 * (y[0] + np.sum(4 * y[1:-1:2]) + np.sum(2 * \
    y[2:-2:2]) + y[-1])
    
    """On calcule l'int�grale � l'aide de la formule I = pas / 3 * \
    (x[0] + 4 * x[1] + 2 * x[2] + ... + 2 * x[-3] + 4 * x[-2] + x[-1])"""
    
    erreur = abs(integrale - integraleExacte)
    
    return integrale, erreur


npt = np.array([1e3, 1e4, 1e5, 1e6], dtype=np.int64)
# On cr�e une liste qui prend toutes les valeurs de nombre de pas possibles

integraleExacte = 4

"""Par calcul, on trouve que l'int�grale exacte de l'expression �tudi�e entre
0 et 3 vaut 4"""

inf = 0
sup = 3
# On d�finit les bornes d'int�gration

integraleSimpson = np.array([])
erreurSimpson = np.array([])

"""On cr�e un ndarray vide integrale et un ndarray erreur auxquels on 
ajoutera les valeurs des int�gales calcul�es au fur et � mesure des boucles 
d'it�ration""" 

for i in npt:    
    integrale, erreur = intSimpson(fct, inf, sup, i, integraleExacte)
    integraleSimpson = np.append(integraleSimpson, integrale)
    erreurSimpson = np.append(erreurSimpson, erreur)
    # On affecte l'integrale et l'erreur aux ndarrays correspondants

print('La valeur de l\'int�grale et de son erreur associ�e pour un nombre de \
pas N sont :\n' + str(integraleSimpson) + ' et ' + str(erreurSimpson) + '.')

"""On montre l'int�grale et l'erreur associ�e � tous les pas et la pente de la
droite dans l'espace log-log de l'erreur par rapport au pas pour chaque 
m�thode d'int�gration utilis�e"""