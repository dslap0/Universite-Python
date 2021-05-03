# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trace la projection en 2D de la trajectoire en 3D de 
diff�rentes exoplan�tes autour de leur �toile correspondante et effectue
quelques v�rifications en trouvant des r�sultats facilement pr�visibles."""

import numpy as np

import matplotlib.pyplot as plt

def projectionPositionExo(orbite, masseEtoile, temps):
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

    return positionX, positionY

plt.figure(0)

masseEtoile = 1
demiGrandAxe = 1
anomalieMoyenneDepart = 0
excentricite = 0
longitudeNoeud = 0
inclinaison = [0, np.pi / 2]
argumentPeriastre = 0
temps = np.linspace(0, 1, 1001)
# On d�finit les param�tres de d�part
iTempsPointe = np.arange(0, 1001, 100)
# On d�finit un ndarray avec les indices de temps o� on doit ajouter un point

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les param�tres esth�tiques du graphique

for i in inclinaison:
    orbite = np.array([demiGrandAxe, excentricite, anomalieMoyenneDepart,
longitudeNoeud, i, argumentPeriastre])

    positionX, positionY = projectionPositionExo(orbite, masseEtoile, temps)
    # On trouve la position de l'exoplan�te pour tous les temps demand�s

    plt.plot(positionX, positionY, '-')
    plt.plot(positionX[iTempsPointe], positionY[iTempsPointe], '.')
    # On met les trac�s qu'on d�sire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ3-1.png')

plt.figure(1)

excentricite = 0.5
longitudeNoeud = [0, np.pi / 2, np.pi * 3 / 2]
inclinaison = 0
# On d�finit les param�tres qui changent entre les deux graphiques

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les param�tres esth�tiques du graphique

for i in longitudeNoeud:
    orbite = np.array([demiGrandAxe, excentricite, anomalieMoyenneDepart, i,
inclinaison, argumentPeriastre])

    positionX, positionY = projectionPositionExo(orbite, masseEtoile, temps)
    # On trouve la position de l'exoplan�te pour tous les temps demand�s

    plt.plot(positionX, positionY, '-')
    plt.plot(positionX[iTempsPointe], positionY[iTempsPointe], '.')
    # On met les trac�s qu'on d�sire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ3-2.png')

plt.figure(2)

longitudeNoeud = 0
inclinaison = 0
argumentPeriastre = [0, np.pi / 2, np.pi * 3 / 2]
# On d�finit les param�tres qui changent entre les deux graphiques

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les param�tres esth�tiques du graphique

for i in argumentPeriastre:
    orbite = np.array([demiGrandAxe, excentricite, anomalieMoyenneDepart,
longitudeNoeud, inclinaison, i])

    positionX, positionY = projectionPositionExo(orbite, masseEtoile, temps)
    # On trouve la position de l'exoplan�te pour tous les temps demand�s

    plt.plot(positionX, positionY, '-')
    plt.plot(positionX[iTempsPointe], positionY[iTempsPointe], '.')
    # On met les trac�s qu'on d�sire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ3-3.png')

plt.show()