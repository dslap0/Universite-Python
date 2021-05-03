# -*- coding: latin-1 -*-
#@author: Nicolas

import numpy as np
import scipy.constants as cst

import matplotlib.pyplot as plt

# On définit quelques constantes
RAYONSOLAIRE = 7.0e8

# On déclare nos arrays et nos listes utiles pour la suite
etoiles = ["Betelgeuse", "Proxima Centauri", "Rigel", "Soleil", "Sirius B"]
tempEff = np.array([3600, 3000, 12000, 5800, 25000])
rayon = np.array([900, 0.15, 100, 1, 0.0084])
distance = np.array([220, 1.3, 260, 0.00000485])

# On fait un array étalonné pour nos longueurs d'onde possibles
longueurDOnde = np.logspace(-3, 2, num=1000)

# On déclare l'array qui va contenir les valeurs de flux de surface
fluxSurface = np.empty((len(etoiles), len(longueurDOnde)))

# On déclare la liste qui va contenir les flux de surface maximum
iFluxSurfaceMax = np.empty_like(etoiles, dtype=int)

# On ouvre le premier graphique
plt.figure(0)

# On itère sur chaque température et sur chaque longueur d'onde et on place 
# les flux obtenus dans l'array fluxSurface. Après chaque rangée on trouve le 
# maximum et on met le tout en graphique
for i in range(0, len(etoiles)):
    fluxTemporaire = 2 * cst.pi * cst.h * cst.c ** 2 / \
        (longueurDOnde ** 5 * (np.exp(cst.h * cst.c / (longueurDOnde * \
        cst.k * tempEff[i])) - 1))

    fluxSurface[i][:] = fluxTemporaire[:]

    iFluxSurfaceMax[i] = fluxSurface[i].argmax()

    plt.plot(longueurDOnde, fluxSurface[i], label=etoiles[i])
    plt.axvline(longueurDOnde[iFluxSurfaceMax[i]])

plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.savefig("Devoir1AstroFigA.png")
plt.show()

plt.figure(1)

luminosite = 4 * cst.pi * (rayon * RAYONSOLAIRE) ** 2 * \
    cst.Stefan_Boltzmann * tempEff ** 4

iLuminositeMax = luminosite.argmax()

print("L'étoile ayant la plus grande luminosité est " + \
    etoiles[iLuminositeMax] + " avec une luminosité de " + \
    str(luminosite[iLuminositeMax]))

