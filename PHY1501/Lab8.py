# -.- coding:latin1 -.-
# @author: Nicolas
""" Ce code produit les r�sultats et les graphiques voulus pour le
laboratoire 8, portant sur la d�viation lumineuse dans un prisme.
"""

import numpy as np
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

def cauchy(longueurDOndeRaie, B, A):
    """ Cette fonction trouve la valeur de l'indice de r�fraction 
    associ� � la longueur d'onde d'une raie et � ses coefficients de
    Cauchy par la m�thode �ponyme.
    longueurDOndeRaie : Longueurs d'ondes des raies � �tudier (ndarray, 
    float, en nm).
    B : Coefficient de Cauchy du produit (float).
    A : Coefficient de Cauchy de la somme (float).
    """
    return B / longueurDOndeRaie ** 2 + A

def calculIncertitudeIndiceRefractionCauchy(incertitudeCoeffCauchy,
incertitudeLongueurDOndeCauchy, B, longueurDOndeCauchy):
    """ Cette fonction vise � calculer l'incertitude sur l'indice de 
    r�fraction calcul� par la m�thode de Cauchy (voir fonction cauchy).
    incertitudeCoeffCauchy : Incertitudes sur les coefficients de Cauchy
    (ndarray, float)
    incertitudeLongueurDOndeCauchy : Incertitude sur la longueur d'onde
    th�orique donn�e (ndarray, float, en nm).
    B : Coefficient de Cauchy du produit (float).
    longueurDOndeCauchy : Longueur d'onde th�orique donn�e (float).
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
    label='Donn�es exp�rimentales')
    # On trace le premier graphique

    coeffCauchy, covarCoeffCauchy = curve_fit(cauchy, longueurDOndeRaie,
    indiceRefraction)
    incertitudeCoeffCauchy = np.sqrt(np.diag(covarCoeffCauchy))
    # On trouve les coefficients de Cauchy du prisme #63 et leurs incertitudes

    x = np.linspace(2.5e-6, 5.5e-6, 100)
    y = coeffCauchy[0] * x + coeffCauchy[1]
    plt.plot(x, y, '-', label='Droite de r�gression obtenue avec curve_fit')
    # On trace la courbe de r�gression

    plt.xlabel("Inverse de la longueur d'onde au carr� (en 1/nm$^{2}$)")
    plt.ylabel("Indice de r�fraction")
    plt.errorbar(longueurDOndeRaie ** -2, indiceRefraction,
    xerr=incertitudeLongueurDOndeRaieGraph,
    yerr=incertitudeIndiceRefraction, linestyle='None', color='g')
    plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    plt.legend()
    # On modifie les options esth�tiques du graphique

    return coeffCauchy, covarCoeffCauchy, incertitudeCoeffCauchy

angleRaieReseauMesure = np.array([98.5 + 2 / 60, 100 + 2 / 60,
101 + 10 / 60, 102.5, 103.5 + 11 / 60, 103.5 + 21 / 60])
incertitudeAngleRaieReseauMesure = 2 / 60
longueurDOndeRaie = np.array([0, 0, 0, 0, 576.96, 579.07])

"""On entre les donn�es exp�rimentales mesur�es avec le r�seau de diffraction, 
l'incertitude d�termin�e lors de la mesure et les longueurs d'ondes donn�es"""

angleRaieReseau = (2 * np.pi * (angleRaieReseauMesure - 83.2)) / 360
incertitudeAngleRaieReseau = np.sqrt(2 * ((np.pi / 360 * \
incertitudeAngleRaieReseauMesure) ** 2))
# On la v�ritable valeur de l'angle de chaque raie et son incertitude

distanceFentes = np.mean(longueurDOndeRaie[-2:] / 
np.sin(angleRaieReseau[-2:]))
incertitudeDistanceFentes = np.sqrt(np.sum((longueurDOndeRaie[-2:] * \
incertitudeAngleRaieReseau / (2 * np.cos(angleRaieReseau[-2:]))) ** 2))
# On trouve la distance entre les raies des fentes et son incertitude

longueurDOndeRaie[:-2] = distanceFentes * np.sin(angleRaieReseau[:-2])
incertitudeLongueurDOndeRaie = np.sqrt((np.sin(angleRaieReseau[:-2]) * \
incertitudeDistanceFentes) ** 2 + (distanceFentes * \
np.cos(angleRaieReseau[:-2]) * incertitudeAngleRaieReseau) ** 2)
# On trouve les longueurs d'ondes exp�rimentales et leurs incertitudes

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
# On trouve les angles d'arr�tes des deux prismes et leurs incertitudes

minimumDeviation = np.array([[175.5 + 2 / 60, 344 + 11 / 60], [177 + 16 / 60, 
346 + 18 / 60], [178 + 8 / 60, 347 + 9 / 60], [178.5 + 15 / 60, 348 + 9 / 60],
[179 + 17 / 60, 348.5 + 16 / 60], [179 + 19 / 60, 348.5 + 19 / 60]]) 
minimumDeviation[:, 0] = 180 - minimumDeviation[:, 0] + 66.5 + 24 / 60
minimumDeviation[:, 1] = 360 - minimumDeviation[:, 1] + 56 + 26 / 60
minimumDeviation = 2 * np.pi * minimumDeviation / 360
incertitudeMinimumDeviation = incertitudeAngleRaieReseau
# On trouve le minimum de d�viation et l'incertitude sur celui-ci

indiceRefraction = (np.sin((minimumDeviation + angleDArrete) / 2)) / \
np.sin(angleDArrete / 2)
incertitudeIndiceRefraction = np.sqrt(((np.cos((minimumDeviation +
angleDArrete) / 2) * incertitudeMinimumDeviation) / (2 * 
np.sin(angleDArrete / 2))) ** 2 + ((np.cos((minimumDeviation + angleDArrete) / 
2) / np.cos(angleDArrete / 2)) * incertitudeAngleDArrete) ** 2)
# On trouve l'indice de r�fraction et son incertitude

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

"""On met les longueurs d'onde qui servent � �valuer l'indice de r�fraction
avec la m�thode de Cauchy pour trouver le nombre d'Abb� et leurs
incertitudes"""

coeffCauchy = np.stack((coeffCauchy0, coeffCauchy1), axis=-1)
incertitudeCoeffCauchy = np.stack((incertitudeCoeffCauchy0, incertitudeCoeffCauchy1), axis=-1)

indiceRefractionCauchy = cauchy(longueurDOndeCauchy, coeffCauchy[0, 0],
coeffCauchy[1, 0])
incertitudeIndiceRefractionCauchy = \
calculIncertitudeIndiceRefractionCauchy(incertitudeCoeffCauchy[:, 0],
incertitudeLongueurDOndeCauchy, coeffCauchy[0, 0], longueurDOndeCauchy)

for i in range(1, coeffCauchy[:, 0].size):
    """On calcule les indices de r�fraction et leurs incertitudes pour chaque 
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

