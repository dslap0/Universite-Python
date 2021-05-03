# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule la trajectoire de neutrons ayant été lancés à
travers une plaque solide amorphe selon certains paramètres de départ.
Le programme transmet ensuite la proportion de ces neutrons ayant été
émis, la proportion des neutrons ayant été réfléchis et la proportion
de ceux qui ont été absorbés. Il trace ensuite un graphique de la 
variation de ces proportions par rapport à la probabilité qu'un noyau
rencontré disperse le neutron qui interagit avec lui."""

import numpy as np

import matplotlib.pyplot as plt

def etatNeutrons(pAbsorption, pDispersion, libreParcoursMoyen, epaisseur,
nombreNeutrons):
    """Cette fonction calcule la trajectoire de neutrons ayant été
    lancés à travers une plaque solide amorphe selon certains 
    paramètres de départ et transmet ensuite les proportions de 
    neutrons ayant été émis, réfléchis et absorbés.

    pAbsorption : Probabilité d'absorption du neutron par un atome.
    pDispersion : Probabilité de dispertion du neutron par un atome.
    libreParcoursMoyen : Distance moyenne parcourue en ligne droite 
    avant d'intéragir avec un noyau.
    epaisseur : Épaisseur de la plaque solide amorphe
    nombreNeutrons : Nombre de neutrons dont il faut calculer la
    trajectoire.
    """
    if pDispersion + pAbsorption > 1:
        print('Erreur, la probabilité que le neutron soit absorbé ou \
dispersé est supérieure\nà 100%. Veuillez réessayer.')
        return None, None, None

    absorbes, transmis, reflechis, = 0, 0, 0
    # On mets les compteurs à 0

    while absorbes + transmis + reflechis < nombreNeutrons:
        positionX, direction = 0, 1
        
        """On définit la position horizontale et la direction du neutron au
        lancement (donnée par le cosinus de l'angle entre sa trajectoire et
        l'axe des x puisqu'on ne s'intéresse qu'à sa position en x)"""
        
        while True:
            
            """La boucle est incassable, on doit donc satisfaire un des test
            if (ou elif) pour en sortir"""

            positionX += np.random.exponential(libreParcoursMoyen) * direction
            
            """ On trouve la distance parcourue en X avant une possible 
            interaction"""

            if positionX < 0:
                reflechis += 1
                break
            # On fait le test de réflexion
            elif positionX > epaisseur:
                transmis += 1
                break
            # On fait le test de transmission

            rdm = np.random.random()
            # On pige un nombre au hasard entre 0 et 1

            if rdm < pAbsorption:
                absorbes += 1
                break
            # On fait le test d'absorption
            elif rdm < pAbsorption + pDispersion:
                direction = 1 - 2 * np.random.random()
            # On calcule le nouvel angle si le neutron est dipersé par l'atome

    proportionAbsorbes = absorbes / nombreNeutrons
    proportionTransmis = transmis / nombreNeutrons
    proportionReflechis = reflechis / nombreNeutrons
    # On trouve les proportions de neutrons absorbés, transmis et réfléchis

    return proportionAbsorbes, proportionTransmis, proportionReflechis

def incertitudeGaussienne(quantite, repetition):
    """Cette fonction trouve l'incertitude sur une quantité obéissant à
    une distribution Gaussienne.

    quantite : Quantité dont il faut calculer l'incertitude, de type ndarray.
    repetition : Nombre de répétitions de l'expérience.
    """
    incertitude = np.sqrt(quantite * (1 - quantite) / (repetition - 1))

    return incertitude

pAbsorption = 0.2
pDispersion = np.arange(0, 1 - pAbsorption, 0.1)
epaisseur = 1
libreParcoursMoyen = 0.2
nombreNeutrons = 10000
# On définit les conditions de départ

proportions = []
# On définit une liste vide où on va placer les résultats

for element in pDispersion:
    proportions.extend(etatNeutrons(pAbsorption, element, libreParcoursMoyen,
epaisseur, nombreNeutrons))
# On place les résultats dans la nouvelle liste

A, T, R = [], [], []
# On définit les listes qui trieront les résultats

i = 0
# On remet le compteur à 0

while i < len(proportions):
    if i % 3 == 0:
        A.append(proportions[i])
    elif i % 3 == 1:
        T.append(proportions[i])
    else:
        R.append(proportions[i])
    i += 1
# On assigne les résultats obtenus aux listes correspondantes

A = np.array(A)
T = np.array(T)
R = np.array(R)

"""On transforme les résultats en ndarray pour effectuer le calcul 
d'incertitude"""

incertitudeA = incertitudeGaussienne(A, nombreNeutrons)
incertitudeT = incertitudeGaussienne(T, nombreNeutrons)
incertitudeR = incertitudeGaussienne(R, nombreNeutrons)
# On calcule les différentes incertitudes sur les résultats obtenus

moyenneIncertitudeA = np.mean(incertitudeA)
moyenneIncertitudeT = np.mean(incertitudeT)
moyenneIncertitudeR = np.mean(incertitudeR)
# On trouve les incertitudes moyennes pour chaque proportion trouvée

plt.plot(pDispersion, A, 'b-')
plt.plot(pDispersion, T, 'g-')
plt.plot(pDispersion, R, 'r-')

plt.text(pDispersion[0], A[0], s='incertitude : ' + str(moyenneIncertitudeA))
plt.text(pDispersion[0], T[0], s='incertitude : ' + str(moyenneIncertitudeT))
plt.text(pDispersion[0], R[0], s='incertitude : ' + str(moyenneIncertitudeR))
# On montre les incertitudes moyennes sur les courbes correspondantes

plt.xlabel('Probabilité de dispersion des neutrons')
plt.ylabel('Proportions des neutrons')
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire6-figureQ4-1.png')
plt.show()