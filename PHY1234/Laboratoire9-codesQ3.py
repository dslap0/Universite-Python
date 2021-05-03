# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code vise à déterminer la position de marcheurs aléatoires après
des nombres de pas définis et de montrer le déplacement moyen en x 
selon le nombre d'itérations déjà faits."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 1000
nPas = 1001
# On définit des paramètres initiaux

x = np.zeros([nMarcheurs, nPas], dtype=int)
y = np.zeros([nMarcheurs, nPas], dtype=int)
# On définit les positions initiales de chaque marcheur

nPasEcoules = np.zeros(nPas, dtype=int)

for k in range(1, nPas):
    # On fait le même calcul pour chaque pas
    rdm = np.random.randint(0, 4, nMarcheurs)
    # On trouve des valeurs pour faire le test de direction du pas

    x[0:, k] = np.where(rdm == 0, x[0:, k - 1] + 1, x[0:, k - 1])
    y[0:, k] = np.where(rdm == 1, y[0:, k - 1] + 1, y[0:, k - 1])
    x[0:, k] = np.where(rdm == 2, x[0:, k] - 1, x[0:, k])
    y[0:, k] = np.where(rdm == 3, y[0:, k] - 1, y[0:, k])
    # On fait les tests de direction du pas et on ajoute le déplacement 

    nPasEcoules[k] = k - 1

xMoy = np.mean(x, axis=0)

plt.plot(nPasEcoules, xMoy, '-')

plt.xlabel('Nombre de pas écoulés')
plt.ylabel('Déplacement moyen en x')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ3.png')
plt.show()