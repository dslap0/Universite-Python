# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule la trajectoire de neutrons ayant �t� lanc�s �
travers une plaque solide amorphe selon certains param�tres de d�part.
Le programme transmet ensuite la proportion de ces neutrons ayant �t�
�mis, la proportion des neutrons ayant �t� r�fl�chis et la proportion
de ceux qui ont �t� absorb�s. Il trace ensuite trois histogrammes des 
r�sultats de chacune des proportions sur 500 essais."""

import numpy as np

import matplotlib.pyplot as plt

def etatNeutrons(pAbsorption, pDispersion, libreParcoursMoyen,epaisseur,
nombreNeutrons):
    """Cette fonction calcule la trajectoire de neutrons ayant �t�
    lanc�s � travers une plaque solide amorphe selon certains 
    param�tres de d�part et transmet ensuite les proportions de 
    neutrons ayant �t� �mis, r�fl�chis et absorb�s.

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

    absorbes, transmis, reflechis, = 0, 0, 0
    # On mets les compteurs � 0

    while absorbes + transmis + reflechis < nombreNeutrons:
        positionX, direction = 0, 1
        
        """On d�finit la position horizontale et la direction du neutron au
        lancement (donn�e par le cosinus de l'angle entre sa trajectoire et
        l'axe des x puisqu'on ne s'int�resse qu'� sa position en x)"""
        
        while True:
            
            """La boucle est incassable, on doit donc satisfaire un des test
            if (ou elif) pour en sortir"""

            positionX += np.random.exponential(libreParcoursMoyen) * direction
            
            """ On trouve la distance parcourue en X avant une possible 
            interaction"""

            if positionX < 0:
                reflechis += 1
                break
            # On fait le test de r�flexion
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
            # On calcule le nouvel angle si le neutron est dipers� par l'atome

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

pAbsorption = 0.3
pDispersion = 0.3
epaisseur = 1
libreParcoursMoyen = 0.2
nombreNeutrons = 1000
# On d�finit les conditions de d�part

proportions = []
# On d�finit une liste vide o� on va placer les r�sultats

i = 0
# On met le compteur � 0

while i < 500:
    proportions.extend(etatNeutrons(pAbsorption, pDispersion,
libreParcoursMoyen, epaisseur, nombreNeutrons))
    i += 1

"""On r�p�te l'exp�rience 500 fois et on place ces r�sultats dans la nouvelle
liste"""

A, T, R = [], [], []
# On d�finit les listes qui trieront les r�sultats

i = 0
# On remet le compteur � 0

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

moyenneIncertitudeA = np.mean(incertitudeA)
moyenneIncertitudeT = np.mean(incertitudeT)
moyenneIncertitudeR = np.mean(incertitudeR)
# On trouve les incertitudes moyennes pour chaque proportion trouv�e

print('Incertitude moyenne sur la proportion des neutrons:\nAbsorb�s: ' + \
str(moyenneIncertitudeA) + '\nTransmis: ' + str(moyenneIncertitudeT) + \
'\nR�fl�chis: ' + str(moyenneIncertitudeR))
# On montre les ndarray d'incertitudes calcul�s

plt.figure(1)
# On cr�e la premi�re figure � afficher pour 500 exp�riences

plt.subplot(1, 3, 1, xlabel='Neutrons absorb�s',
ylabel='Nombres d\'occurences')
plt.hist(A)
plt.tick_params(labelsize='small')
plt.subplot(1, 3, 2, xlabel= 'Neutrons transmis')
plt.hist(T)
plt.tick_params(labelsize='small')
plt.subplot(1, 3, 3, xlabel='Neutrons r�fl�chis')
plt.hist(R)
plt.tick_params(labelsize='small')
# On cr�e les 3 histogrammes

plt.tight_layout(pad=0.5, h_pad=0)
# On modifie les options esth�tiques

plt.savefig('Laboratoire6-figureQ3-1.png')
# On sauvegarde la premi�re figure pour 500 exp�riences

plt.show()