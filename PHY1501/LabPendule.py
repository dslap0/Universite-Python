# -.- coding:latin1 -.-
# @author : Nicolas
""" Ce code analyse les données de l'expérience maison sur le pendule et 
fourni les graphiques et les résultats voulus
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def f(x, a, b):
    return a * x + b


l = 1.05
dL = 0.05
m = 137e-3
dM = 0.5e-3
d = 5.5e-2
dD = 0.5e-2

# Partie (1) du labo 
a1 = np.array([5, 10, 15, 20, 25, 30])
dA1 = 0.5
t1 = np.array([1.78, 2, 1.9, 1.95, 2.04, 1.78])
dT1 = 0.3

plt.figure(1)
plt.plot(a1, t1, '.', label="Points expérimentaux", color='b')

# On modifie les paramètres esthétiques du graphique
plt.errorbar(a1, t1, dT1, dA1, ls='None', color='b')
plt.xlabel("Amplitude de départ de l'oscillation (degré)")
plt.ylabel("Durée d'une oscillation (s)")
plt.legend()

plt.savefig("LabPenduleFig1.png")

# Partie (2) du labo
a2 = a1
dA2 = dA1
t2 = np.array([20.63, 20.64, 20.79, 20.85, 20.9, 21.17])
dT2 = dT1

plt.figure(2)
plt.plot(a2, t2, '.', label="Points expérimentaux", color='b')


# On modifie les paramètres esthétiques du graphique
plt.errorbar(a2, t2, dT2, dA2, ls='None', color='b')
plt.xlabel("Amplitude de départ de l'oscillation (degré)")
plt.ylabel("Durée de 10 oscillations (s)")
plt.legend()

plt.savefig("LabPenduleFig2.png")

a3 = np.array([30, 22, 18, 14, 13, 11, 10, 8, 7, 6, 6, 5, 5, 4, 4, 4, 3, 3, 3, 
    2, 2])
dA3 = 0.7
t3 = np.array([0., 20.57, 41.67, 62.56, 83.54, 104.52, 125.47, 146.34, 167.18, 
    188.06, 209.02, 229.82, 250.61, 271.45, 292.31, 313.1, 333.92, 354.74, 
    375.65, 396.29, 417.25])
dT3 = dT2

# On trouve la hauteur du pendule
xExp = l * (1 - np.cos(a3 * np.pi / 180))
dXExp = np.sqrt(dL * (1 - np.cos(a3 * np.pi / 180)) ** 2 + (dA3 * np.pi / 180 * 
    l * (1 + np.sin(a3 * np.pi / 180))) ** 2)

# On trouve les beta expérimentaux pour chaque oscillation
betaExp = -np.log(xExp[1:] / xExp[0]) / t3[1:]
dBetaExp = np.sqrt((-xExp[0] * np.log(xExp[1:]) * dXExp[1:] / t3[1:]) ** 2 + 
    (-np.log(1 / xExp[0]) * dXExp[1:] / (t3[1:] * xExp[1:])) ** 2 + 
    (-np.log(xExp[1:] / xExp[0]) * dT3 / t3[1:] ** 2) ** 2)

# On fait la moyenne sur les betas obtenus
betaExpMoy = np.mean(betaExp)
dBetaExpMoy = np.std(betaExp)

xExp = xExp[0] * np.exp(-betaExpMoy * t3)
aExp = aTh = np.arccos((l - xExp) / l) * 180 / np.pi

print(betaExpMoy, dBetaExpMoy)

# On trouve b théorique
b = 3 * np.pi * d * 1.7e-5
dB = np.sqrt((3 * np.pi * 1.7e-5 * dD) ** 2 + (3 * np.pi * d * 0.2e-5) ** 2)

# On troube beta theorique
betaTh = b / (2 * m)
dBetaTh = np.sqrt((b * dM / (2 * m ** 2)) ** 2 + (dB / (2 * m)) ** 2)

print(betaTh, dBetaTh)

# On trouve les x théoriques
xTh = xExp[0] * np.exp(-betaTh * t3)
dXTh = np.sqrt((-xExp[0] * t3 * dBetaTh * np.exp(-betaTh * t3)) ** 2 + 
    (-xExp[0] * dT3 * betaTh * np.exp(-betaTh * t3) ** 2) + (dXExp[0] * 
    np.exp(-betaTh * t3)) ** 2)

# On trouve les amplitudes théoriques
aTh = np.arccos((l - xTh) / l) * 180 / np.pi
dATh = np.sqrt((((1 - 1 / l) * dXTh * np.sqrt(1 - ((l - xTh) / l) ** 2) ** 
    -1) ** 2 + ((1 - xTh / l ** 2) * dL * np.sqrt(1 - ((l - xTh) / l) ** 2) ** 
    -1) ** 2) * 180 / np.pi)

plt.figure(3)

plt.plot(t3, a3, '.', label="Points expérimentaux", color='b')
plt.plot(t3, aTh, '-', label=r"Courbe avec $\beta_{th}$", color='r')
plt.plot(t3, aExp, '-', label=r"Courbe avec $\beta_{exp}$", color='y')

# On modifie les paramètres esthétiques du graphique
plt.errorbar(t3, a3, dA3, dT3, ls='None', color='b')
plt.xlabel("Temps écoulé (s)")
plt.ylabel("Amplitude de l'oscillation (degrés)")
plt.legend()

plt.savefig("LabPenduleFig3.png")

# On trouve w1
w1 = np.array([])
for i in range(0, len(t3) - 1):
    w1 = 10 / (t3[i + 1] - t3[i])

# On trouve w0
w0 = np.sqrt(w1 ** 2 + betaExp ** 2)
w0Moy = np.mean(w0)
dW0Moy = np.std(w0)

# On trouve l'accélération gravitationnelle expérimentale
g = l * w0Moy ** 2
dG = np.sqrt((w0Moy ** 2 * dL) ** 2 + (2 * l * w0Moy * dW0Moy) ** 2)

print(w0Moy, dW0Moy)
print(g, dG)

plt.show()