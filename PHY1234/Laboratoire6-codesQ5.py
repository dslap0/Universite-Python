# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule la trajectoire de neutrons ayant �t� lanc�s �
travers une plaque solide amorphe selon certains param�tres de d�part.
Le programme transmet ensuite la proportion de ces neutrons ayant �t�
�mis, la proportion des neutrons ayant �t� r�fl�chis et la proportion
de ceux qui ont �t� absorb�s. Il le fait plut�t rapidement en utilisant
le plein potentiel de Numpy."""

import numpy as np

def etatNeutronsNP(pAbsorption, pDispersion, libreParcoursMoyen, epaisseur,
nombreNeutrons):
    """Cette fonction calcule la trajectoire de neutrons ayant �t�
    lanc�s � travers une plaque solide amorphe selon certains 
    param�tres de d�part et transmet ensuite les proportions de 
    neutrons ayant �t� �mis, r�fl�chis et absorb�s en utilisant le 
    module Numpy.

    pAbsorption : Probabilit� d'absorption du neutron par un atome.
    pDispersion : Probabilit� de dispertion du neutron par un atome.
    libreParcoursMoyen : Distance moyenne parcourue en ligne droite 
    avant d'int�ragir avec un noyau.
    epaisseur : �paisseur de la plaque solide amorphe
    nombreNeutrons : Nombre de neutrons dont il faut calculer la
    trajectoire.
    """
    if pDispersion + pAbsorption > 1:
        print('Erreur, la probabilit� que le neutron soit absorb� ou \
dispers� est sup�rieure\n� 100%. Veuillez r�essayer.')
        return None, None, None

    positionsX = np.zeros(nombreNeutrons)
    directions = np.ones(nombreNeutrons)

    """On d�finit deux ndarrays avec le bon nombre d'�l�ments qui garderont
    les informations sur la position sur l'axe des x et sur la direction du
    neutron (donn� par le cosinus de l'angle entre la trajectoire et l'axe des
    x puisqu'il n'y a que la position en x qui nous importe)"""

    actifs = np.ones(nombreNeutrons, dtype=bool)
    # On d�finit un ndarray qui va garder le compte des neutrons actifs

    iActifs, = actifs.nonzero()
    # On trouve les indices des neutrons encore actifs dans la plaque

    while iActifs.size != 0:
        # On continue tant qu'il reste des neutrons actifs
        positionsX[iActifs] += np.random.exponential(scale=libreParcoursMoyen,
size=iActifs.size) * directions[iActifs]
        
        """On calcule la distance par rapport � l'axe des x que le neutron 
        parcourt avant une nouvelle interraction"""

        i, = np.nonzero(positionsX[iActifs] < 0)
        # On fait le test de r�flexion
        actifs[iActifs[i]] = False
        # On rends les neutrons r�fl�chis inactifs

        i, = np.nonzero(positionsX[iActifs] > epaisseur)
        # On fait le test de transmission
        actifs[iActifs[i]] = False
        # On rend les neutrons transmis inactifs

        iActifs, = actifs.nonzero()
        # On red�finit quels neutrons sont actifs

        rdm = np.random.random(iActifs.size)

        """On fait un ndarray de nombres al�atoires entre 0 et 1 pour notre
        test d'absorption"""

        i, = np.nonzero(rdm < pAbsorption)
        # On fait le test d'absorption
        actifs[iActifs[i]] = False
        # On rend les neutrons absorb�s inactifs

        i, = np.nonzero(rdm > 1 - pDispersion)
        # On fait le test de dispersion
        directions[iActifs[i]] = 1 - 2 * np.random.random(i.size)
        # On calcule le nouvel angle si le neutron est dipers� par l'atome

        iActifs, = actifs.nonzero()
        # On red�finit encore quels neutrons sont actifs

    reflechis = np.size(np.nonzero(positionsX < 0))
    transmis = np.size(np.nonzero(positionsX > epaisseur))
    absorbes = np.size(np.nonzero((positionsX >= 0) & (positionsX <= \
    epaisseur)))
    # On trouve les �tats finaux des neutrons

    proportionAbsorbes = absorbes / nombreNeutrons
    proportionTransmis = transmis / nombreNeutrons
    proportionReflechis = reflechis / nombreNeutrons
    # On trouve les proportions de neutrons absorb�s, transmis et r�fl�chis

    return proportionAbsorbes, proportionTransmis, proportionReflechis