print("\nTh�ta des raies diffract�es par le r�seau de diffraction (du " +
"violet au rouge, en \nradians):")
print(angleRaieReseau)
print("Incertitude sur le th�ta des raies diffract�es par le r�seau (en " + 
"radians):")
print(incertitudeAngleRaieReseau)
print("\nDistance entre les fentes du r�seau de diffraction (en " +
"nanom�tres):")
print(distanceFentes)
print("Incertitude sur les distances entre les fentes (en nanom�tres):")
print(incertitudeDistanceFentes)
print("\nDistance entre deux fentes du r�seau de diffraction telles que " +
"donn�es par le \nconstructeur (en nanom�tres):")
print(distanceFentesTheorique)
print("Incertitude sur la distance entre deux fentes du r�seau de " + 
"diffraction \ndonn�e par le constructeur, correspondant � 500 fentes par " +
"pouce (en nanom�tres):")
print(incertitudeDistanceFentesTheorique)
print("\nLongueurs d'ondes des raies �mises par la lampe (du violet au " +
"rouge, en nanom�tres):")
print(longueurDOndeRaie)
print("Incertitude sur les longueurs d'onde des raies �mises par la lampe " +
"(du violet au \nrouge, en nanom�tres):")
print(incertitudeLongueurDOndeRaie)
print("\nAngle d'arr�te des prismes (le premier �tant le #54, le tout en " +
"radians):")
print(angleDArrete)
print("Incertitude sur l'angle d'arr�te des prismes (en radians):")
print(incertitudeAngleDArrete)
print("\nMinimums de d�viation pour chaque raie, en partant du violet au " + 
"jaune (les deux \nraies violettes sont sur la m�me ligne, la premi�re �tant " +
"la raie du prisme #54, \nle tout en radians):")
print(minimumDeviation)
print("Incertitude sur les minimums de d�viations (en radians):")
print(incertitudeMinimumDeviation)
print("\nIndices de r�fraction des raies diffract�s par les prismes (le " +
"premier prisme �tant le #54):")
print(indiceRefraction)
print("Incertitude sur les indices de r�fraction pour chaque raie, en " + 
"partant du violet \nau jaune (les deux raies violettes sont sur la m�me " +
"ligne, la premi�re �tant la \nraie du prisme #54):")
print(incertitudeIndiceRefraction)
print("\nValeurs des coefficients de Cauchy B et A des prismes selon " + 
"l'�quation de Cauchy \n(le prisme #54 en premier):")
print(coeffCauchy)
print("Incertitudes des coefficients de Cauchy B et A des prismes selon " +
"l'�quation de Cauchy \n(le prisme #54 en premier):")
print(incertitudeCoeffCauchy)
print("\nValeurs des indices de r�fraction pour une longueur d'onde de " +
"587.56 nm (prisme #54 \nen premier):")
print(indiceRefractionCauchy[0, :])
print("Incertitude des indices de r�fraction pour une longueur d'onde de " +
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
# On pr�sente les r�sultats � l'utilisateur