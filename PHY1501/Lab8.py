# -.- coding:latin1 -.-
# @author: Nicolas
""" Ce code produit les résultats et les graphiques voulus pour le
laboratoire 8, portant sur la déviation lumineuse dans un prisme.
"""

import numpy as np
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

def cauchy(longueurDOndeRaie, B, A):
    """ Cette fonction trouve la valeur de l'indice de réfraction 
    associé à la longueur d'onde d'une raie et à ses coefficients de
    Cauchy par la méthode éponyme.
    longueurDOndeRaie : Longueurs d'ondes des raies à étudier (ndarray, 
    float, en nm).
    B : Coefficient de Cauchy du produit (float).
    A : Coefficient de Cauchy de la somme (float).
    """
    return B / longueurDOndeRaie ** 2 + A

def calculIncertitudeIndiceRefractionCauchy(incertitudeCoeffCauchy,
incertitudeLongueurDOndeCauchy, B, longueurDOndeCauchy):
    """ Cette fonction vise à calculer l'incertitude sur l'indice de 
    réfraction calculé par la méthode de Cauchy (voir fonction cauchy).
    incertitudeCoeffCauchy : Incertitudes sur les coefficients de Cauchy
    (ndarray, float)
    incertitudeLongueurDOndeCauchy : Incertitude sur la longueur d'onde
    théorique donnée (ndarray, float, en nm).
    B : Coefficient de Cauchy du produit (float).
    longueurDOndeCauchy : Longueur d'onde théorique donnée (float).
    """
    return np.sqrt(incertitudeCoeffCauchy[1] ** 2 + 
(incertitudeCoeffCauchy[0] / longueurDOndeCauchy ** 2) ** 2 + (2 * B * 
incertitudeLongueurDOndeCauchy / longueurDOndeCauchy ** 3) ** 2)

def traceGraph(longueurDOndeRaie, indiceRefraction, cauchy,
incertitudeLongueurDOndeRaieGraph, incertitudeIndiceRefraction):
    """ Cette fonction trace le graphique de l'indice de refraction en 
    fonction de la longueur d'onde et trace la courbe de regression du
    khi deux en fonction de ses valeurs. Elle retourne les valeurs des
    coefficients de cette courbe, la matrice de leur covariance et leur
    incertitude.
    """
    plt.plot(longueurDOndeRaie ** -2, indiceRefraction, '.g',
    label='Données expérimentales')
    # On trace le premier graphique

    coeffCauchy, covarCoeffCauchy = curve_fit(cauchy, longueurDOndeRaie,
    indiceRefraction)
    incertitudeCoeffCauchy = np.sqrt(np.diag(covarCoeffCauchy))
    # On trouve les coefficients de Cauchy du prisme #63 et leurs incertitudes

    x = np.linspace(2.5e-6, 5.5e-6, 100)
    y = coeffCauchy[0] * x + coeffCauchy[1]
    plt.plot(x, y, '-', label='Droite de régression obtenue avec curve_fit')
    # On trace la courbe de régression

    plt.xlabel("Inverse de la longueur d'onde au carré (en 1/nm$^{2}$)")
    plt.ylabel("Indice de réfraction")
    plt.errorbar(longueurDOndeRaie ** -2, indiceRefraction,
    xerr=incertitudeLongueurDOndeRaieGraph,
    yerr=incertitudeIndiceRefraction, linestyle='None', color='g')
    plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    plt.legend()
    # On modifie les options esthétiques du graphique

    return coeffCauchy, covarCoeffCauchy, incertitudeCoeffCauchy

angleRaieReseauMesure = np.array([98.5 + 2 / 60, 100 + 2 / 60,
101 + 10 / 60, 102.5, 103.5 + 11 / 60, 103.5 + 21 / 60])
incertitudeAngleRaieReseauMesure = 2 / 60
longueurDOndeRaie = np.array([0, 0, 0, 0, 576.96, 579.07])

"""On entre les données expérimentales mesurées avec le réseau de diffraction, 
l'incertitude déterminée lors de la mesure et les longueurs d'ondes données"""

angleRaieReseau = (2 * np.pi * (angleRaieReseauMesure - 83.2)) / 360
incertitudeAngleRaieReseau = np.sqrt(2 * ((np.pi / 360 * \
incertitudeAngleRaieReseauMesure) ** 2))
# On la véritable valeur de l'angle de chaque raie et son incertitude

distanceFentes = np.mean(longueurDOndeRaie[-2:] / 
np.sin(angleRaieReseau[-2:]))
incertitudeDistanceFentes = np.sqrt(np.sum((longueurDOndeRaie[-2:] * \
incertitudeAngleRaieReseau / (2 * np.cos(angleRaieReseau[-2:]))) ** 2))
# On trouve la distance entre les raies des fentes et son incertitude

