# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trouve les param�tres de l'orbite d'une exoplan�te si on lui
fournit la postion de celle-ci sur le plan du ciel et v�rifie s'il fonctionne
correctement."""

import numpy as np
from scipy.optimize import minimize

def projectionPositionExo(orbite, temps, masseEtoile):
    """Cette fonction renvoie la position en 3D d'une exoplan�te en
    orbite autour de son �toile si on lui fournit les param�tres de
    l'orbite qu'on cherche � calculer en agrument.
    orbite : Param�tres de l'orbite de l'exoplan�te (ndarray contenant,
    dans l'ordre, le demi-grand axe de l'orbite, son excentricit�, son
    anomalie moyenne au d�but de son parcours, la longitude du noeud 
    ascendant, l'inclinaison et l'argument du p�riastre)
    temps : Temps o� on veut mesurer la position (ndarray)
    masseEtoile : Masse de l'�toile de l'exoplan�te (int)
    """
    temps = np.atleast_1d(temps)
    # On transforme un temps qui aurait �t� entr� comme un scalaire en ndarray
    demiGrandAxe, excentricite, anomalieMoyenneDepart, longitudeNoeud, \
    inclinaison, argumentPeriastre = orbite
    # On d�balle les param�tres contenu dans le ndarray orbite

    periode = np.sqrt(demiGrandAxe ** 3 / masseEtoile)
    # On trouve la p�riode de l'orbite
    anomalieMoyenne = anomalieMoyenneDepart + 2 * np.pi * temps / periode
    # On trouve l'anomalie moyenne au temps recherch�

    anomalieExcentrique = np.where(anomalieMoyenne % (2 * np.pi) < np.pi,
anomalieMoyenne + excentricite / 2, anomalieMoyenne - excentricite / 2)
    # On trouve la valeur de d�part pour le calcul de l'anomalie excentrique

    precision = np.ones(anomalieExcentrique.size)
    # On s'assure de faire la premi�re it�ration

    actifs = np.ones(precision.size, dtype=bool)

    """On d�finit un ndarray qui tiendra le compte des anomalie excentriques
    ayant la pr�cision exig�e"""

    iActifs, = actifs.nonzero()

    """On d�finit un ndarray qui tiendra le compte des indices des anomalies
    excentriques qui manquent encore de pr�cision"""

    while iActifs.size != 0:

        """On continue les calculs jusqu'� ce qu'on aille la pr�cision voulue
        pour chaque valeur d'anomalie excentrique recherch�e"""

        dAnomalieExcentrique = -(anomalieMoyenne[iActifs] -
anomalieExcentrique[iActifs] + excentricite * 
np.sin(anomalieExcentrique[iActifs])) / (-1 + excentricite * 
np.cos(anomalieExcentrique[iActifs]))
        
        """On calcule dans un ndarray lee nouvelles diff�rences entre les
        valeurs d'anomalies excentriques en utilisant la m�thode de Newton,
        soit en �valuant le rapport entre la fonction dont on recherche le
        z�ro et sa d�riv�e au point calcul� pr�c�demment"""

        anomalieExcentrique[iActifs] += dAnomalieExcentrique
        # On modifie les anomalies excentriques qui ont besoin de l'�tre
        precision[iActifs] = abs(dAnomalieExcentrique)
        # On modifie la pr�cision des anomalies qu'on a nouvellement calcul�

        actifs = np.where(precision > 1e-6, True, False)

        """On met � jour quelles anomalies excentriques doivent �tre
        recalcul�es"""

        iActifs, = actifs.nonzero()

        """On met � jour les indices des anomalies excentriques qui manquent 
        encore de pr�cision"""

    distanceEtoile = demiGrandAxe * (1 - excentricite * 
np.cos(anomalieExcentrique))
    # On calcule la distance entre l'�toile et l'exoplan�te

    anomalieVraie = 2 * np.arctan2(np.sqrt(1 - excentricite) * 
np.cos(anomalieExcentrique / 2), np.sqrt(1 + excentricite) *
np.sin(anomalieExcentrique / 2))
    # On calcule l'anomalie vraie au temps recherch�

    positionX0 = distanceEtoile * np.cos(anomalieVraie)
    positionY0 = distanceEtoile * np.sin(anomalieVraie)
    # On trouve la position de l'�toile sur un r�f�rentiel 2D

    positionX = (np.cos(argumentPeriastre) * np.cos(longitudeNoeud) - 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.cos(longitudeNoeud) + 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en x de l'exoplan�te aux temps recherch�s
    positionY = (np.cos(argumentPeriastre) * np.sin(longitudeNoeud) - 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.sin(longitudeNoeud) + 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en y de l'exoplan�te aux temps recherch�s

    return positionX, positionY

def khi2Orbite(orbite, temps, masseEtoile, xExpermimental,
incertitudeXExperimental, yExperimental, incertitudeYExperimental):
    """La fonction calcule le khi-deux d'une orbite donn�e en argument.
    orbite : Param�tres de l'orbite de l'exoplan�te (ndarray contenant,
    dans l'ordre, le demi-grand axe de l'orbite, son excentricit�, son
    anomalie moyenne au d�but de son parcours, la longitude du noeud 
    ascendant, l'inclinaison et l'argument du p�riastre).
    temps : Temps o� on veut mesurer la position (ndarray)
    masseEtoile : Masse de l'�toile de l'exoplan�te (int)
    xExpermimental : Position en x de l'�toile sur le plan du ciel (ndarray)
    incertitudeXExperimental : incertitude sur les positions en x sur le
    plan du ciel (ndarray)
    yExperimental : Position en y de l'�toile sur le plan du ciel (ndarray)
    incertitudeYExperimental : incertitude sur les positions en y sur le
    plan du ciel (ndarray)
    """
    temps = np.atleast_1d(temps)
    # On transforme un temps qui aurait �t� entr� comme un scalaire en ndarray
    demiGrandAxe, excentricite, anomalieMoyenneDepart, longitudeNoeud, \
    inclinaison, argumentPeriastre = orbite
    # On d�balle les param�tres contenu dans le ndarray orbite

    periode = np.sqrt(demiGrandAxe ** 3 / masseEtoile)
    # On trouve la p�riode de l'orbite
    anomalieMoyenne = anomalieMoyenneDepart + 2 * np.pi * temps / periode
    # On trouve l'anomalie moyenne au temps recherch�

    anomalieExcentrique = np.where(anomalieMoyenne % (2 * np.pi) < np.pi,
anomalieMoyenne + excentricite / 2, anomalieMoyenne - excentricite / 2)
    # On trouve la valeur de d�part pour le calcul de l'anomalie excentrique

    precision = np.ones(anomalieExcentrique.size)
    # On s'assure de faire la premi�re it�ration

    actifs = np.ones(precision.size, dtype=bool)

    """On d�finit un ndarray qui tiendra le compte des anomalie excentriques
    ayant la pr�cision exig�e"""

    iActifs, = actifs.nonzero()

    """On d�finit un ndarray qui tiendra le compte des indices des anomalies
    excentriques qui manquent encore de pr�cision"""

    while iActifs.size != 0:

        """On continue les calculs jusqu'� ce qu'on aille la pr�cision voulue
        pour chaque valeur d'anomalie excentrique recherch�e"""

        dAnomalieExcentrique = -(anomalieMoyenne[iActifs] -
anomalieExcentrique[iActifs] + excentricite *
np.sin(anomalieExcentrique[iActifs])) / (-1 + excentricite * 
np.cos(anomalieExcentrique[iActifs]))
        
        """On calcule dans un ndarray lee nouvelles diff�rences entre les
        valeurs d'anomalies excentriques en utilisant la m�thode de Newton,
        soit en �valuant le rapport entre la fonction dont on recherche le
        z�ro et sa d�riv�e au point calcul� pr�c�demment"""

        anomalieExcentrique[iActifs] += dAnomalieExcentrique
        # On modifie les anomalies excentriques qui ont besoin de l'�tre
        precision[iActifs] = abs(dAnomalieExcentrique)
        # On modifie la pr�cision des anomalies qu'on a nouvellement calcul�

        actifs[iActifs] = np.where(precision[iActifs] > 1e-6, True, False)

        """On met � jour quelles anomalies excentriques doivent �tre
        recalcul�es"""

        iActifs, = actifs.nonzero()

        """On met � jour les indices des anomalies excentriques qui manquent 
        encore de pr�cision"""

    distanceEtoile = demiGrandAxe * (1 - excentricite * 
np.cos(anomalieExcentrique))
    # On calcule la distance entre l'�toile et l'exoplan�te

    anomalieVraie = 2 * np.arctan2(np.sqrt(1 - excentricite) * 
np.cos(anomalieExcentrique / 2), np.sqrt(1 + excentricite) *
np.sin(anomalieExcentrique / 2))
    # On calcule l'anomalie vraie au temps recherch�

    positionX0 = distanceEtoile * np.cos(anomalieVraie)
    positionY0 = distanceEtoile * np.sin(anomalieVraie)
    # On trouve la position de l'�toile sur un r�f�rentiel 2D

    positionX = (np.cos(argumentPeriastre) * np.cos(longitudeNoeud) - 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.cos(longitudeNoeud) + 
np.cos(inclinaison) * np.sin(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en x de l'exoplan�te aux temps recherch�s
    positionY = (np.cos(argumentPeriastre) * np.sin(longitudeNoeud) - 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.sin(argumentPeriastre)) * \
positionX0 - (np.sin(argumentPeriastre) * np.sin(longitudeNoeud) + 
np.cos(inclinaison) * np.cos(longitudeNoeud) * np.cos(argumentPeriastre)) * \
positionY0
    # On trouve la position en y de l'exoplan�te aux temps recherch�s

    khi2 = np.sum(((xExpermimental - positionX) / incertitudeXExperimental) **
2 + ((yExperimental - positionY) / incertitudeYExperimental) ** 2)
    # On trouve le khi-deux qu'on va ensuite tenter de r�duire

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
# On trouve la position de l'exoplan�te pour tous les temps demand�s

incertitudeXExperimental = 1e-6 * np.ones(temps.size)
incertitudeYExperimental = 1e-6 * np.ones(temps.size)
# On ne met des petites incertitudes sur ces r�sultats calcul�s

orbiteEstimee = np.array([demiGrandAxe + 0.1, excentricite + 0.1,
anomalieMoyenneDepart + 0.1, longitudeNoeud + 0.1, 
inclinaison + 0.1, argumentPeriastre + 0.001])
# On mets des valeurs l�g�rement fausses pour la minimisation du khi-deux

bornes = ((1e-6, 100), (0, 1 - 1e-6), (0, 2 * np.pi - 1e-6), (0, 2 * 
np.pi - 1e-6), (0, np.pi - 1e-6), (0, 2 * np.pi - 1e-6))
# On d�finit les bornes de validit� de chaque param�tre dans l'ordre

res = minimize(fun=khi2Orbite, x0=orbiteEstimee, args=(temps, masseEtoile, 
xExpermimental, incertitudeXExperimental, yExperimental,
incertitudeYExperimental), method='L-BFGS-B', bounds=bornes)
# On minimise le khi-deux de l'orbite

if res.success is True:
    
    """On affiche la valeur des param�tres estim�s si la minimisation a
    fonctionn�e"""

    print('La minimisation a r�ussie. Voici les param�tres de l\'orbite \
minimis�e et de la vraie orbite:')
    print(res.x)
    print(orbite)
else:
    # On affiche un message d'erreur si la minimisation a �chou�e
    print('La minimisation a �chou�e.')