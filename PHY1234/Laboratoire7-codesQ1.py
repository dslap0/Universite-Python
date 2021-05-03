# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme vérfie la validité des anomalies excentriques trouvés par la
focntion calculAnomalieExcentrique avec un test de validation."""

import numpy as np

import matplotlib.pyplot as plt

def calculAnomalieExcentrique(anomalieMoyenne, excentricite,
precisionDemandee):
    """Cette fonction vise à trouver l'anomalie excentrique de l'orbite
    d'une exoplanète dont les paramètres orbitaux sont donnés.
    anomalieMoyenne : fraction de la période orbitale écoulée depuis le
    passage au périastre (float en rad).
    excentricite : indique l'aplatissement de l'ellipse de l'exoplanète
    (float).
    precision : précision demandée au programme (float).
    """
    anomalieMoyenne = np.atleast_1d(anomalieMoyenne)
    # On transforme l'anomalie moyenne en ndarray si elle ne l'était pas déjà

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
        
        actifs[iActifs] = np.where(precision[iActifs] > precisionDemandee, True, False)
        
        """On met à jour quelles anomalies excentriques doivent être
        recalculées"""
        
        iActifs, = actifs.nonzero()
        
        """On met à jour les indices des anomalies excentriques qui manquent 
        encore de précision"""

    return anomalieExcentrique

anomalieMoyenne = np.linspace(0, 2 * np.pi - 1e-9, 10000)
excentricite = np.linspace(0, 1 - 1e-9, 6)
precisionDemandee = 1e-12

"""On définit des valeurs dans l'intervalle de validité des paramètres pour
nos tests"""

anomalieExcentrique = np.array([])

"""On définit le array dans lequel on va venir placer les valeurs d'anomalies
excentriques"""

for i in excentricite:
        
    """On calcule la valeur de l'anomalie excentrique pour chaque anomalie
    moyenne et pour chaque excentricité correspondante"""
    
    anomalieExcentrique = calculAnomalieExcentrique(anomalieMoyenne,
i, precisionDemandee)
    
    plt.plot(anomalieMoyenne, anomalieExcentrique, '-')
    # On trace le graphique de la variation de l'anomalie excentrique

plt.xlabel('Anomalie moyenne (en rad)')
plt.ylabel('Anomalie excentrique (en rad)')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire7-figureQ1.png')
plt.show()