longueurDOndeRaie[:-2] = distanceFentes * np.sin(angleRaieReseau[:-2])
incertitudeLongueurDOndeRaie = np.sqrt((np.sin(angleRaieReseau[:-2]) * \
incertitudeDistanceFentes) ** 2 + (distanceFentes * \
np.cos(angleRaieReseau[:-2]) * incertitudeAngleRaieReseau) ** 2)
# On trouve les longueurs d'ondes expérimentales et leurs incertitudes

distanceFentesTheorique = 2.54e7 / 15000
incertitudeDistanceFentesTheorique = abs(2.54e7 / 15500 - 2.54e7 / 14500) / 2
longueurDOndeRaie[-2:] = distanceFentesTheorique * np.sin(angleRaieReseau[-2:])
incertitudeLongueurDOndeRaieJaunes = np.sqrt((np.sin(angleRaieReseau[-2:]) * 
incertitudeDistanceFentesTheorique) ** 2 + (np.cos(angleRaieReseau[-2:]) * 
incertitudeAngleRaieReseau) ** 2)
incertitudeLongueurDOndeRaie = np.append(incertitudeLongueurDOndeRaie,
incertitudeLongueurDOndeRaieJaunes)
# On trouve les longueurs d'ondes des deux raies jaunes et leurs incertitude

angleDArrete = (np.pi * np.array([118 + 18 / 60 - 1 - 8 / 60,
109 + 25 / 60 - (360 - 349.5)])) / 360
incertitudeAngleDArrete = incertitudeAngleRaieReseau
# On trouve les angles d'arrêtes des deux prismes et leurs incertitudes

minimumDeviation = np.array([[175.5 + 2 / 60, 344 + 11 / 60], [177 + 16 / 60, 
346 + 18 / 60], [178 + 8 / 60, 347 + 9 / 60], [178.5 + 15 / 60, 348 + 9 / 60],
[179 + 17 / 60, 348.5 + 16 / 60], [179 + 19 / 60, 348.5 + 19 / 60]]) 
minimumDeviation[:, 0] = 180 - minimumDeviation[:, 0] + 66.5 + 24 / 60
minimumDeviation[:, 1] = 360 - minimumDeviation[:, 1] + 56 + 26 / 60
minimumDeviation = 2 * np.pi * minimumDeviation / 360
incertitudeMinimumDeviation = incertitudeAngleRaieReseau
# On trouve le minimum de déviation et l'incertitude sur celui-ci

indiceRefraction = (np.sin((minimumDeviation + angleDArrete) / 2)) / \
np.sin(angleDArrete / 2)
incertitudeIndiceRefraction = np.sqrt(((np.cos((minimumDeviation +
angleDArrete) / 2) * incertitudeMinimumDeviation) / (2 * 
np.sin(angleDArrete / 2))) ** 2 + ((np.cos((minimumDeviation + angleDArrete) / 
2) / np.cos(angleDArrete / 2)) * incertitudeAngleDArrete) ** 2)
# On trouve l'indice de réfraction et son incertitude

incertitudeLongueurDOndeRaieGraph = ((longueurDOndeRaie - 
incertitudeLongueurDOndeRaie) ** -2 - (longueurDOndeRaie + 
incertitudeLongueurDOndeRaie) ** -2) / 2

plt.figure(0)
coeffCauchy0, covarCoeffCauchy0, incertitudeCoeffCauchy0 = \
traceGraph(longueurDOndeRaie, indiceRefraction[:, 0], cauchy,
incertitudeLongueurDOndeRaieGraph, incertitudeIndiceRefraction[:, 0])
plt.savefig("Lab8 Figure 0.png")

plt.figure(1)
coeffCauchy1, covarCoeffCauchy1, incertitudeCoeffCauchy1 = \
traceGraph(longueurDOndeRaie, indiceRefraction[:, 1], cauchy,
incertitudeLongueurDOndeRaieGraph, incertitudeIndiceRefraction[:, 1])
plt.savefig("Lab8 Figure 1.png")

longueurDOndeCauchy = np.array([587.56, 486.13, 656.281])
incertitudeLongueurDOndeCauchy = np.array([0.005, 0.005, 0.0005])

"""On met les longueurs d'onde qui servent à évaluer l'indice de réfraction
avec la méthode de Cauchy pour trouver le nombre d'Abbé et leurs
incertitudes"""

coeffCauchy = np.stack((coeffCauchy0, coeffCauchy1), axis=-1)
incertitudeCoeffCauchy = np.stack((incertitudeCoeffCauchy0, incertitudeCoeffCauchy1), axis=-1)

indiceRefractionCauchy = cauchy(longueurDOndeCauchy, coeffCauchy[0, 0],
coeffCauchy[1, 0])
incertitudeIndiceRefractionCauchy = \
calculIncertitudeIndiceRefractionCauchy(incertitudeCoeffCauchy[:, 0],
incertitudeLongueurDOndeCauchy, coeffCauchy[0, 0], longueurDOndeCauchy)

