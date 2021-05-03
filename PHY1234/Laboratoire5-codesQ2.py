# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'intégrale définie entre 0 et 3 de 
l'expression (3x / (2 * (x + 1) ** (1 / 2))) dx, selon le nombre de 
points de maille spécifié par l'utilisateur, et calcule ensuite 
l'erreur entre cette valeur calculée et la véritable valeur de 
l'intégrale définie. Le programme fait cette opération avec la méthode
des trapèzes, puis pour la méthode de Romberg à 10 et 25 points de 
maille respectivement."""

import numpy as np 

npt = np.array([10, 25, 40, 60, 100, 160, 250, 400, 600])
# On crée une liste qui prend toutes les valeurs de nombre de pas possibles

integraleTrapeze = np.array([])
erreurTrapeze = np.array([])

"""On crée les ndarrays vides integrale et erreur auxquels on ajoutera les 
valeurs des intégales calculées au fur et à mesure des boucles d'itération""" 

i = 0

# On applique la méthode des trapèzes
while i < len(npt):
    x = np.linspace(0, 3, npt[i])
    # On crée les valeurs de x qui nous servira à calculer l'intégrale
    y = 3 * x / (2 * np.sqrt(x + 1))
    # On calcule les valeurs de y pour la fonction qui nous intéresse
    integraleTrapeze = np.append(integraleTrapeze, 0.5 * np.sum((y[1:] + \
y[:-1]) * (x[1:] - x[:-1])))

    """On calcule l'aire d'un trapèze rectangle dont la base est dx et les 
    cotés sont les valeurs de y associée à chacun des deux x qui délimitent 
    dx"""

    erreurTrapeze = np.append(erreurTrapeze, abs(integraleTrapeze[i] - 4))
    
    i += 1

i0 = np.where(npt == 10)
i1 = np.where(npt == 25)
# On trouve i où npt[i] == 10 et 25

h = 3 / (npt - 1)

integraleRomberg = (h[i1] ** 2 * integraleTrapeze[i0] - h[i0] ** 2 * \
integraleTrapeze[i1]) / (h[i1] ** 2 - h[i0] ** 2)
# On calcule l'intégrale avec la méthode de Romberg

erreurRomberg = abs(integraleRomberg - 4)

print('La valeur de l\'intégrale et de son erreur associée pour un nombre de \
pas de N = 25 sont :\n' + str(integraleRomberg) + ' et ' + \
str(erreurRomberg) + ' avec la méthode de Romberg\n' + \
str(integraleTrapeze[i1]) + ' et ' + str(erreurTrapeze[i1]) + ' avec la \
méthode du trapèze')

"""On montre l'intégrale et l'erreur associée à un pas de 10 et 25 pour la 
méthode de Romberg, puis on compare avec l'intégrale et l'erreur associée à un
pas de 25 avec la méthode des trapèzes uniquement"""