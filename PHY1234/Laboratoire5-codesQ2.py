# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule l'int�grale d�finie entre 0 et 3 de 
l'expression (3x / (2 * (x + 1) ** (1 / 2))) dx, selon le nombre de 
points de maille sp�cifi� par l'utilisateur, et calcule ensuite 
l'erreur entre cette valeur calcul�e et la v�ritable valeur de 
l'int�grale d�finie. Le programme fait cette op�ration avec la m�thode
des trap�zes, puis pour la m�thode de Romberg � 10 et 25 points de 
maille respectivement."""

import numpy as np 

npt = np.array([10, 25, 40, 60, 100, 160, 250, 400, 600])
# On cr�e une liste qui prend toutes les valeurs de nombre de pas possibles

integraleTrapeze = np.array([])
erreurTrapeze = np.array([])

"""On cr�e les ndarrays vides integrale et erreur auxquels on ajoutera les 
valeurs des int�gales calcul�es au fur et � mesure des boucles d'it�ration""" 

i = 0

# On applique la m�thode des trap�zes
while i < len(npt):
    x = np.linspace(0, 3, npt[i])
    # On cr�e les valeurs de x qui nous servira � calculer l'int�grale
    y = 3 * x / (2 * np.sqrt(x + 1))
    # On calcule les valeurs de y pour la fonction qui nous int�resse
    integraleTrapeze = np.append(integraleTrapeze, 0.5 * np.sum((y[1:] + \
y[:-1]) * (x[1:] - x[:-1])))

    """On calcule l'aire d'un trap�ze rectangle dont la base est dx et les 
    cot�s sont les valeurs de y associ�e � chacun des deux x qui d�limitent 
    dx"""

    erreurTrapeze = np.append(erreurTrapeze, abs(integraleTrapeze[i] - 4))
    
    i += 1

i0 = np.where(npt == 10)
i1 = np.where(npt == 25)
# On trouve i o� npt[i] == 10 et 25

h = 3 / (npt - 1)

integraleRomberg = (h[i1] ** 2 * integraleTrapeze[i0] - h[i0] ** 2 * \
integraleTrapeze[i1]) / (h[i1] ** 2 - h[i0] ** 2)
# On calcule l'int�grale avec la m�thode de Romberg

erreurRomberg = abs(integraleRomberg - 4)

print('La valeur de l\'int�grale et de son erreur associ�e pour un nombre de \
pas de N = 25 sont :\n' + str(integraleRomberg) + ' et ' + \
str(erreurRomberg) + ' avec la m�thode de Romberg\n' + \
str(integraleTrapeze[i1]) + ' et ' + str(erreurTrapeze[i1]) + ' avec la \
m�thode du trap�ze')

"""On montre l'int�grale et l'erreur associ�e � un pas de 10 et 25 pour la 
m�thode de Romberg, puis on compare avec l'int�grale et l'erreur associ�e � un
pas de 25 avec la m�thode des trap�zes uniquement"""