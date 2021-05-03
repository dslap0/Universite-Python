# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'intégrale définie entre 0 et 3 de 
l'expression (3x / (2 * (x + 1) ** (1 / 2))) dx, selon le nombre de 
points de maille spécifié par l'utilisateur, et calcule ensuite 
l'erreur entre cette valeur calculée et la véritable valeur de 
l'intégrale définie. Le programme trace ensuite le graphique de
l'erreur par rapport au pas de maille spécifié et trace ensuite la 
droite de régression linéaire pour ce graphique."""

import numpy as np 

import matplotlib.pyplot as plt

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
    
    """On calcule la valeur de l'ordonnée à l'origine de la droite 
    de régression"""

    return m, b

npt = np.array([25, 40, 60, 100, 160, 250, 400, 600])
# On crée une liste qui prend toutes les valeurs de nombre de pas possibles

integrale = np.array([])
erreur = np.array([])

"""On crée les ndarrays vides integrale et erreur auxquels on ajoutera les 
valeurs des intégales calculées au fur et à mesure des boucles d'itération""" 

i = 0

# On applique la méthode des trapèzes
while i < len(npt):
    x = np.linspace(0, 3, npt[i])
    # On crée les valeurs de x qui nous servira à calculer l'intégrale
    y = 3 * x / (2 * np.sqrt(x + 1))
    # On calcule les valeurs de y pour la fonction qui nous intéresse
    integrale = np.append(integrale, 0.5 * np.sum((y[1:] + y[:-1]) * \
(x[1:] - x[:-1])))

    """On calcule l'aire d'un trapèze rectangle dont la base est dx et les 
    cotés sont les valeurs de y associée à chacun des deux x qui délimitent 
    dx"""

    erreur = np.append(erreur, abs(integrale[i] - 4))
    
    i += 1

h = 3 / (npt - 1)

# On trace la droite de régression linéaire
m, b = regressionLineaireLog(h, erreur)
# On trouve la pente et l'ordonnée à l'origine de la droite de régression

epsilon = np.exp(m * np.log(h) + b)

"""On trouve le ndarray de epsilon qui nous servirons à tracer une 
régression linéaire sur le graphique logarithmique"""

plt.plot(h, erreur, 'ro')
plt.plot(h, epsilon, '-')

plt.xscale('log')
plt.gca().invert_xaxis()
plt.yscale('log')
plt.xlabel('Largeur de pas de l\'intégrale (log)')
plt.ylabel('Erreur sur l\'intégrale (log)')
# On ajuste les paramètres de présentation du graphique

i = np.where(npt == 40)
# On trouve i où npt[i] == 40

print('La pente de la droite dans l\'espace log-log de l\'erreur par rapport \
au pas est de :\n'+ str(m) + '\n\nLa valeur de l\'intégrale et de son erreur \
associée pour un nombre de pas N = 40 sont :\n' + str(integrale[i]) + \
' et ' + str(erreur[i]))

"""On montre l'intégrale et l'erreur associée à un pas de 40 et la pente de la
droite dans l'espace log-log de l'erreur par rapport au pas"""

plt.savefig('Laboratoire5-figureQ1.png')
plt.show()