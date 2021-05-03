# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code vise à déterminer la position de marcheurs aléatoires après
des nombres de pas définis et d'en montrer le graphique."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 1000
nPas = 1001
# On définit des paramètres initiaux

x = np.zeros([nMarcheurs, nPas])
y = np.zeros([nMarcheurs, nPas])
# On définit les positions initiales de chaque marcheur

for k in range(1, nPas):
    # On fait le même calcul pour chaque pas
    rdm = np.random.randint(0, 4, nMarcheurs)
    # On trouve des valeurs pour faire le test de direction du pas

    x[0:, k] = np.where(rdm == 0, x[0:, k - 1] + 1, x[0:, k - 1])
    y[0:, k] = np.where(rdm == 1, y[0:, k - 1] + 1, y[0:, k - 1])
    x[0:, k] = np.where(rdm == 2, x[0:, k] - 1, x[0:, k])
    y[0:, k] = np.where(rdm == 3, y[0:, k] - 1, y[0:, k])
    # On fait les test de direction du pas et le déplacement qui en découle

deplacement = x ** 2 + y ** 2

plt.plot(x[0:, 1000], y[0:, 1000], '.')
plt.plot(x[0:, 300], y[0:, 300], '.')
plt.plot(x[0:, 100], y[0:, 100], '.')
plt.plot(x[0:, 30], y[0:, 30], '.')
plt.plot(x[0:, 10], y[0:, 10], '.')
# On montre la position des marcheurs après certains pas

plt.xlabel('Position en x')
plt.ylabel('Position en y')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ1.png')
plt.show()