# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'int�grale d'une certaine fonction selon trois
mani�res diff�rentes, soit la m�thode du trap�ze, la m�thode de Simpson
et la m�thode de Boole, puis trouve la valeur de la pente de la droite 
de r�gression lin�aire qui sera affich�e sur un graphique. Dans ce 
code, la fonction est : 3x / (2 * (x + 1) ** (1 / 2))"""

import numpy as np

def fct1(x):
    """Cette fonction calcule les valeurs de y associ�es � la fonction
    f(x) = 2 * x.
    x : valeurs d'abscisses donn�es � la fonction
    """
    y = 2 * x
    
    return y

def fct2(x):
    """Cette fonction calcule les valeurs de y associ�es � la fonction
    f(x) = 3 * x ** 2.
    x : valeurs d'abscisses donn�es � la fonction
    """
    y = 3 * x ** 2
    
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

    integrale = pas / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * \
np.sum(y[2:-2:2]) + y[-1])

    """On calcule l'int�grale � l'aide de la formule I = pas / 3 * \
    (x[0] + 4 * x[1] + 2 * x[2] + ... + 2 * x[-3] + 4 * x[-2] + x[-1])"""

    erreur = abs(integrale - integraleExacte)

    return integrale, erreur

npt = 25
# On cr�e une liste qui prend toutes les valeurs de nombre de pas possibles

integraleExacte = 1

"""Par calcul, on trouve que l'int�grale exacte des expressions �tudi�es 
valent toutes les deux 1"""

inf = 0
sup = 1
# On d�finit les bornes d'int�gration

integraleTrapeze, erreurTrapeze = intTrapeze(fct1, inf, sup, npt, 
integraleExacte)

integraleSimpson, erreurSimpson = intSimpson(fct2, inf, sup, npt,
integraleExacte)

print('La valeur de l\'int�grale et de son erreur associ�e pour un nombre de \
pas N = 25 sont :\n' + str(integraleTrapeze) + ' et ' + str(erreurTrapeze) + \
' pour la m�thode des trap�zes,\n' + str(integraleSimpson) + ' et ' \
+ str(erreurSimpson) + ' pour la m�thode de Simpson.')