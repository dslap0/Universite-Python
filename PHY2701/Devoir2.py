# -*- coding: latin-1 -*-
#@author: Nicolas

""" Ce code sert � trouver la fraction d'atomes ionis�s dans un gaz et � tracer
un graphique de cette fraction selon la temp�rature, pour un niveau
d'ionisation de 2 (code utile pour le probl�me 4 partie b du devoir 2 en 
Astronomie).
"""

import numpy as np
import scipy.constants as cst

import matplotlib.pyplot as plt


def calculFractionIonises(temperature, densiteGaz):
    """ Cette fonction trouve la fraction d'atomes ionis�s de niveau 2 � partir 
    de param�tres fournis en argument dans un gaz d'hydrog�ne �lectriquement 
    neutre.
    niveau: niveau d'ionisation recherch�.
    temperature: temp�rature dans le gaz.
    """
    khi = 13.6 * 1.6e-19

    # On d�finit les coefficients de l'�quation
    b = (cst.m_p / densiteGaz) * (2 * cst.pi * cst.m_e * cst.Boltzmann *
        temperature / cst.Planck ** 2) ** (3 / 2) * np.exp(-khi / 
        (cst.Boltzmann * temperature))
    c = -b


    # On trouve les z�ros
    x1 = (-b + np.sqrt(b ** 2 - 4 * c)) / 2
    x2 = (-b - np.sqrt(b ** 2 - 4 * c)) / 2

    return x1, x2


# On d�finit un array avec les temp�ratures
temperature = np.linspace(5e3, 25e3, 1000)

# On trouve les z�ros de la fonction recherch�s
x1, x2 = calculFractionIonises(temperature, 1e-6)

# On teste laquelle des deux solutions est possible
x = x1 if x1.all() >= 0 else x2

plt.figure(0)

plt.plot(temperature, x)

# On modifie les param�tres esth�tiques du graphique
plt.xlabel('Temp�rature du gaz (en K)')
plt.ylabel('Proportions d\'atomes ionis�s')

plt.savefig('Devoir2Astrofig1.png')
plt.show()