def incertitudeGaussienne(quantite, repetition):
    """Cette fonction trouve l'incertitude sur une quantit� ob�issant �
    une distribution Gaussienne.

    quantite : Quantit� dont il faut calculer l'incertitude, de type ndarray.
    repetition : Nombre de r�p�titions de l'exp�rience.
    """
    incertitude = np.sqrt(quantite * (1 - quantite) / (repetition - 1))

    return incertitude

epaisseur = 1
libreParcoursMoyen = 0.2
nombreNeutrons = 1000
# On d�finit les conditions de d�part communes

proportions = []
# On d�finit une liste vide o� on va placer les r�sultats

proportions.extend(etatNeutronsNP(0, 0, libreParcoursMoyen, epaisseur, 
nombreNeutrons))

"""On fait le test pour le cas o� la probabilit� que le neutron soit absorb�
est la m�me que la probabilit� qu'il soit dipers�."""

proportions.extend(etatNeutronsNP(1, 0, libreParcoursMoyen, epaisseur, 
nombreNeutrons))
# On fait le test pour le cas o� la propabilit� d'absorption est de 100%

proportions.extend(etatNeutronsNP(0.3, 0.3, libreParcoursMoyen, epaisseur,
nombreNeutrons))

"""On fait le test o� la probabilit� d'absorption et la probabilit� de
dispertion sont � 30%"""

proportions.extend(etatNeutronsNP(libreParcoursMoyen, 0, libreParcoursMoyen,
epaisseur, nombreNeutrons))

"""On fait le test o� la probabilit� d'absorption est �gale au parcours libre
moyen et la probabilit� de dispertion est nulle"""

A, T, R = [], [], []
# On d�finit les listes qui trieront les r�sultats

i = 0
# On met le compteur � 0

while i < len(proportions):
    if i % 3 == 0:
        A.append(proportions[i])
    elif i % 3 == 1:
        T.append(proportions[i])
    else:
        R.append(proportions[i])
    i += 1
# On assigne les r�sultats obtenus aux listes correspondantes

A = np.array(A)
T = np.array(T)
R = np.array(R)

"""On transforme les r�sultats en ndarray pour effectuer le calcul
d'incertitude"""

incertitudeA = incertitudeGaussienne(A, nombreNeutrons)
incertitudeT = incertitudeGaussienne(T, nombreNeutrons)
incertitudeR = incertitudeGaussienne(R, nombreNeutrons)
# On calcule les diff�rentes incertitudes sur les r�sultats obtenus

i = 0
# On remet le compteur � 0

while i < len(A):
    # On arr�te lorsqu'il n'y a plus d'�l�ments � montrer � l'utilisateur
    if i == 0:
        print('Probabilit� d\'absorption et de dispertion �gales:')
    elif i == 1:
        print('Probabilit� d\'absorption �gale � 1:')
    elif i == 2:
        print('Probabilit� d\'absorption et de dispertion � 0.3:')
    else:
        print('Probabilit� d\'absorption � 0.2 et probabilit� de dispertion \
� 0:')

    """On d�crit bri�vement chaque test effectu� avant d'afficher les
    r�sultats � l'utilisateur"""

    print('Proportions des neutrons:\nAbsorb�s: ' + str(A[i]) + \
' avec une incertitude de ' + str(incertitudeA[i]) + '\nTransmis: ' +  \
str(T[i]) + ' avec une incertitude de ' + str(incertitudeT[i]) + \
'\nR�fl�chis: ' + str(R[i]) + ' avec une incertitude de ' + \
str(incertitudeR[i]) + '\n')
    # On montre les r�sultats des tests effectu�s
    i += 1