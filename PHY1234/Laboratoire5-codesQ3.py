# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'intégrale d'une certaine fonction selon trois
manières différentes, soit la méthode du trapèze, la méthode de Simpson
et la méthode de Boole, puis trouve la valeur de la pente de la droite 
de régression linéaire qui sera affichée sur un graphique. Dans ce 
code, la fonction est : 3x / (2 * (x + 1) ** (1 / 2))"""

import numpy as np

import matplotlib.pyplot as plt


def fct(x):
    """Cette fonction calcule les valeurs de y associées à la fonction
    f(x) = 3 * x / 2 * (x + 1) ** (1 / 2).
    x : valeurs d'abscisses données à la fonction
    """
    y = 3 * x / (2 * np.sqrt(x + 1))
    
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
    
    integrale = pas / 3 * (y[0] + np.sum(4 * y[1:-1:2]) + np.sum(2 * \
    y[2:-2:2]) + y[-1])
    
    """On calcule l'intégrale à l'aide de la formule I = pas / 3 * \
    (x[0] + 4 * x[1] + 2 * x[2] + ... + 2 * x[-3] + 4 * x[-2] + x[-1])"""
    
    erreur = abs(integrale - integraleExacte)
    
    return integrale, erreur

def intBoole(fct, inf, sup, npt, integraleExacte):
    """Cette fonction sert à calculer l'intégrale de la fonction donnée
    en argument avec la méthode de Boole, en s'assurant que le nombre
    de pas soit conforme.
    
    fct : Fonction à intégrée, définie plus tôt
    inf : Borne inférieure de l'intégrale
    sup : Borne supérieure de l'intégrale
    npt : Nombre d'éléments à intégrer
    integraleExacte : Valeur exacte de l'intégale
    """
    if npt % 4 == 0:
        npt += 1
    elif npt % 4 == 2:
        npt += 3
    elif npt % 4 == 3:
        npt += 2
    # On s'est assuré de travailler avec une valeur de npt valide
    
    x = np.linspace(inf, sup, npt)
    y = fct(x)
    
    pas = (sup - inf) / (npt - 1)
    # On trouve le pas entre chaque élément de x
    
    integrale = 2 * pas / 45 * (7 * y[0] + np.sum(32 * y[1:-1:2]) + \
np.sum(12 * y[2:-2:4]) + np.sum(14 * y[4:-4:4]) + 7 * y[-1])
    
    """On calcule l'intégrale à l'aide de la formule I = 2 * pas / 45 * \
    (7 * x[0] + 32 * x[1] + 12 * x[2] + 32 * x[3] + 14 * x[4] + ...\
    + 14 * x[-5] + 32 * x[-4] + 12 * x[-3] + 32 * x[-2] + 7 * x[-1])"""
    
    erreur = abs(integrale - integraleExacte)
    
    return integrale, erreur

def regressionLineaireLog(x, y):
    """Fonction qui calcule la régression linéaire de la fonction 
    donnée en argument avec la méthode des moindres carrés (en prenant
    en compte une fonction sur un graphique logarithmique).

    x : correspond aux valeurs d'abscisses de la fonction.
    y : Ndarray prenant l'ensemble des valeurs de y associées à
    un certain pas.
    """
    x = np.log(x)
    y = np.log(y)
    # On définit les x et y d'une pente logarithmique
    
    N = 1 / len(x)
    m = (N * np.sum(y * x) - N ** 2 * np.sum(y) * np.sum(x)) / \
    (N * np.sum(x ** 2) - (N * np.sum(x)) ** 2)
    # On calcule la valeur de la pente de la droite de régression linéaire
    
    b = N * np.sum(y) - m * N * np.sum(x)
    
    """On calcule la valeur de l'ordonnée à l'origine de la droite de 
    régression"""

    return m, b


npt = np.array([25, 40, 60, 100, 160, 250, 400, 600])
# On crée une liste qui prend toutes les valeurs de nombre de pas possibles

integraleExacte = 4

"""Par calcul, on trouve que l'intégrale exacte de l'expression étudiée entre
0 et 3 vaut 4"""

inf = 0
sup = 3
# On définit les bornes d'intégration

integraleTrapeze = np.array([])
erreurTrapeze = np.array([])
integraleSimpson = np.array([])
erreurSimpson = np.array([])
integraleBoole = np.array([])
erreurBoole = np.array([])

"""On crée des ndarrays vides integrales et erreurs correspondant auxquels on 
ajoutera les valeurs des intégales calculées au fur et à mesure des boucles 
d'itération""" 

