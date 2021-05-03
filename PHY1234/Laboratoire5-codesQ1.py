# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'int�grale d�finie entre 0 et 3 de 
l'expression (3x / (2 * (x + 1) ** (1 / 2))) dx, selon le nombre de 
points de maille sp�cifi� par l'utilisateur, et calcule ensuite 
l'erreur entre cette valeur calcul�e et la v�ritable valeur de 
l'int�grale d�finie. Le programme trace ensuite le graphique de
l'erreur par rapport au pas de maille sp�cifi� et trace ensuite la 
droite de r�gression lin�aire pour ce graphique."""

import numpy as np 

import matplotlib.pyplot as plt

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
    
    """On calcule la valeur de l'ordonn�e � l'origine de la droite 
    de r�gression"""

    return m, b

npt = np.array([25, 40, 60, 100, 160, 250, 400, 600])
# On cr�e une liste qui prend toutes les valeurs de nombre de pas possibles

integrale = np.array([])
erreur = np.array([])

"""On cr�e les ndarrays vides integrale et erreur auxquels on ajoutera les 
valeurs des int�gales calcul�es au fur et � mesure des boucles d'it�ration""" 

i = 0

# On applique la m�thode des trap�zes
while i < len(npt):
    x = np.linspace(0, 3, npt[i])
    # On cr�e les valeurs de x qui nous servira � calculer l'int�grale
    y = 3 * x / (2 * np.sqrt(x + 1))
    # On calcule les valeurs de y pour la fonction qui nous int�resse
    integrale = np.append(integrale, 0.5 * np.sum((y[1:] + y[:-1]) * \
(x[1:] - x[:-1])))

    """On calcule l'aire d'un trap�ze rectangle dont la base est dx et les 
    cot�s sont les valeurs de y associ�e � chacun des deux x qui d�limitent 
    dx"""

    erreur = np.append(erreur, abs(integrale[i] - 4))
    
    i += 1

h = 3 / (npt - 1)

# On trace la droite de r�gression lin�aire
m, b = regressionLineaireLog(h, erreur)
# On trouve la pente et l'ordonn�e � l'origine de la droite de r�gression

epsilon = np.exp(m * np.log(h) + b)

"""On trouve le ndarray de epsilon qui nous servirons � tracer une 
r�gression lin�aire sur le graphique logarithmique"""

plt.plot(h, erreur, 'ro')
plt.plot(h, epsilon, '-')

plt.xscale('log')
plt.gca().invert_xaxis()
plt.yscale('log')
plt.xlabel('Largeur de pas de l\'int�grale (log)')
plt.ylabel('Erreur sur l\'int�grale (log)')
# On ajuste les param�tres de pr�sentation du graphique

i = np.where(npt == 40)
# On trouve i o� npt[i] == 40

print('La pente de la droite dans l\'espace log-log de l\'erreur par rapport \
au pas est de :\n'+ str(m) + '\n\nLa valeur de l\'int�grale et de son erreur \
associ�e pour un nombre de pas N = 40 sont :\n' + str(integrale[i]) + \
' et ' + str(erreur[i]))

"""On montre l'int�grale et l'erreur associ�e � un pas de 40 et la pente de la
droite dans l'espace log-log de l'erreur par rapport au pas"""

plt.savefig('Laboratoire5-figureQ1.png')
plt.show()