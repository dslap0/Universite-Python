# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trace la trajectoire en 2D de diff�rentes exoplan�tes autour
de leur �toile correspondante et effectue quelques v�rifications en trouvant
des r�sultats facilement pr�visibles."""

import numpy as np

import matplotlib.pyplot as plt

def positionExo(orbite, masseEtoile, temps):
    """Cette fonction renvoie la position en 2D d'une exoplan�te en
    orbite autour de son �toile si on lui fournit les param�tres de
    l'orbite qu'on cherche � calculer en agrument.
    orbite : Param�tres de l'orbite de l'exoplan�te (ndarray contenant,
    dans l'ordre, le demi-grand axe de l'orbite, son excentricit� et 
    son anomalie moyenne au d�but de son parcours)
    temps : Temps o� on veut mesurer la position (ndarray)
    masseEtoile : Masse de l'�toile de l'exoplan�te (int)
    """
    temps = np.atleast_1d(temps)
    # On transforme un temps qui aurait �t� entr� comme un scalaire en ndarray
    demiGrandAxe, excentricite, anomalieMoyenneDepart = orbite
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

        actifs[iActifs] = np.where(precision[iActifs] > 1e-12, True, False)

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
    # On trouve la position en x de l'exoplan�te aux temps recherch�s
    positionY0 = distanceEtoile * np.sin(anomalieVraie)
    # On trouve la position en y de l'exoplan�te aux temps recherch�s

    return positionX0, positionY0

plt.figure(0)
# On cr�e la premi�re figure

masseEtoile = 1
demiGrandAxe = 1
excentricite = [0, 0.5, 0.8]
anomalieMoyenneDepart = 0
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

for i in excentricite:
    orbite = np.array([demiGrandAxe, i, anomalieMoyenneDepart])
    # On d�finit les param�tres de d�part pour la courbe qu'on cherche � tracer

    positionX0, positionY0 = positionExo(orbite, masseEtoile, temps)
    # On trouve la position de l'exoplan�te pour tous les temps demand�s

    plt.plot(positionX0, positionY0, '-')
    plt.plot(positionX0[iTempsPointe], positionY0[iTempsPointe], '.')
    # On met les trac�s qu'on d�sire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ2-1.png')

plt.figure(1)
# On cr�e la deuxi�me figure

excentricite = 0.5
anomalieMoyenneDepart = [0, np.pi / 2, np.pi]
# On d�finit les param�tres qui changent entre les deux graphiques

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les param�tres esth�tiques du graphique

for i in anomalieMoyenneDepart:
    orbite = np.array([demiGrandAxe, excentricite, i])
    # On d�finit les param�tres de d�part pour la courbe qu'on cherche � tracer

    positionX0, positionY0 = positionExo(orbite, masseEtoile, temps)
    # On trouve la position de l'exoplan�te pour tous les temps demand�s

    plt.plot(positionX0, positionY0, '-')
    plt.plot(positionX0[iTempsPointe], positionY0[iTempsPointe], '.')
    # On met les trac�s qu'on d�sire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ2-2.png')

plt.figure(2)
# On cr�e la troisi�me figure

masseEtoile = [1, 0.25]
anomalieMoyenneDepart = 0
# On d�finit les param�tres qui changent entre les deux graphiques

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les param�tres esth�tiques du graphique

for i in masseEtoile:
    orbite = np.array([demiGrandAxe, excentricite, anomalieMoyenneDepart])
    # On d�finit les param�tres de d�part pour la courbe qu'on cherche � tracer

    positionX0, positionY0 = positionExo(orbite, i, temps)
    # On trouve la position de l'exoplan�te pour tous les temps demand�s

    plt.plot(positionX0, positionY0, '-')
    plt.plot(positionX0[iTempsPointe], positionY0[iTempsPointe], '.')
    # On met les trac�s qu'on d�sire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ2-3.png')

plt.show()