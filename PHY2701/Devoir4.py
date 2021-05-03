# -.- coding:latin1 -.-
# @author: Nicolas Levasseur

import numpy as np
import matplotlib.pyplot as plt

def calcul_temperature(albedo, angle, temperatureEtoile, rayonEtoile, 
    distanceEtoile):
    const = (1 - albedo) ** (1/4) * \
        temperatureEtoile * np.sqrt(rayonEtoile / distanceEtoile)
    return const * np.cos(angle) ** (1/4)


# On définit les constantes pour Mercure
albedo = 0.06
distanceEtoile = 57.9e9 # Source : https://www.asc-csa.gc.ca/fra/astronomie/systeme-solaire/mercure.asp
temperatureEtoile = 5778
rayonEtoile = 6.957e8

# Constantes utiles pour la suite des calculs
angle = np.linspace(-np.pi / 2, np.pi / 2, 1000)

temperature = calcul_temperature(
    albedo, angle, temperatureEtoile, rayonEtoile, distanceEtoile)

plt.plot(angle / np.pi, temperature)

# On modifie les options esthétiques du graphique
plt.xlabel(r"Latitude par rapport a l'équateur (en $\pi$ radians)")
plt.ylabel("Température (en Kelvins)")

plt.savefig("PHY2701Devoir4Fig1.png")
plt.show()

# On trouve la température au point sub-solaire
temperatureSubSolaire = calcul_temperature(
    albedo, 0, temperatureEtoile, rayonEtoile, distanceEtoile)

print("La température au point sub-solaire est de %.f K." % temperatureSubSolaire)
