# -.- coding:latin1 -.-
# @author: Nicolas
""" Ce code sert à mettre en graphique le potentiel électrique sur 
l'énergie en fonction de la fréquence dans deux circuits RCL 
prédéterminés.
"""

import numpy as np

import matplotlib.pyplot as plt

resistance = [1000, 10000]
capacite = [50e-9, 10e-9]

frequence = np.linspace(100, 100000, 10000)
# On met des fréquence sur le domaine de la fonction qu'on veut étudier

potentielSurEnergieA = 1 / np.sqrt(1 + 1 / (resistance[0] * capacite[0] * 2 * 
np.pi * frequence) ** 2)
potentielSurEnergieB = 1 / np.sqrt(1 + 1 / (resistance[1] * capacite[1] * 2 * 
np.pi * frequence) ** 2)
# On calcule les valeurs qu'on veut afficher

plt.figure(0)
plt.plot(frequence, potentielSurEnergieA, '-')

plt.xlabel("Fréquence de l'oscillateur (en Hz)")
plt.ylabel(r"$\frac{V}{E}$ (en joules/volts)")
# On modifie les options graphiques

plt.savefig("PreLab1FigA.png")

plt.figure(1)
plt.plot(frequence, potentielSurEnergieB, '-')

plt.xlabel("Fréquence de l'oscillateur (en Hz)")
plt.ylabel(r"$\frac{V}{E}$ (en joules/volts)")
# On modifie les options graphiques

plt.savefig("PreLab1FigB.png")

plt.show()