# -.- coding:latin1 -.-
# @author: Nicolas
""" Ce code sert à mettre en graphique I/I0 en fonction de theta afin de
préparer le laboratoire 6.
"""

import numpy as np

import matplotlib.pyplot as plt

def traceGraph(x, y):
    """ On trace un graphique avec matplotlib et on modifie les options
    esthétiques de celui-ci.
    """
    plt.plot(x, y, '-')

    # On modifie les options esthétiques
    plt.xlabel(r'$\theta$ (en radians)')
    plt.ylabel(r'$\frac{I}{I_0}$')
    plt.xlim(-0.1, 0.1)
    plt.ylim(0, 0.05)

""" On initialise les variables importantes """
# Largeur d'une fente
b = 0.04e-3
# Distance entre les fentes
d = 0.25e-3
# Longueur d'onde des faisceauc
longueurDOnde = 632.8e-9
# Angles pour le traçage de la courbe
theta = np.linspace(-0.5, 0.5, 100000)

alpha = np.pi * b * np.sin(theta) / longueurDOnde
beta = np.pi * d * np.sin(theta) / longueurDOnde

ISurI01 = np.sin(alpha) ** 2 / alpha ** 2
ISurI02 = ISurI01 * (np.sin(2 * beta) ** 2 / (2 * np.sin(beta)) ** 2)

# On trace pour une fente
plt.figure(0)
traceGraph(theta, ISurI01)
plt.savefig('PreLab6_Fig1.png')


# On trace pour 2 fentes
plt.figure(1)
traceGraph(theta, ISurI02)
plt.savefig('PreLab6_Fig2.png')

plt.show()