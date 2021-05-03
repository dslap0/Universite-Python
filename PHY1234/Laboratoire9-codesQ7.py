# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code vise à déterminer la position de marcheurs aléatoires après
des nombres de pas définis et d'en montrer le graphique."""

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

nMarcheurs = 1000
nPas = 1001
# On définit des paramètres initiaux

x = np.zeros([nMarcheurs, nPas])
y = np.zeros([nMarcheurs, nPas])
z = np.zeros([nMarcheurs, nPas])
# On définit les positions initiales de chaque marcheur


for k in range(1, nPas):
    # On fait le même calcul pour chaque pas

    rdm = np.random.randint(0, 6, nMarcheurs)
    # On trouve des valeurs pour faire le test de direction du pas

    x[:, k] = np.where(rdm == 0, x[:, k - 1] + 1, x[:, k - 1])
    y[:, k] = np.where(rdm == 1, y[:, k - 1] + 1, y[:, k - 1])
    z[:, k] = np.where(rdm == 2, z[:, k - 1] + 1, z[:, k - 1])
    x[:, k] = np.where(rdm == 3, x[:, k] - 1, x[:, k])
    y[:, k] = np.where(rdm == 4, y[:, k] - 1, y[:, k])
    z[:, k] = np.where(rdm == 5, z[:, k] - 1, z[:, k])
    # On fait les test de direction du pas et le déplacement qui en découle

deplacement = x ** 2 + y ** 2

fig = plt.figure(0)
ax = Axes3D(fig)
ax.scatter(x[:, 1000], y[:, 1000], z[:, 1000])
ax.scatter(x[:, 300], y[:, 300], z[:, 300])
ax.scatter(x[:, 100], y[:, 100], z[:, 100])
ax.scatter(x[:, 30], y[:, 30], z[:, 30])
ax.scatter(x[:, 10], y[:, 10], z[:, 10])
# On montre la position des marcheurs après certains pas

ax.set_xlabel('Position en x')
ax.set_ylabel('Position en y')
ax.set_zlabel('Position en z')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ7.png')

fig = plt.figure(1)
ax = Axes3D(fig)
ax.scatter(x[:, 10], y[:, 10], z[:, 10], color='tab:purple')

ax.set_xlabel('Position en x')
ax.set_ylabel('Position en y')
ax.set_zlabel('Position en z')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ7-1.png')

fig = plt.figure(2)
ax = Axes3D(fig)
ax.scatter(x[:, 30], y[:, 30], z[:, 30], color='tab:red')

ax.set_xlabel('Position en x')
ax.set_ylabel('Position en y')
ax.set_zlabel('Position en z')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ7-2.png')

fig = plt.figure(3)
ax = Axes3D(fig)
ax.scatter(x[:, 100], y[:, 100], z[:, 100], color='tab:green')

ax.set_xlabel('Position en x')
ax.set_ylabel('Position en y')
ax.set_zlabel('Position en z')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ7-3.png')

fig = plt.figure(4)
ax = Axes3D(fig)
ax.scatter(x[:, 300], y[:, 300], z[:, 300], color='tab:orange')

ax.set_xlabel('Position en x')
ax.set_ylabel('Position en y')
ax.set_zlabel('Position en z')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ7-4.png')

fig = plt.figure(5)
ax = Axes3D(fig)
ax.scatter(x[:, 1000], y[:, 1000], z[:, 1000], color='tab:blue')

ax.set_xlabel('Position en x')
ax.set_ylabel('Position en y')
ax.set_zlabel('Position en z')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ7-5.png')

plt.show()