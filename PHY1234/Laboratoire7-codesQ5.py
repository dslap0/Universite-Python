# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trouve les param�tres de l'orbite d'une exoplan�te donn� dans
un document texte donn� fournit la postion de celle-ci sur le plan du ciel."""

import numpy as np
from scipy.optimize import minimize

import matplotlib.pyplot as plt

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

    i = 0
    # On initialise le compteur d'it�rations

    while (iActifs.size != 0) and (i < 1000):

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

        i += 1

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

    return khi2

temps, xExpermimental, incertitudeXExperimental, yExperimental, \
incertitudeYExperimental = np.loadtxt('mesuresOrbite.txt', unpack=True)
masseEtoile = 0.9
# On d�finit les arguments non-variables � partir du fichier

demiGrandAxe = 100 * np.random.rand(100)
excentricite = np.random.rand(100)
anomalieMoyenneDepart = 2 * np.pi * np.random.rand(100)
longitudeNoeud = 2 * np.pi * np.random.rand(100)
inclinaison = np.pi * np.random.rand(100)
argumentPeriastre = 2 * np.pi * np.random.rand(100)
# On d�finit des arrays pour les orbites de d�part

bornes = ((1e-6, 100), (0, 1 - 1e-6), (0, 2 * np.pi - 1e-6), (0, 2 * 
np.pi - 1e-6), (0, np.pi - 1e-6), (0, 2 * np.pi - 1e-6))
# On d�finit les bornes de validit� de chaque param�tre dans l'ordre

minimisee = 1e12
# On s'assure de prendre des valeurs optimis�es

i = 0
# On met le compteur � z�ro

while i < len(demiGrandAxe):
    orbiteEstimee = np.array([demiGrandAxe[i], excentricite[i],
anomalieMoyenneDepart[i], longitudeNoeud[i], inclinaison[i],
argumentPeriastre[i]])
    # On permet � l'orbite estim�e de parcourir toutes les valeurs donn�es

    res = minimize(khi2Orbite, orbiteEstimee, args=(temps,
masseEtoile, xExpermimental, incertitudeXExperimental, yExperimental,
incertitudeYExperimental), method='L-BFGS-B', bounds=bornes)
    # On minimise le khi-deux de l'orbite
    if res.success is True:
        if res.fun < minimisee:

            """On change la valeur du meilleur r�sultat seulement si la
            minimisation est meilleure"""

            meilleurRes = res
            minimisee = meilleurRes.fun

    i += 1

orbiteEstimee = meilleurRes.x
# On red�finit la nouvelle estimation de base pour le prochain test

demiGrandAxe, excentricite, anomalieMoyenneDepart, longitudeNoeud, \
inclinaison, argumentPeriastre = orbiteEstimee
# On d�balle les param�tres contenu dans le ndarray des param�tres estim�s

demiGrandAxe += np.random.normal(0, size=1000)
excentricite += np.random.normal(0, size=1000)
anomalieMoyenneDepart += np.random.normal(0, size=1000)
longitudeNoeud += np.random.normal(0, size=1000)
inclinaison += np.random.normal(0, size=1000)
argumentPeriastre += np.random.normal(0, size=1000)
# On fait des l�g�res variations sur chaque param�tres

while i < len(demiGrandAxe):
    orbiteEstimee = np.array([demiGrandAxe[i], excentricite[i],
anomalieMoyenneDepart[i], longitudeNoeud[i], inclinaison[i],
argumentPeriastre[i]])
    # On permet � l'orbite estim�e de parcourir toutes les valeurs donn�es

    res = minimize(khi2Orbite, orbiteEstimee, args=(temps,
masseEtoile, xExpermimental, incertitudeXExperimental, yExperimental,
incertitudeYExperimental), method='L-BFGS-B', bounds=bornes)
    # On minimise le khi-deux de l'orbite
    if res.success is True:
        if res.fun < minimisee:

            """On change la valeur du meilleur r�sultat seulement si la
            minimisation est meilleure"""

            meilleurRes = res
            minimisee = meilleurRes.fun

    i += 1

orbite = meilleurRes.x
# On d�finit les param�tres de l'orbite de la courbe

print('Voici les param�tres de l\'orbite repr�sentant la situation: \n' + \
str(orbite))

plt.figure(0)

plt.plot(xExpermimental, yExperimental, '.')
plt.errorbar(xExpermimental, yExperimental, xerr=incertitudeXExperimental,
yerr=incertitudeYExperimental, ls='None')
# On trace les valeurs exp�riementales et leurs barres d'incertitudes

positionX, positionY = projectionPositionExo(orbite, temps, masseEtoile)
# On trouve les valeurs pr�dites au m�me moment par le mod�le

plt.plot(positionX, positionY, '*')
# On trace l'orbite de l'exoplan�te

plt.xlabel('Position en x (en UA)')
plt.ylabel('Position en y (en UA)')
# On change les param�tres esth�tiques

plt.savefig('Laboratoire7-figureQ5-1.png')

plt.figure(1)

temps = np.linspace(0, 1, 1001)
iTempsPointe = np.arange(0, 1001, 100)
# On d�finit un ndarray avec les indices de temps o� on doit ajouter un point

positionX, positionY = projectionPositionExo(orbite, temps, masseEtoile)
# On trouve toutes les positions possibles de l'exoplan�te sur son orbite

plt.plot(positionX, positionY, '-')
# On trace l'orbite de l'exoplan�te

plt.plot(positionX[iTempsPointe], positionY[iTempsPointe], '.')
# On trace les points � chaque 0.1 ann�es

plt.xlabel('Position en x (en UA)')
plt.ylabel('Position en y (en UA)')
# On change les param�tres esth�tiques

plt.savefig('Laboratoire7-figureQ5-2.png')

plt.show()