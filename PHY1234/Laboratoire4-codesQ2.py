# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trace la courbe produite par un projectile à partir
d'un fichier contenant les informations sur la position du projectile à
chaque instant."""

import numpy as np

import matplotlib.pyplot as plt

t = []
x = []
y = []
# On crée les trois listes vides t, x et y

fichier = open('Trajectoire du projectile.txt', 'r')
for ligne in fichier:
    if not ligne.startswith('#'):
        # On ne prend en compte que les lignes qui ne commencent pas par #
        tempsPosition = fichier.read().replace('\n', '').split(' ')
        # On sépare chaque élément dans une grande liste nommée tempsPosition
fichier.close()

tempsPosition = list(filter(None, tempsPosition))

element = 0
while element != len(tempsPosition):
    """On crée une boucle qui met les éléments dans 3 listes différentes 
    (t, x ou y) selon leur position dans la liste tempsPosition"""
    if element % 3 == 0:
        t.append(float(tempsPosition[element]))
    elif element % 3 == 1:
        x.append(tempsPosition[element])
    elif element % 3 == 2:
        y.append(tempsPosition[element])
    element += 1

t = np.array(t, dtype=np.float32)
x = np.array(x, dtype=np.float32)
y = np.array(y, dtype=np.float32)
# On transforme les listes en ndarray

element = 0
while element < len(x):
    """On crée une boucle while qui n'applique que le marqueur losange à
    chaque 10 éléments de la liste"""
    plt.plot(x[element], y[element], marker='D', color='b')
    element += 10

plt.plot(x, y, color='b')
# On trace la courbe voulue

plt.axis('scaled')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
# On effectue les modifications de mise en forme de la figure

plt.savefig('Laboratoire4-figureQ2.png')
plt.show()