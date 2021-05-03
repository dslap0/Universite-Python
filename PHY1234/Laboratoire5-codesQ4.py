# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'intégrale d'une certaine fonction selon trois
manières différentes, soit la méthode du trapèze, la méthode de Simpson
et la méthode de Boole, puis trouve la valeur de la pente de la droite 
de régression linéaire qui sera affichée sur un graphique. Dans ce 
code, la fonction est : 3x / (2 * (x + 1) ** (1 / 2))"""

import numpy as np

def fct1(x):
    """Cette fonction calcule les valeurs de y associées à la fonction
    f(x) = 2 * x.
    x : valeurs d'abscisses données à la fonction
    """
    y = 2 * x
    
    return y

def fct2(x):
    """Cette fonction calcule les valeurs de y associées à la fonction
    f(x) = 3 * x ** 2.
    x : valeurs d'abscisses données à la fonction
    """
    y = 3 * x ** 2
    
    return y

def intTrapeze(fct, inf, sup, npt, integraleExacte):
    """Cette fonction sert à calculer l'intégrale d'une fonction donnée
    en argument à l'aide de la méthode des trapèzes.
    
    fct : Fonction à intégrée, définie plus tôt
    inf : Borne inférieure de l'intégrale
    sup : Borne supérieure de l'intégrale
    npt : Nombre de pas à intégrer
    integraleExacte : Valeur exacte de l'intégale
    """
    x = np.linspace(inf, sup, npt)
    y = fct(x)

    integrale =  0.5 * np.sum((y[1:] + y[:-1]) * (x[1:] - x[:-1]))

    """On calcule l'aire d'un trapèze rectangle dont la base est dx et les 
    cotés sont les valeurs de y associée à chacun des deux x qui délimitent 
    dx"""

    erreur = abs(integrale - integraleExacte)

    return integrale, erreur

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

    integrale = pas / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * \
np.sum(y[2:-2:2]) + y[-1])

    """On calcule l'intégrale à l'aide de la formule I = pas / 3 * \
    (x[0] + 4 * x[1] + 2 * x[2] + ... + 2 * x[-3] + 4 * x[-2] + x[-1])"""

    erreur = abs(integrale - integraleExacte)

    return integrale, erreur

npt = 25
# On crée une liste qui prend toutes les valeurs de nombre de pas possibles

integraleExacte = 1

"""Par calcul, on trouve que l'intégrale exacte des expressions étudiées 
valent toutes les deux 1"""

inf = 0
sup = 1
# On définit les bornes d'intégration

integraleTrapeze, erreurTrapeze = intTrapeze(fct1, inf, sup, npt, 
integraleExacte)

integraleSimpson, erreurSimpson = intSimpson(fct2, inf, sup, npt,
integraleExacte)

print('La valeur de l\'intégrale et de son erreur associée pour un nombre de \
pas N = 25 sont :\n' + str(integraleTrapeze) + ' et ' + str(erreurTrapeze) + \
' pour la méthode des trapèzes,\n' + str(integraleSimpson) + ' et ' \
+ str(erreurSimpson) + ' pour la méthode de Simpson.')