for i in npt:
    integrale, erreur = intTrapeze(fct, inf, sup, i, integraleExacte)
    
    integraleTrapeze = np.append(integraleTrapeze, integrale)
    erreurTrapeze = np.append(erreurTrapeze, erreur)
    # On affecte l'integrale et l'erreur à leurs ndarrays correspondants
    
    integrale, erreur = intSimpson(fct, inf, sup, i, integraleExacte)
    
    integraleSimpson = np.append(integraleSimpson, integrale)
    erreurSimpson = np.append(erreurSimpson, erreur)
    # On affecte l'integrale et l'erreur à leurs ndarrays correspondants
    
    integrale, erreur = intBoole(fct, inf, sup, i, integraleExacte)
    
    integraleBoole = np.append(integraleBoole, integrale)
    erreurBoole = np.append(erreurBoole, erreur)
    # On affecte l'integrale et l'erreur à leurs ndarrays correspondants

h = (sup - inf) / (npt - 1)

mTrapeze, bTrapeze = regressionLineaireLog(h, erreurTrapeze)
mSimpson, bSimpson = regressionLineaireLog(h, erreurSimpson)
mBoole, bBoole = regressionLineaireLog(h, erreurBoole)

"""On trouve la pente et l'ordonnée à l'origine de la droite de régression en
fonction de chaque méthode d'intégration utilisée"""

epsilonTrapeze = np.exp(mTrapeze * np.log(h) + bTrapeze)
epsilonSimpson = np.exp(mSimpson * np.log(h) + bSimpson)
epsilonBoole = np.exp(mBoole * np.log(h) + bBoole)
# On trouve la valeur de la pente de la droite de régression linéaire

i = np.where(npt == 100)
# On trouve i où npt[i] == 100

print('(À noter que les résultats sont présentés sous la forme : méthode du \
trapèze,\nméthode de Simpson puis méthode de Boole). La pente de la droite \
dans l\'espace\nlog-log de l\'erreur par rapport au pas est de :\n' + \
str(mTrapeze) + ', ' + str(mSimpson) + ', ' + str(mBoole) + '\n\nLa valeur \
de l\'intégrale et de son erreur associée pour un nombre de pas N = 100 \
sont :\n' + str(integraleTrapeze[i]) + ' et ' + str(erreurTrapeze[i]) + \
',\n' + str(integraleSimpson[i]) + ' et ' + str(erreurSimpson[i]) + ',\n' + \
str(integraleBoole[i]) + ' et ' + str(erreurBoole[i]) + '.')

"""On montre l'intégrale et l'erreur associée à un pas de 40 et la pente de la
droite dans l'espace log-log de l'erreur par rapport au pas pour chaque 
méthode d'intégration utilisée"""

plt.plot(h, erreurTrapeze, 'ro')
plt.plot(h, erreurSimpson,'b*')
plt.plot(h, erreurBoole, 'g+')

"""On affiche les erreurs des intégrales selon chaque méthode selon le nombre
de pas pour chaque méthode d'intégration"""

plt.plot(h, epsilonTrapeze, 'r-')
plt.plot(h, epsilonSimpson, 'b-')
plt.plot(h, epsilonBoole, 'g-')

"""On affiche les droites de régression linéaire de l'erreur sur l'intégrale 
selon chaque méthode d'intégration par rapport au nombre de pas pris en
compte"""

plt.xscale('log')
plt.gca().invert_xaxis()
plt.yscale('log')
plt.xlabel('Longueur du pas d\'intégration (log)')
plt.ylabel('Erreur sur l\'intégrale (log)')
# On ajuste les paramètres de présentation du graphique

plt.savefig('Laboratoire5-figureQ3.png')
plt.show()