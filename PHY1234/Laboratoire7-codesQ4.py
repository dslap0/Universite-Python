# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trouve les paramètres de l'orbite d'une exoplanète si on lui
fournit la postion de celle-ci sur le plan du ciel et vérifie s'il fonctionne
correctement."""

import numpy as np
from scipy.optimize import minimize

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

        actifs[iActifs] = np.where(precision[iActifs] > 1e-6, True, False)

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

    khi2 = np.sum(((xExpermimental - positionX) / incertitudeXExperimental) **
2 + ((yExperimental - positionY) / incertitudeYExperimental) ** 2)
    # On trouve le khi-deux qu'on va ensuite tenter de réduire

    return khi2

masseEtoile = 1
demiGrandAxe = 1
anomalieMoyenneDepart = 0.4
excentricite = 0.3
longitudeNoeud = 0.2
inclinaison = 0.1
argumentPeriastre = 0.1
temps = np.linspace(0, 1 - 1e-6, 12)

orbite = np.array([demiGrandAxe, excentricite, anomalieMoyenneDepart, 
longitudeNoeud, inclinaison, argumentPeriastre])

xExpermimental, yExperimental = projectionPositionExo(orbite, temps, 
masseEtoile)
# On trouve la position de l'exoplanète pour tous les temps demandés

incertitudeXExperimental = 1e-6 * np.ones(temps.size)
incertitudeYExperimental = 1e-6 * np.ones(temps.size)
# On ne met des petites incertitudes sur ces résultats calculés

orbiteEstimee = np.array([demiGrandAxe + 0.1, excentricite + 0.1,
anomalieMoyenneDepart + 0.1, longitudeNoeud + 0.1, 
inclinaison + 0.1, argumentPeriastre + 0.001])
# On mets des valeurs légèrement fausses pour la minimisation du khi-deux

bornes = ((1e-6, 100), (0, 1 - 1e-6), (0, 2 * np.pi - 1e-6), (0, 2 * 
np.pi - 1e-6), (0, np.pi - 1e-6), (0, 2 * np.pi - 1e-6))
# On définit les bornes de validité de chaque paramètre dans l'ordre

res = minimize(fun=khi2Orbite, x0=orbiteEstimee, args=(temps, masseEtoile, 
xExpermimental, incertitudeXExperimental, yExperimental,
incertitudeYExperimental), method='L-BFGS-B', bounds=bornes)
# On minimise le khi-deux de l'orbite

if res.success is True:
    
    """On affiche la valeur des paramètres estimés si la minimisation a
    fonctionnée"""

    print('La minimisation a réussie. Voici les paramètres de l\'orbite \
minimisée et de la vraie orbite:')
    print(res.x)
    print(orbite)
else:
    # On affiche un message d'erreur si la minimisation a échouée
    print('La minimisation a échouée.')