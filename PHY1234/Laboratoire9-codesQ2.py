# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code vise � d�terminer la position de marcheurs al�atoires apr�s
des nombres de pas d�finis et de montrer le d�placement quadratique 
moyen selon le nombre d'it�rations d�j� faits."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 1000
nPas = 1001
# On d�finit des param�tres initiaux

x = np.zeros([nMarcheurs, nPas], dtype=int)
y = np.zeros([nMarcheurs, nPas], dtype=int)
# On d�finit les positions initiales de chaque marcheur

nPasEcoules = np.ones(nPas, dtype=int)

for k in range(1, nPas):
    # On fait le m�me calcul pour chaque pas
    rdm = np.random.randint(0, 4, nMarcheurs)
    # On trouve des valeurs pour faire le test de direction du pas

    x[0:, k] = np.where(rdm == 0, x[0:, k - 1] + 1, x[0:, k - 1])
    y[0:, k] = np.where(rdm == 1, y[0:, k - 1] + 1, y[0:, k - 1])
    x[0:, k] = np.where(rdm == 2, x[0:, k] - 1, x[0:, k])
    y[0:, k] = np.where(rdm == 3, y[0:, k] - 1, y[0:, k])
    # On fait les tests de direction du pas et on ajoute le d�placement 

    nPasEcoules[k] = nPasEcoules[k - 1] + 1

deplacement = x ** 2 + y ** 2

deplacementMoy = np.mean(deplacement, axis=0)

plt.plot(nPasEcoules, deplacementMoy, '-')

plt.xlabel('Nombre de pas �coul�s')
plt.ylabel('D�placement quadratique moyen')
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire9-figureQ2.png')
plt.show()