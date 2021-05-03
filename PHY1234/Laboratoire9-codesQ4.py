# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code vise � d�terminer la position de marcheurs al�atoires apr�s
des nombres de pas d�finis et d'en montrer le graphique. Les marcheurs 
peuvent devenir fixes s'ils sont sur l'axe des y ou s'ils sont 
adjacents � un marcheur fixe."""

import numpy as np

import matplotlib.pyplot as plt

tailleReseau = 256
nMarcheurs = 5000
nIterationsMax = 100000
# On d�finit certains param�tres de base

x = np.random.randint(1, tailleReseau + 1, nMarcheurs)
y = np.random.randint(1, tailleReseau + 1, nMarcheurs)
# On d�finit les positions de d�part des marcheurs

statutMobile = np.ones(nMarcheurs, dtype='bool')
grilleFixe = np.zeros([tailleReseau + 2, tailleReseau + 2], dtype='bool')
# On fait deux tableaux d'�tats, un pour les marcheurs et un pour le terrain

grilleFixe[:, 0] = True
# On fixe des sites collants � y = 0, au bas du reseau

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
    # On fait les tests de direction du pas et on ajoute le d�placement

    x[iMobile] = np.clip(x[iMobile], 1, tailleReseau)
    y[iMobile] = np.clip(y[iMobile], 1, tailleReseau)
    # On s'assure que les marcheurs restent dans le r�seau

    voisinFixe = grilleFixe[x[iMobile] - 1, y[iMobile] - 1] + \
grilleFixe[x[iMobile], y[iMobile] - 1] + grilleFixe[x[iMobile] + 1,
y[iMobile] - 1] + grilleFixe[x[iMobile] + 1, y[iMobile]] + \
grilleFixe[x[iMobile] + 1, y[iMobile] + 1] + grilleFixe[x[iMobile],
y[iMobile] + 1] + grilleFixe[x[iMobile] - 1, y[iMobile] + 1] + \
grilleFixe[x[iMobile] - 1, y[iMobile]]
    # On v�rifie si un voisin est collant

    iFixe = iMobile[voisinFixe.nonzero()[0]]
    # Tableau des indices des nouveaux marcheurs fixes

    if iFixe.size > 0:
        statutMobile[iFixe] = False
        grilleFixe[x[iFixe], y[iFixe]] = True
        
        """On fixe les marcheurs et leur position sur la grille pour ceux qui
        doivent �tre fix�s"""

        nFixes += iFixe.size

    nIterations += 1
    
    print('Iteration {}, nombre de marcheurs fixes {}'.format(nIterations, 
nFixes))

plt.plot(x, y, '.', markersize=2)

plt.xlabel('Position en x')
plt.ylabel('Position en y')
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire9-figureQ4.png')
plt.show()