# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'intégrale d'une certaine fonction selon la 
méthode de Simpson et un certain nombre de pas, puis trouve la valeur 
de la pente de la droite de régression linéaire qui sera affichée sur 
un graphique. Dans ce code, la fonction est : 
3x / (2 * (x + 1) ** (1 / 2))"""

import numpy as np

def fct(x):
    """Cette fonction calcule les valeurs de y associées à la fonction
    f(x) = 3 * x / 2 * (x + 1) ** (1 / 2).
    x : valeurs d'abscisses données à la fonction
    """
    y = 3 * x / (2 * np.sqrt(x + 1))
    
    return y

def intSimpson(fct, inf, sup, npt, integraleExacte):
    """Cette fonction sert à calculer l'intégrale de la fonction donnée
    en argument avec la méthode de Simpson, en s'assurant que le nombre
    de pas soit conforme.
    
    fct : Fonction à intégrée, définie plus tôt
    inf : Borne inférieure de l'intégrale
    sup : Borne supérieure de l'intégrale
    npt : Nombre d'éléments à intégrer
    integraleExacte : Valeur exacte de l'intégale
    """
    if npt % 2 == 0:
        # On vérifie la valeur de npt et on la change si nécessaire
        npt += 1
    
    x = np.linspace(inf, sup, npt)
    y = fct(x)

    pas = (sup - inf) / (npt - 1)
    # On trouve le pas entre chaque élément de x
    
    integrale = pas / 3 * (y[0] + np.sum(4 * y[1:-1:2]) + np.sum(2 * \
    y[2:-2:2]) + y[-1])
    
    """On calcule l'intégrale à l'aide de la formule I = pas / 3 * \
    (x[0] + 4 * x[1] + 2 * x[2] + ... + 2 * x[-3] + 4 * x[-2] + x[-1])"""
    
    erreur = abs(integrale - integraleExacte)
    
    return integrale, erreur


npt = np.array([1e3, 1e4, 1e5, 1e6], dtype=np.int64)
# On crée une liste qui prend toutes les valeurs de nombre de pas possibles

integraleExacte = 4

"""Par calcul, on trouve que l'intégrale exacte de l'expression étudiée entre
0 et 3 vaut 4"""

inf = 0
sup = 3
# On définit les bornes d'intégration

integraleSimpson = np.array([])
erreurSimpson = np.array([])

"""On crée un ndarray vide integrale et un ndarray erreur auxquels on 
ajoutera les valeurs des intégales calculées au fur et à mesure des boucles 
d'itération""" 

for i in npt:    
    integrale, erreur = intSimpson(fct, inf, sup, i, integraleExacte)
    integraleSimpson = np.append(integraleSimpson, integrale)
    erreurSimpson = np.append(erreurSimpson, erreur)
    # On affecte l'integrale et l'erreur aux ndarrays correspondants

print('La valeur de l\'intégrale et de son erreur associée pour un nombre de \
pas N sont :\n' + str(integraleSimpson) + ' et ' + str(erreurSimpson) + '.')

"""On montre l'intégrale et l'erreur associée à tous les pas et la pente de la
droite dans l'espace log-log de l'erreur par rapport au pas pour chaque 
méthode d'intégration utilisée"""