for i in range(1, coeffCauchy[:, 0].size):
    """On calcule les indices de réfraction et leurs incertitudes pour chaque 
    prisme pour calculer leur nombre d'Abbe"""
    nvIndiceRefractionCauchy = cauchy(longueurDOndeCauchy, coeffCauchy[0, i],
    coeffCauchy[1, i])
    indiceRefractionCauchy = np.stack((indiceRefractionCauchy, 
nvIndiceRefractionCauchy), axis =-1)
    nvIncertitudeIndiceRefractionCauchy = \
calculIncertitudeIndiceRefractionCauchy(incertitudeCoeffCauchy[:, i],
incertitudeLongueurDOndeCauchy, coeffCauchy[0, i], longueurDOndeCauchy)
    incertitudeIndiceRefractionCauchy = \
np.stack((incertitudeIndiceRefractionCauchy,
nvIncertitudeIndiceRefractionCauchy), axis=-1)

nombreDAbbe = (indiceRefractionCauchy[0, :] - 1) / \
(indiceRefractionCauchy[1, :] - indiceRefractionCauchy[2, :])
incertitudeNombreDAbbe = np.sqrt((incertitudeIndiceRefraction[0, :] / 
indiceRefractionCauchy[1] - indiceRefractionCauchy[2]) ** 2 + \
(incertitudeIndiceRefractionCauchy[1, :] * (indiceRefractionCauchy[0] - 1) / 
(indiceRefractionCauchy[1] - indiceRefractionCauchy[2]) ** 2) ** 2 + 
(incertitudeIndiceRefractionCauchy[2, :] * (indiceRefractionCauchy[0] - 1) / 
(indiceRefractionCauchy[1] - indiceRefractionCauchy[2]) ** 2) ** 2)
# On trouve les nombres d'Abbe des prismes et leurs incertitude

print("\nThêta des raies diffractées par le réseau de diffraction (du " +
"violet au rouge, en \nradians):")
print(angleRaieReseau)
print("Incertitude sur le thêta des raies diffractées par le réseau (en " + 
"radians):")
print(incertitudeAngleRaieReseau)
print("\nDistance entre les fentes du réseau de diffraction (en " +
"nanomètres):")
print(distanceFentes)
print("Incertitude sur les distances entre les fentes (en nanomètres):")
print(incertitudeDistanceFentes)
print("\nDistance entre deux fentes du réseau de diffraction telles que " +
"données par le \nconstructeur (en nanomètres):")
print(distanceFentesTheorique)
print("Incertitude sur la distance entre deux fentes du réseau de " + 
"diffraction \ndonnée par le constructeur, correspondant à 500 fentes par " +
"pouce (en nanomètres):")
print(incertitudeDistanceFentesTheorique)
print("\nLongueurs d'ondes des raies émises par la lampe (du violet au " +
"rouge, en nanomètres):")
print(longueurDOndeRaie)
print("Incertitude sur les longueurs d'onde des raies émises par la lampe " +
"(du violet au \nrouge, en nanomètres):")
print(incertitudeLongueurDOndeRaie)
print("\nAngle d'arrête des prismes (le premier étant le #54, le tout en " +
"radians):")
print(angleDArrete)
print("Incertitude sur l'angle d'arrête des prismes (en radians):")
print(incertitudeAngleDArrete)
print("\nMinimums de déviation pour chaque raie, en partant du violet au " + 
"jaune (les deux \nraies violettes sont sur la même ligne, la première étant " +
"la raie du prisme #54, \nle tout en radians):")
print(minimumDeviation)
print("Incertitude sur les minimums de déviations (en radians):")
print(incertitudeMinimumDeviation)
print("\nIndices de réfraction des raies diffractés par les prismes (le " +
"premier prisme étant le #54):")
print(indiceRefraction)
print("Incertitude sur les indices de réfraction pour chaque raie, en " + 
"partant du violet \nau jaune (les deux raies violettes sont sur la même " +
"ligne, la première étant la \nraie du prisme #54):")
print(incertitudeIndiceRefraction)
print("\nValeurs des coefficients de Cauchy B et A des prismes selon " + 
"l'équation de Cauchy \n(le prisme #54 en premier):")
print(coeffCauchy)
print("Incertitudes des coefficients de Cauchy B et A des prismes selon " +
"l'équation de Cauchy \n(le prisme #54 en premier):")
print(incertitudeCoeffCauchy)
print("\nValeurs des indices de réfraction pour une longueur d'onde de " +
"587.56 nm (prisme #54 \nen premier):")
print(indiceRefractionCauchy[0, :])
print("Incertitude des indices de réfraction pour une longueur d'onde de " +
"587.56 nm (prisme #54 \nen premier):")
print(incertitudeIndiceRefractionCauchy[0, :])
print("\nNombre d'Abbe des prismes #54 et #63, respectivement:")
print(nombreDAbbe)
print("Incertitude sur le nombe d'Abbe des prismes #54 et #63, respectivement:")
print(incertitudeNombreDAbbe)
print("\nMatrices de covariance de la droite de regression du khi-deux:")
print(covarCoeffCauchy0)
print(covarCoeffCauchy1)
plt.show()
# On présente les résultats à l'utilisateur