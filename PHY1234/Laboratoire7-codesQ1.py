# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme v�rfie la validit� des anomalies excentriques trouv�s par la
focntion calculAnomalieExcentrique avec un test de validation."""

import numpy as np

import matplotlib.pyplot as plt

def calculAnomalieExcentrique(anomalieMoyenne, excentricite,
precisionDemandee):
    """Cette fonction vise � trouver l'anomalie excentrique de l'orbite
    d'une exoplan�te dont les param�tres orbitaux sont donn�s.
    anomalieMoyenne : fraction de la p�riode orbitale �coul�e depuis le
    passage au p�riastre (float en rad).
    excentricite : indique l'aplatissement de l'ellipse de l'exoplan�te
    (float).
    precision : pr�cision demand�e au programme (float).
    """
    anomalieMoyenne = np.atleast_1d(anomalieMoyenne)
    # On transforme l'anomalie moyenne en ndarray si elle ne l'�tait pas d�j�

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
        
        actifs[iActifs] = np.where(precision[iActifs] > precisionDemandee, True, False)
        
        """On met � jour quelles anomalies excentriques doivent �tre
        recalcul�es"""
        
        iActifs, = actifs.nonzero()
        
        """On met � jour les indices des anomalies excentriques qui manquent 
        encore de pr�cision"""

    return anomalieExcentrique

anomalieMoyenne = np.linspace(0, 2 * np.pi - 1e-9, 10000)
excentricite = np.linspace(0, 1 - 1e-9, 6)
precisionDemandee = 1e-12

"""On d�finit des valeurs dans l'intervalle de validit� des param�tres pour
nos tests"""

anomalieExcentrique = np.array([])

"""On d�finit le array dans lequel on va venir placer les valeurs d'anomalies
excentriques"""

for i in excentricite:
        
    """On calcule la valeur de l'anomalie excentrique pour chaque anomalie
    moyenne et pour chaque excentricit� correspondante"""
    
    anomalieExcentrique = calculAnomalieExcentrique(anomalieMoyenne,
i, precisionDemandee)
    
    plt.plot(anomalieMoyenne, anomalieExcentrique, '-')
    # On trace le graphique de la variation de l'anomalie excentrique

plt.xlabel('Anomalie moyenne (en rad)')
plt.ylabel('Anomalie excentrique (en rad)')
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire7-figureQ1.png')
plt.show()