# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'int�grale d'une certaine fonction selon trois
mani�res diff�rentes, soit la m�thode du trap�ze, la m�thode de Simpson
et la m�thode de Boole, puis trouve la valeur de la pente de la droite 
de r�gression lin�aire qui sera affich�e sur un graphique. Dans ce 
code, la fonction est : 3x / (2 * (x + 1) ** (1 / 2))"""

import numpy as np

import matplotlib.pyplot as plt


def fct(x):
    """Cette fonction calcule les valeurs de y associ�es � la fonction
    f(x) = 3 * x / 2 * (x + 1) ** (1 / 2).
    x : valeurs d'abscisses donn�es � la fonction
    """
    y = 3 * x / (2 * np.sqrt(x + 1))
    
    return y

def intTrapeze(fct, inf, sup, npt, integraleExacte):
    """Cette fonction sert � calculer l'int�grale d'une fonction donn�e
    en argument � l'aide de la m�thode des trap�zes.
    
    fct : Fonction � int�gr�e, d�finie plus t�t
    inf : Borne inf�rieure de l'int�grale
    sup : Borne sup�rieure de l'int�grale
    npt : Nombre de pas � int�grer
    integraleExacte : Valeur exacte de l'int�gale
    """
    x = np.linspace(inf, sup, npt)
    y = fct(x)
    
    integrale =  0.5 * np.sum((y[1:] + y[:-1]) * (x[1:] - x[:-1]))
    
    """On calcule l'aire d'un trap�ze rectangle dont la base est dx et les 
    cot�s sont les valeurs de y associ�e � chacun des deux x qui d�limitent 
    dx"""
    
    erreur = abs(integrale - integraleExacte)
    
    return integrale, erreur

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

def intBoole(fct, inf, sup, npt, integraleExacte):
    """Cette fonction sert � calculer l'int�grale de la fonction donn�e
    en argument avec la m�thode de Boole, en s'assurant que le nombre
    de pas soit conforme.
    
    fct : Fonction � int�gr�e, d�finie plus t�t
    inf : Borne inf�rieure de l'int�grale
    sup : Borne sup�rieure de l'int�grale
    npt : Nombre d'�l�ments � int�grer
    integraleExacte : Valeur exacte de l'int�gale
    """
    if npt % 4 == 0:
        npt += 1
    elif npt % 4 == 2:
        npt += 3
    elif npt % 4 == 3:
        npt += 2
    # On s'est assur� de travailler avec une valeur de npt valide
    
    x = np.linspace(inf, sup, npt)
    y = fct(x)
    
    pas = (sup - inf) / (npt - 1)
    # On trouve le pas entre chaque �l�ment de x
    
    integrale = 2 * pas / 45 * (7 * y[0] + np.sum(32 * y[1:-1:2]) + \
np.sum(12 * y[2:-2:4]) + np.sum(14 * y[4:-4:4]) + 7 * y[-1])
    
    """On calcule l'int�grale � l'aide de la formule I = 2 * pas / 45 * \
    (7 * x[0] + 32 * x[1] + 12 * x[2] + 32 * x[3] + 14 * x[4] + ...\
    + 14 * x[-5] + 32 * x[-4] + 12 * x[-3] + 32 * x[-2] + 7 * x[-1])"""
    
    erreur = abs(integrale - integraleExacte)
    
    return integrale, erreur

def regressionLineaireLog(x, y):
    """Fonction qui calcule la r�gression lin�aire de la fonction 
    donn�e en argument avec la m�thode des moindres carr�s (en prenant
    en compte une fonction sur un graphique logarithmique).

    x : correspond aux valeurs d'abscisses de la fonction.
    y : Ndarray prenant l'ensemble des valeurs de y associ�es �
    un certain pas.
    """
    x = np.log(x)
    y = np.log(y)
    # On d�finit les x et y d'une pente logarithmique
    
    N = 1 / len(x)
    m = (N * np.sum(y * x) - N ** 2 * np.sum(y) * np.sum(x)) / \
    (N * np.sum(x ** 2) - (N * np.sum(x)) ** 2)
    # On calcule la valeur de la pente de la droite de r�gression lin�aire
    
    b = N * np.sum(y) - m * N * np.sum(x)
    
    """On calcule la valeur de l'ordonn�e � l'origine de la droite de 
    r�gression"""

    return m, b


npt = np.array([25, 40, 60, 100, 160, 250, 400, 600])
# On cr�e une liste qui prend toutes les valeurs de nombre de pas possibles

integraleExacte = 4

"""Par calcul, on trouve que l'int�grale exacte de l'expression �tudi�e entre
0 et 3 vaut 4"""

inf = 0
sup = 3
# On d�finit les bornes d'int�gration

integraleTrapeze = np.array([])
erreurTrapeze = np.array([])
integraleSimpson = np.array([])
erreurSimpson = np.array([])
integraleBoole = np.array([])
erreurBoole = np.array([])

"""On cr�e des ndarrays vides integrales et erreurs correspondant auxquels on 
ajoutera les valeurs des int�gales calcul�es au fur et � mesure des boucles 
d'it�ration""" 

