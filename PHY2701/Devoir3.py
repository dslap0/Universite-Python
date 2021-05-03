# -.- coding:latin1 -.-
# @author: Nicolas

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cst

# On définit les constantes de l'étoile étudiée
rayonEtoile = 6.957e8
masseEtoile = 1.989e30

# On définit la distance avec le centre de l'étoile (qu'on appelle rayon)
rayon = np.linspace(0, rayonEtoile, 10000)

# On calcule la pression à partir du rayon
cstePression = 3 * cst.G * masseEtoile ** 2 / (8 * cst.pi * rayonEtoile ** 6)
pression = cstePression * (rayonEtoile ** 2 - rayon ** 2)

# On calcule la température en fonction du rayon
csteTemperature = cst.G * cst.atomic_mass * 0.6 * \
    masseEtoile / (2 * rayonEtoile ** 3 * cst.k)
temperature = csteTemperature * (rayonEtoile ** 2 - rayon ** 2)

# On modifie le rayon, la pression et la température pour s'affranchir des 
# unités
rayon /= rayonEtoile
pression /= pression.max()
temperature /= temperature.max()

# On trace le premier graphique, celui du rayon de la pression en fonction du
# rayon de l'étoile
plt.figure(1)
plt.plot(rayon, pression)

# On change les paramètres esthétiques du graphique
plt.xlabel("Distance avec le centre de l'étoile (en proportion)")
plt.ylabel("Pression dans l'étoile (en proportion)")
plt.title("Pression dans une étoile selon le rayon parcouru")

plt.savefig("PHY2701Devoir3Fig1.png")

# On trace le deuxieme graphique, celui du rayon de la température en fonction 
# du rayon de l'étoile
plt.figure(2)
plt.plot(rayon, temperature)

# On change les paramètres esthétiques du graphique
plt.xlabel("Distance avec le centre de l'étoile (en proportion)")
plt.ylabel("Température dans l'étoile (en proportion)")
plt.title("Température dans une étoile selon le rayon parcouru")

plt.savefig("PHY2701Devoir3Fig2.png")

# On montre les graphiques produits
plt.show()
