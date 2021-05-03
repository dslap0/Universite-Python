# -*- coding: latin-1 -*-
#@author: Nicolas

""" Ce code sert à trouver la fraction d'atomes ionisés dans un gaz et à tracer
un graphique de cette fraction selon la température, pour un niveau
d'ionisation de 2 (code utile pour le problème 4 partie b du devoir 2 en 
Astronomie).
"""

import numpy as np
import scipy.constants as cst

import matplotlib.pyplot as plt


def calculFractionIonises(temperature, densiteGaz):
    """ Cette fonction trouve la fraction d'atomes ionisés de niveau 2 à partir 
    de paramètres fournis en argument dans un gaz d'hydrogène électriquement 
    neutre.
    niveau: niveau d'ionisation recherché.
    temperature: température dans le gaz.
    """
    khi = 13.6 * 1.6e-19

    # On définit les coefficients de l'équation
    b = (cst.m_p / densiteGaz) * (2 * cst.pi * cst.m_e * cst.Boltzmann *
        temperature / cst.Planck ** 2) ** (3 / 2) * np.exp(-khi / 
        (cst.Boltzmann * temperature))
    c = -b


    # On trouve les zéros
    x1 = (-b + np.sqrt(b ** 2 - 4 * c)) / 2
    x2 = (-b - np.sqrt(b ** 2 - 4 * c)) / 2

    return x1, x2


# On définit un array avec les températures
temperature = np.linspace(5e3, 25e3, 1000)

# On trouve les zéros de la fonction recherchés
x1, x2 = calculFractionIonises(temperature, 1e-6)

# On teste laquelle des deux solutions est possible
x = x1 if x1.all() >= 0 else x2

plt.figure(0)

plt.plot(temperature, x)

# On modifie les paramètres esthétiques du graphique
plt.xlabel('Température du gaz (en K)')
plt.ylabel('Proportions d\'atomes ionisés')

plt.savefig('Devoir2Astrofig1.png')
plt.show()
