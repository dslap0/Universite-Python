# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme trace la trajectoire en 2D de différentes exoplanètes autour
de leur étoile correspondante et effectue quelques vérifications en trouvant
des résultats facilement prévisibles."""

import numpy as np

import matplotlib.pyplot as plt

def positionExo(orbite, masseEtoile, temps):
    """Cette fonction renvoie la position en 2D d'une exoplanète en
    orbite autour de son étoile si on lui fournit les paramètres de
    l'orbite qu'on cherche à calculer en agrument.
    orbite : Paramètres de l'orbite de l'exoplanète (ndarray contenant,
    dans l'ordre, le demi-grand axe de l'orbite, son excentricité et 
    son anomalie moyenne au début de son parcours)
    temps : Temps où on veut mesurer la position (ndarray)
    masseEtoile : Masse de l'étoile de l'exoplanète (int)
    """
    temps = np.atleast_1d(temps)
    # On transforme un temps qui aurait été entré comme un scalaire en ndarray
    demiGrandAxe, excentricite, anomalieMoyenneDepart = orbite
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

        actifs[iActifs] = np.where(precision[iActifs] > 1e-12, True, False)

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
    # On trouve la position en x de l'exoplanète aux temps recherchés
    positionY0 = distanceEtoile * np.sin(anomalieVraie)
    # On trouve la position en y de l'exoplanète aux temps recherchés

    return positionX0, positionY0

plt.figure(0)
# On crée la première figure

masseEtoile = 1
demiGrandAxe = 1
excentricite = [0, 0.5, 0.8]
anomalieMoyenneDepart = 0
temps = np.linspace(0, 1, 1001)
# On définit les paramètres de départ
iTempsPointe = np.arange(0, 1001, 100)
# On définit un ndarray avec les indices de temps où on doit ajouter un point

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les paramètres esthétiques du graphique

for i in excentricite:
    orbite = np.array([demiGrandAxe, i, anomalieMoyenneDepart])
    # On définit les paramètres de départ pour la courbe qu'on cherche à tracer

    positionX0, positionY0 = positionExo(orbite, masseEtoile, temps)
    # On trouve la position de l'exoplanète pour tous les temps demandés

    plt.plot(positionX0, positionY0, '-')
    plt.plot(positionX0[iTempsPointe], positionY0[iTempsPointe], '.')
    # On met les tracés qu'on désire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ2-1.png')

plt.figure(1)
# On crée la deuxième figure

excentricite = 0.5
anomalieMoyenneDepart = [0, np.pi / 2, np.pi]
# On définit les paramètres qui changent entre les deux graphiques

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les paramètres esthétiques du graphique

for i in anomalieMoyenneDepart:
    orbite = np.array([demiGrandAxe, excentricite, i])
    # On définit les paramètres de départ pour la courbe qu'on cherche à tracer

    positionX0, positionY0 = positionExo(orbite, masseEtoile, temps)
    # On trouve la position de l'exoplanète pour tous les temps demandés

    plt.plot(positionX0, positionY0, '-')
    plt.plot(positionX0[iTempsPointe], positionY0[iTempsPointe], '.')
    # On met les tracés qu'on désire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ2-2.png')

plt.figure(2)
# On crée la troisième figure

masseEtoile = [1, 0.25]
anomalieMoyenneDepart = 0
# On définit les paramètres qui changent entre les deux graphiques

plt.axhline(ls='dotted')
plt.axvline(ls='dotted')
plt.xlabel('Position en x (UA)')
plt.ylabel('Position en y (UA)')
plt.axis('equal')
# On ajuste les paramètres esthétiques du graphique

for i in masseEtoile:
    orbite = np.array([demiGrandAxe, excentricite, anomalieMoyenneDepart])
    # On définit les paramètres de départ pour la courbe qu'on cherche à tracer

    positionX0, positionY0 = positionExo(orbite, i, temps)
    # On trouve la position de l'exoplanète pour tous les temps demandés

    plt.plot(positionX0, positionY0, '-')
    plt.plot(positionX0[iTempsPointe], positionY0[iTempsPointe], '.')
    # On met les tracés qu'on désire sur le graphique pour la courbe actuelle

plt.savefig('Laboratoire7-figureQ2-3.png')

plt.show()