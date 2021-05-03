# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule la trajectoire de neutrons ayant été lancés à
travers une plaque solide amorphe selon certains paramètres de départ.
Le programme transmet ensuite la proportion de ces neutrons ayant été
émis, la proportion des neutrons ayant été réfléchis et la proportion
de ceux qui ont été absorbés. Il le fait plutôt rapidement en utilisant
le plein potentiel de Numpy."""

import numpy as np

def etatNeutronsNP(pAbsorption, pDispersion, libreParcoursMoyen, epaisseur,
nombreNeutrons):
    """Cette fonction calcule la trajectoire de neutrons ayant été
    lancés à travers une plaque solide amorphe selon certains 
    paramètres de départ et transmet ensuite les proportions de 
    neutrons ayant été émis, réfléchis et absorbés en utilisant le 
    module Numpy.

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

    positionsX = np.zeros(nombreNeutrons)
    directions = np.ones(nombreNeutrons)

    """On définit deux ndarrays avec le bon nombre d'éléments qui garderont
    les informations sur la position sur l'axe des x et sur la direction du
    neutron (donné par le cosinus de l'angle entre la trajectoire et l'axe des
    x puisqu'il n'y a que la position en x qui nous importe)"""

    actifs = np.ones(nombreNeutrons, dtype=bool)
    # On définit un ndarray qui va garder le compte des neutrons actifs

    iActifs, = actifs.nonzero()
    # On trouve les indices des neutrons encore actifs dans la plaque

    while iActifs.size != 0:
        # On continue tant qu'il reste des neutrons actifs
        positionsX[iActifs] += np.random.exponential(scale=libreParcoursMoyen,
size=iActifs.size) * directions[iActifs]
        
        """On calcule la distance par rapport à l'axe des x que le neutron 
        parcourt avant une nouvelle interraction"""

        i, = np.nonzero(positionsX[iActifs] < 0)
        # On fait le test de réflexion
        actifs[iActifs[i]] = False
        # On rends les neutrons réfléchis inactifs

        i, = np.nonzero(positionsX[iActifs] > epaisseur)
        # On fait le test de transmission
        actifs[iActifs[i]] = False
        # On rend les neutrons transmis inactifs

        iActifs, = actifs.nonzero()
        # On redéfinit quels neutrons sont actifs

        rdm = np.random.random(iActifs.size)

        """On fait un ndarray de nombres aléatoires entre 0 et 1 pour notre
        test d'absorption"""

        i, = np.nonzero(rdm < pAbsorption)
        # On fait le test d'absorption
        actifs[iActifs[i]] = False
        # On rend les neutrons absorbés inactifs

        i, = np.nonzero(rdm > 1 - pDispersion)
        # On fait le test de dispersion
        directions[iActifs[i]] = 1 - 2 * np.random.random(i.size)
        # On calcule le nouvel angle si le neutron est dipersé par l'atome

        iActifs, = actifs.nonzero()
        # On redéfinit encore quels neutrons sont actifs

    reflechis = np.size(np.nonzero(positionsX < 0))
    transmis = np.size(np.nonzero(positionsX > epaisseur))
    absorbes = np.size(np.nonzero((positionsX >= 0) & (positionsX <= \
    epaisseur)))
    # On trouve les états finaux des neutrons

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

epaisseur = 1
libreParcoursMoyen = 0.2
nombreNeutrons = 1000
# On définit les conditions de départ communes

proportions = []
# On définit une liste vide où on va placer les résultats

proportions.extend(etatNeutronsNP(0, 0, libreParcoursMoyen, epaisseur, 
nombreNeutrons))

"""On fait le test pour le cas où la probabilité que le neutron soit absorbé
est la même que la probabilité qu'il soit dipersé."""

proportions.extend(etatNeutronsNP(1, 0, libreParcoursMoyen, epaisseur, 
nombreNeutrons))
# On fait le test pour le cas où la propabilité d'absorption est de 100%

proportions.extend(etatNeutronsNP(0.3, 0.3, libreParcoursMoyen, epaisseur,
nombreNeutrons))

"""On fait le test où la probabilité d'absorption et la probabilité de
dispertion sont à 30%"""

proportions.extend(etatNeutronsNP(libreParcoursMoyen, 0, libreParcoursMoyen,
epaisseur, nombreNeutrons))

"""On fait le test où la probabilité d'absorption est égale au parcours libre
moyen et la probabilité de dispertion est nulle"""

A, T, R = [], [], []
# On définit les listes qui trieront les résultats

i = 0
# On met le compteur à 0

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

i = 0
# On remet le compteur à 0

while i < len(A):
    # On arrête lorsqu'il n'y a plus d'éléments à montrer à l'utilisateur
    if i == 0:
        print('Probabilité d\'absorption et de dispertion égales:')
    elif i == 1:
        print('Probabilité d\'absorption égale à 1:')
    elif i == 2:
        print('Probabilité d\'absorption et de dispertion à 0.3:')
    else:
        print('Probabilité d\'absorption à 0.2 et probabilité de dispertion \
à 0:')

    """On décrit brièvement chaque test effectué avant d'afficher les
    résultats à l'utilisateur"""

    print('Proportions des neutrons:\nAbsorbés: ' + str(A[i]) + \
' avec une incertitude de ' + str(incertitudeA[i]) + '\nTransmis: ' +  \
str(T[i]) + ' avec une incertitude de ' + str(incertitudeT[i]) + \
'\nRéfléchis: ' + str(R[i]) + ' avec une incertitude de ' + \
str(incertitudeR[i]) + '\n')
    # On montre les résultats des tests effectués
    i += 1