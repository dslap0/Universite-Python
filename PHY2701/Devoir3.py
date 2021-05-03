# -.- coding:latin1 -.-
# @author: Nicolas

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cst

# On d�finit les constantes de l'�toile �tudi�e
rayonEtoile = 6.957e8
masseEtoile = 1.989e30

# On d�finit la distance avec le centre de l'�toile (qu'on appelle rayon)
rayon = np.linspace(0, rayonEtoile, 10000)

# On calcule la pression � partir du rayon
cstePression = 3 * cst.G * masseEtoile ** 2 / (8 * cst.pi * rayonEtoile ** 6)
pression = cstePression * (rayonEtoile ** 2 - rayon ** 2)

# On calcule la temp�rature en fonction du rayon
csteTemperature = cst.G * cst.atomic_mass * 0.6 * \
    masseEtoile / (2 * rayonEtoile ** 3 * cst.k)
temperature = csteTemperature * (rayonEtoile ** 2 - rayon ** 2)

# On modifie le rayon, la pression et la temp�rature pour s'affranchir des 
# unit�s
rayon /= rayonEtoile
pression /= pression.max()
temperature /= temperature.max()

# On trace le premier graphique, celui du rayon de la pression en fonction du
# rayon de l'�toile
plt.figure(1)
plt.plot(rayon, pression)

# On change les param�tres esth�tiques du graphique
plt.xlabel("Distance avec le centre de l'�toile (en proportion)")
plt.ylabel("Pression dans l'�toile (en proportion)")
plt.title("Pression dans une �toile selon le rayon parcouru")

plt.savefig("PHY2701Devoir3Fig1.png")

# On trace le deuxieme graphique, celui du rayon de la temp�rature en fonction 
# du rayon de l'�toile
plt.figure(2)
plt.plot(rayon, temperature)

# On change les param�tres esth�tiques du graphique
plt.xlabel("Distance avec le centre de l'�toile (en proportion)")
plt.ylabel("Temp�rature dans l'�toile (en proportion)")
plt.title("Temp�rature dans une �toile selon le rayon parcouru")

plt.savefig("PHY2701Devoir3Fig2.png")

# On montre les graphiques produits
plt.show()
