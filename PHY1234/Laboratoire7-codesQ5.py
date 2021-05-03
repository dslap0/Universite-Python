# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trouve les paramètres de l'orbite d'une exoplanète donné dans
un document texte donné fournit la postion de celle-ci sur le plan du ciel."""

import numpy as np
from scipy.optimize import minimize

import matplotlib.pyplot as plt

def projectionPositionExo(orbite, temps, masseEtoile):
    """Cette fonction renvoie la position en 3D d'une exoplanète en
    orbite autour de son étoile si on lui fournit les paramètres de
    l'orbite qu'on cherche à calculer en agrument.
    orbite : Paramètres de l'orbite de l'exoplanète (ndarray contenant,
    dans l'ordre, le demi-grand axe de l'orbite, son excentricité, son
    anomalie moyenne au début de son parcours, la longitude du noeud 
    ascendant, l'inclinaison et l'argument du périastre)
    temps : Temps où on veut mesurer la position (ndarray)
    masseEtoile : Masse de l'étoile de l'exoplanète (int)
    """
    temps = np.atleast_1d(temps)
    # On transforme un temps qui aurait été entré comme un scalaire en ndarray
    demiGrandAxe, excentricite, anomalieMoyenneDepart, longitudeNoeud, \
    inclinaison, argumentPeriastre = orbite
    # On déballe les paramètres contenu dans le ndarray orbite

    periode = np.sqrt(demiGrandAxe ** 3 / masseEtoile)
    # On trouve la période de l'orbite
    anomalieMoyenne = anomalieMoyenneDepart + 2 * np.pi * temps / periode
    # On trouve l'anomalie moyenne au temps recherché

    anomalieExcentrique = np.where(anomalieMoyenne % (2 * np.pi) < np.pi,
anomalieMoyenne + excentricite / 2, anomalieMoyenne - excentricite / 2)
    # On trouve la valeur de départ pour le calcul de l'anomalie excentrique

    precision = np.ones(anomalieExcentrique.size)
    # On s'assure de faire la première itération

    actifs = np.ones(precision.size, dtype=bool)

    """On définit un ndarray qui tiendra le compte des anomalie excentriques
    ayant la précision exigée"""

    iActifs, = actifs.nonzero()

    """On définit un ndarray qui tiendra le compte des indices des anomalies
    excentriques qui manquent encore de précision"""

    while iActifs.size != 0:

        """On continue les calculs jusqu'à ce qu'on aille la précision voulue
        pour chaque valeur d'anomalie excentrique recherchée"""

        dAnomalieExcentrique = -(anomalieMoyenne[iActifs] -
anomalieExcentrique[iActifs] + excentricite * 
np.sin(anomalieExcentrique[iActifs])) / (-1 + excentricite * 
np.cos(anomalieExcentrique[iActifs]))
        
        """On calcule dans un ndarray lee nouvelles différences entre les
        valeurs d'anomalies excentriques en utilisant la méthode de Newton,
        soit en évaluant le rapport entre la fonction dont on recherche le
        zéro et sa dérivée au point calculé précédemment"""

        anomalieExcentrique[iActifs] += dAnomalieExcentrique
        # On modifie les anomalies excentriques qui ont besoin de l'être
        precision[iActifs] = abs(dAnomalieExcentrique)
        # On modifie la précision des anomalies qu'on a nouvellement calculé

        actifs = np.where(precision > 1e-6, True, False)

        """On met à jour quelles anomalies excentriques doivent être
        recalculées"""

        iActifs, = actifs.nonzero()

        """On met à jour les indices des anomalies excentriques qui manquent 
        encore de précision"""

    distanceEtoile = demiGrandAxe * (1 - excentricite * 
np.cos(anomalieExcentrique))
    # On calcule la distance entre l'étoile et l'exoplanète

    anomalieVraie = 2 * np.arctan2(np.sqrt(1 - excentricite) * 
np.cos(anomalieExcentrique / 2), np.sqrt(1 + excentricite) *
np.sin(anomalieExcentrique / 2))
    # On calcule l'anomalie vraie au temps recherché

    positionX0 = distanceEtoile * np.cos(anomalieVraie)
    positionY0 = distanceEtoile * np.sin(anomalieVraie)
    # On trouve la position de l'étoile sur un référentiel 2D

    positionX = (np.cos(argumentPeriastre) * np.cos(longitudeNoeud) - 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.cos(longitudeNoeud) + 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en x de l'exoplanète aux temps recherchés
    positionY = (np.cos(argumentPeriastre) * np.sin(longitudeNoeud) - 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.sin(longitudeNoeud) + 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en y de l'exoplanète aux temps recherchés

    return positionX, positionY

def khi2Orbite(orbite, temps, masseEtoile, xExpermimental,
incertitudeXExperimental, yExperimental, incertitudeYExperimental):
    """La fonction calcule le khi-deux d'une orbite donnée en argument.
    orbite : Paramètres de l'orbite de l'exoplanète (ndarray contenant,
    dans l'ordre, le demi-grand axe de l'orbite, son excentricité, son
    anomalie moyenne au début de son parcours, la longitude du noeud 
    ascendant, l'inclinaison et l'argument du périastre).
    temps : Temps où on veut mesurer la position (ndarray)
    masseEtoile : Masse de l'étoile de l'exoplanète (int)
    xExpermimental : Position en x de l'étoile sur le plan du ciel (ndarray)
    incertitudeXExperimental : incertitude sur les positions en x sur le
    plan du ciel (ndarray)
    yExperimental : Position en y de l'étoile sur le plan du ciel (ndarray)
    incertitudeYExperimental : incertitude sur les positions en y sur le
    plan du ciel (ndarray)
    """
    temps = np.atleast_1d(temps)
    # On transforme un temps qui aurait été entré comme un scalaire en ndarray
    demiGrandAxe, excentricite, anomalieMoyenneDepart, longitudeNoeud, \
    inclinaison, argumentPeriastre = orbite
    # On déballe les paramètres contenu dans le ndarray orbite

    periode = np.sqrt(demiGrandAxe ** 3 / masseEtoile)
    # On trouve la période de l'orbite
    anomalieMoyenne = anomalieMoyenneDepart + 2 * np.pi * temps / periode
    # On trouve l'anomalie moyenne au temps recherché

    anomalieExcentrique = np.where(anomalieMoyenne % (2 * np.pi) < np.pi,
anomalieMoyenne + excentricite / 2, anomalieMoyenne - excentricite / 2)
    # On trouve la valeur de départ pour le calcul de l'anomalie excentrique

    precision = np.ones(anomalieExcentrique.size)
    # On s'assure de faire la première itération

    actifs = np.ones(precision.size, dtype=bool)

    """On définit un ndarray qui tiendra le compte des anomalie excentriques
    ayant la précision exigée"""

    iActifs, = actifs.nonzero()

    """On définit un ndarray qui tiendra le compte des indices des anomalies
    excentriques qui manquent encore de précision"""

    i = 0
    # On initialise le compteur d'itérations

    while (iActifs.size != 0) and (i < 1000):

        """On continue les calculs jusqu'à ce qu'on aille la précision voulue
        pour chaque valeur d'anomalie excentrique recherchée"""

        dAnomalieExcentrique = -(anomalieMoyenne[iActifs] -
anomalieExcentrique[iActifs] + excentricite *
np.sin(anomalieExcentrique[iActifs])) / (-1 + excentricite * 
np.cos(anomalieExcentrique[iActifs]))
        
        """On calcule dans un ndarray lee nouvelles différences entre les
        valeurs d'anomalies excentriques en utilisant la méthode de Newton,
        soit en évaluant le rapport entre la fonction dont on recherche le
        zéro et sa dérivée au point calculé précédemment"""

        anomalieExcentrique[iActifs] += dAnomalieExcentrique
        # On modifie les anomalies excentriques qui ont besoin de l'être
        precision[iActifs] = abs(dAnomalieExcentrique)
        # On modifie la précision des anomalies qu'on a nouvellement calculé

        actifs[iActifs] = np.where(precision[iActifs] > 1e-6, True, False)

        """On met à jour quelles anomalies excentriques doivent être
        recalculées"""

        iActifs, = actifs.nonzero()

        """On met à jour les indices des anomalies excentriques qui manquent 
        encore de précision"""

        i += 1

    distanceEtoile = demiGrandAxe * (1 - excentricite * 
np.cos(anomalieExcentrique))
    # On calcule la distance entre l'étoile et l'exoplanète

    anomalieVraie = 2 * np.arctan2(np.sqrt(1 - excentricite) * 
np.cos(anomalieExcentrique / 2), np.sqrt(1 + excentricite) *
np.sin(anomalieExcentrique / 2))
    # On calcule l'anomalie vraie au temps recherché

    positionX0 = distanceEtoile * np.cos(anomalieVraie)
    positionY0 = distanceEtoile * np.sin(anomalieVraie)
    # On trouve la position de l'étoile sur un référentiel 2D

    positionX = (np.cos(argumentPeriastre) * np.cos(longitudeNoeud) - 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.cos(longitudeNoeud) + 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en x de l'exoplanète aux temps recherchés
    positionY = (np.cos(argumentPeriastre) * np.sin(longitudeNoeud) - 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.sin(longitudeNoeud) + 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en y de l'exoplanète aux temps recherchés

    khi2 = np.sum(((xExpermimental - positionX) / incertitudeXExperimental) **
2 + ((yExperimental - positionY) / incertitudeYExperimental) ** 2)

    return khi2

temps, xExpermimental, incertitudeXExperimental, yExperimental, \
incertitudeYExperimental = np.loadtxt('mesuresOrbite.txt', unpack=True)
masseEtoile = 0.9
# On définit les arguments non-variables à partir du fichier

demiGrandAxe = 100 * np.random.rand(100)
excentricite = np.random.rand(100)
anomalieMoyenneDepart = 2 * np.pi * np.random.rand(100)
longitudeNoeud = 2 * np.pi * np.random.rand(100)
inclinaison = np.pi * np.random.rand(100)
argumentPeriastre = 2 * np.pi * np.random.rand(100)
# On définit des arrays pour les orbites de départ

bornes = ((1e-6, 100), (0, 1 - 1e-6), (0, 2 * np.pi - 1e-6), (0, 2 * 
np.pi - 1e-6), (0, np.pi - 1e-6), (0, 2 * np.pi - 1e-6))
# On définit les bornes de validité de chaque paramètre dans l'ordre

minimisee = 1e12
# On s'assure de prendre des valeurs optimisées

i = 0
# On met le compteur à zéro

while i < len(demiGrandAxe):
    orbiteEstimee = np.array([demiGrandAxe[i], excentricite[i],
anomalieMoyenneDepart[i], longitudeNoeud[i], inclinaison[i],
argumentPeriastre[i]])
    # On permet à l'orbite estimée de parcourir toutes les valeurs données

    res = minimize(khi2Orbite, orbiteEstimee, args=(temps,
masseEtoile, xExpermimental, incertitudeXExperimental, yExperimental,
incertitudeYExperimental), method='L-BFGS-B', bounds=bornes)
    # On minimise le khi-deux de l'orbite
    if res.success is True:
        if res.fun < minimisee:

            """On change la valeur du meilleur résultat seulement si la
            minimisation est meilleure"""

            meilleurRes = res
            minimisee = meilleurRes.fun

    i += 1

orbiteEstimee = meilleurRes.x
# On redéfinit la nouvelle estimation de base pour le prochain test

demiGrandAxe, excentricite, anomalieMoyenneDepart, longitudeNoeud, \
inclinaison, argumentPeriastre = orbiteEstimee
# On déballe les paramètres contenu dans le ndarray des paramètres estimés

demiGrandAxe += np.random.normal(0, size=1000)
excentricite += np.random.normal(0, size=1000)
anomalieMoyenneDepart += np.random.normal(0, size=1000)
longitudeNoeud += np.random.normal(0, size=1000)
inclinaison += np.random.normal(0, size=1000)
argumentPeriastre += np.random.normal(0, size=1000)
# On fait des légères variations sur chaque paramètres

while i < len(demiGrandAxe):
    orbiteEstimee = np.array([demiGrandAxe[i], excentricite[i],
anomalieMoyenneDepart[i], longitudeNoeud[i], inclinaison[i],
argumentPeriastre[i]])
    # On permet à l'orbite estimée de parcourir toutes les valeurs données

    res = minimize(khi2Orbite, orbiteEstimee, args=(temps,
masseEtoile, xExpermimental, incertitudeXExperimental, yExperimental,
incertitudeYExperimental), method='L-BFGS-B', bounds=bornes)
    # On minimise le khi-deux de l'orbite
    if res.success is True:
        if res.fun < minimisee:

            """On change la valeur du meilleur résultat seulement si la
            minimisation est meilleure"""

            meilleurRes = res
            minimisee = meilleurRes.fun

    i += 1

orbite = meilleurRes.x
# On définit les paramètres de l'orbite de la courbe

print('Voici les paramètres de l\'orbite représentant la situation: \n' + \
str(orbite))

plt.figure(0)

plt.plot(xExpermimental, yExperimental, '.')
plt.errorbar(xExpermimental, yExperimental, xerr=incertitudeXExperimental,
yerr=incertitudeYExperimental, ls='None')
# On trace les valeurs expériementales et leurs barres d'incertitudes

positionX, positionY = projectionPositionExo(orbite, temps, masseEtoile)
# On trouve les valeurs prédites au même moment par le modèle

plt.plot(positionX, positionY, '*')
# On trace l'orbite de l'exoplanète

plt.xlabel('Position en x (en UA)')
plt.ylabel('Position en y (en UA)')
# On change les paramètres esthétiques

plt.savefig('Laboratoire7-figureQ5-1.png')

plt.figure(1)

temps = np.linspace(0, 1, 1001)
iTempsPointe = np.arange(0, 1001, 100)
# On définit un ndarray avec les indices de temps où on doit ajouter un point

positionX, positionY = projectionPositionExo(orbite, temps, masseEtoile)
# On trouve toutes les positions possibles de l'exoplanète sur son orbite

plt.plot(positionX, positionY, '-')
# On trace l'orbite de l'exoplanète

plt.plot(positionX[iTempsPointe], positionY[iTempsPointe], '.')
# On trace les points à chaque 0.1 années

plt.xlabel('Position en x (en UA)')
plt.ylabel('Position en y (en UA)')
# On change les paramètres esthétiques

plt.savefig('Laboratoire7-figureQ5-2.png')

plt.show()