for i in npt:
    integrale, erreur = intTrapeze(fct, inf, sup, i, integraleExacte)
    
    integraleTrapeze = np.append(integraleTrapeze, integrale)
    erreurTrapeze = np.append(erreurTrapeze, erreur)
    # On affecte l'integrale et l'erreur � leurs ndarrays correspondants
    
    integrale, erreur = intSimpson(fct, inf, sup, i, integraleExacte)
    
    integraleSimpson = np.append(integraleSimpson, integrale)
    erreurSimpson = np.append(erreurSimpson, erreur)
    # On affecte l'integrale et l'erreur � leurs ndarrays correspondants
    
    integrale, erreur = intBoole(fct, inf, sup, i, integraleExacte)
    
    integraleBoole = np.append(integraleBoole, integrale)
    erreurBoole = np.append(erreurBoole, erreur)
    # On affecte l'integrale et l'erreur � leurs ndarrays correspondants

h = (sup - inf) / (npt - 1)

mTrapeze, bTrapeze = regressionLineaireLog(h, erreurTrapeze)
mSimpson, bSimpson = regressionLineaireLog(h, erreurSimpson)
mBoole, bBoole = regressionLineaireLog(h, erreurBoole)

"""On trouve la pente et l'ordonn�e � l'origine de la droite de r�gression en
fonction de chaque m�thode d'int�gration utilis�e"""

epsilonTrapeze = np.exp(mTrapeze * np.log(h) + bTrapeze)
epsilonSimpson = np.exp(mSimpson * np.log(h) + bSimpson)
epsilonBoole = np.exp(mBoole * np.log(h) + bBoole)
# On trouve la valeur de la pente de la droite de r�gression lin�aire

i = np.where(npt == 100)
# On trouve i o� npt[i] == 100

print('(� noter que les r�sultats sont pr�sent�s sous la forme : m�thode du \
trap�ze,\nm�thode de Simpson puis m�thode de Boole). La pente de la droite \
dans l\'espace\nlog-log de l\'erreur par rapport au pas est de :\n' + \
str(mTrapeze) + ', ' + str(mSimpson) + ', ' + str(mBoole) + '\n\nLa valeur \
de l\'int�grale et de son erreur associ�e pour un nombre de pas N = 100 \
sont :\n' + str(integraleTrapeze[i]) + ' et ' + str(erreurTrapeze[i]) + \
',\n' + str(integraleSimpson[i]) + ' et ' + str(erreurSimpson[i]) + ',\n' + \
str(integraleBoole[i]) + ' et ' + str(erreurBoole[i]) + '.')

"""On montre l'int�grale et l'erreur associ�e � un pas de 40 et la pente de la
droite dans l'espace log-log de l'erreur par rapport au pas pour chaque 
m�thode d'int�gration utilis�e"""

plt.plot(h, erreurTrapeze, 'ro')
plt.plot(h, erreurSimpson,'b*')
plt.plot(h, erreurBoole, 'g+')

"""On affiche les erreurs des int�grales selon chaque m�thode selon le nombre
de pas pour chaque m�thode d'int�gration"""

plt.plot(h, epsilonTrapeze, 'r-')
plt.plot(h, epsilonSimpson, 'b-')
plt.plot(h, epsilonBoole, 'g-')

"""On affiche les droites de r�gression lin�aire de l'erreur sur l'int�grale 
selon chaque m�thode d'int�gration par rapport au nombre de pas pris en
compte"""

plt.xscale('log')
plt.gca().invert_xaxis()
plt.yscale('log')
plt.xlabel('Longueur du pas d\'int�gration (log)')
plt.ylabel('Erreur sur l\'int�grale (log)')
# On ajuste les param�tres de pr�sentation du graphique

plt.savefig('Laboratoire5-figureQ3.png')
plt.show()