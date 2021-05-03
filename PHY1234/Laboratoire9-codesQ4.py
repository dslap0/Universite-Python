# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code vise à déterminer la position de marcheurs aléatoires après
des nombres de pas définis et d'en montrer le graphique. Les marcheurs 
peuvent devenir fixes s'ils sont sur l'axe des y ou s'ils sont 
adjacents à un marcheur fixe."""

import numpy as np

import matplotlib.pyplot as plt

tailleReseau = 256
nMarcheurs = 5000
nIterationsMax = 100000
# On définit certains paramètres de base

x = np.random.randint(1, tailleReseau + 1, nMarcheurs)
y = np.random.randint(1, tailleReseau + 1, nMarcheurs)
# On définit les positions de départ des marcheurs

statutMobile = np.ones(nMarcheurs, dtype='bool')
grilleFixe = np.zeros([tailleReseau + 2, tailleReseau + 2], dtype='bool')
# On fait deux tableaux d'états, un pour les marcheurs et un pour le terrain

grilleFixe[:, 0] = True
# On fixe des sites collants à y = 0, au bas du reseau

nFixes = 0
nIterations = 0
# On initialise des compteurs

while (nFixes < nMarcheurs) and (nIterations < nIterationsMax):
    iMobile, = statutMobile.nonzero()
    nMobiles = iMobile.size
    # On trouve l'indice de chaque marcheur mobile et leur nombre

    rdm = np.random.randint(0, 4, nMobiles)
    # On trouve des valeurs pour faire le test de direction du pas

    x[iMobile] = np.where(rdm == 0, x[iMobile] + 1, x[iMobile])
    y[iMobile] = np.where(rdm == 1, y[iMobile] + 1, y[iMobile])
    x[iMobile] = np.where(rdm == 2, x[iMobile] - 1, x[iMobile])
    y[iMobile] = np.where(rdm == 3, y[iMobile] - 1, y[iMobile])
    # On fait les tests de direction du pas et on ajoute le déplacement

    x[iMobile] = np.clip(x[iMobile], 1, tailleReseau)
    y[iMobile] = np.clip(y[iMobile], 1, tailleReseau)
    # On s'assure que les marcheurs restent dans le réseau

    voisinFixe = grilleFixe[x[iMobile] - 1, y[iMobile] - 1] + \
grilleFixe[x[iMobile], y[iMobile] - 1] + grilleFixe[x[iMobile] + 1,
y[iMobile] - 1] + grilleFixe[x[iMobile] + 1, y[iMobile]] + \
grilleFixe[x[iMobile] + 1, y[iMobile] + 1] + grilleFixe[x[iMobile],
y[iMobile] + 1] + grilleFixe[x[iMobile] - 1, y[iMobile] + 1] + \
grilleFixe[x[iMobile] - 1, y[iMobile]]
    # On vérifie si un voisin est collant

    iFixe = iMobile[voisinFixe.nonzero()[0]]
    # Tableau des indices des nouveaux marcheurs fixes

    if iFixe.size > 0:
        statutMobile[iFixe] = False
        grilleFixe[x[iFixe], y[iFixe]] = True
        
        """On fixe les marcheurs et leur position sur la grille pour ceux qui
        doivent être fixés"""

        nFixes += iFixe.size

    nIterations += 1
    
    print('Iteration {}, nombre de marcheurs fixes {}'.format(nIterations, 
nFixes))

plt.plot(x, y, '.', markersize=2)

plt.xlabel('Position en x')
plt.ylabel('Position en y')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire9-figureQ4.png')
plt.show()