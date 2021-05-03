# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code simule la propagation d'une maladie mortelle et contagieuse
dans une population de marcheurs. Il montre ensuite quelques graphiques
pour repr�senter la situation."""

import numpy as np

import matplotlib.pyplot as plt

def instantane(x, y, etat):
    """Cette fonction fait un instantan� des positions de chaque
    marcheur et de leur �tat.
    x : Position en x de chaque marcheur (ndarray)
    y : Position en y de chaqye marcheur (ndarray)
    etat : �tat de chaque marcheur, avec 0 = sain, 1 = infect� et 
    2 = mort (ndarray)
    """
    iSain = np.nonzero(etat == 0)
    iInfecte = np.nonzero(etat == 1)
    iMort = np.nonzero(etat == 2)
    # On trouve les indices des marcheurs sains, infect�s et morts
    
    plt.figure()
    plt.plot(x[iSain], y[iSain], '.b')
    plt.plot(x[iInfecte], y[iInfecte], '.r')
    plt.plot(x[iMort], y[iMort], '.k')

    plt.xlabel('Position en x')
    plt.ylabel('Position en y')
    # On modifie les options esth�tiques du graphique

    plt.savefig('Laboratoire10-figureQ1-6.png')

tailleReseau = 128
nMarcheurs = 5000
dureeSurvie = 20
nIterationsMax = 5000
# On d�finit des param�tres de d�part

np.random.seed() 
# On fait l'initialisation du germe du generateur al�atoire

x = np.random.randint(1, tailleReseau + 1, nMarcheurs)
y = np.random.randint(1, tailleReseau + 1, nMarcheurs)
# On d�finit les positions initiales des marcheurs

etat = np.zeros(nMarcheurs, dtype='int')
# On d�finit un ndarray d'�tat des marcheurs (0: sant�, 1: infect�, 2: mort)
tempsSurvie = np.zeros(nMarcheurs, dtype='int')
# On d�finit un ndarray qui stockera le temps de survie restant (si infect�)

premierInfecte = np.random.randint(0, nMarcheurs)
# On s�lectionne le premier infect�
etat[premierInfecte] = 1
tempsSurvie[premierInfecte] = dureeSurvie
# On l'infecte et on indique son temps de survie restant

nInfectes = 1
nMorts = 0
# On d�finit un compteur d'infect�s et un compteur de morts

iteration = np.array([0])
vivants = np.array([nMarcheurs])
infectes = np.array([nInfectes])

"""On d�finit des ndarrays qui vont nous permettre de voir l'�volution de la
maladie � chaque it�ration sur le graphique"""

while (nInfectes > 0) and (iteration[-1] < nIterationsMax):
    
    """On ex�cute tant que le temps n'est pas �coul� ou que tout le monde n'est
    pas infect�"""

    iVivant, = (etat < 2).nonzero()
    # On trouve les indices des marcheurs vivants
    nVivants = iVivant.size
    # On trouve le nombre de marcheurs vivants

    rdm = np.random.randint(0, 4, nVivants)
    # On trouve des valeurs pour faire le test de direction du pas

    x[iVivant] = np.where(rdm == 0, x[iVivant] + 1, x[iVivant])
    y[iVivant] = np.where(rdm == 1, y[iVivant] + 1, y[iVivant])
    x[iVivant] = np.where(rdm == 2, x[iVivant] - 1, x[iVivant])
    y[iVivant] = np.where(rdm == 3, y[iVivant] - 1, y[iVivant])
    # On fait les test de direction du pas et le d�placement qui en d�coule

    x[iVivant] = np.clip(x[iVivant], 1, tailleReseau)
    y[iVivant] = np.clip(y[iVivant], 1, tailleReseau)
    # On s'assure que les marcheurs ne sortent pas de la grille

    for iInfecte in (etat == 1).nonzero()[0]:
        # On fait une boucle sur tous les marcheurs infect�s
        iNouvelInfecte, = ((x == x[iInfecte]) & (y == y[iInfecte]) & 
(etat == 0)).nonzero()
        # On trouve les indices des marcheurs qui seront infect�s
        nNouveauxInfectes = iNouvelInfecte.size
        # On trouve le nombre de marcheurs qui seront infect�s
        if nNouveauxInfectes > 0:
            # On ne fait la contagion que s'il y a au moins un nouvel infect�
            etat[iNouvelInfecte] = 1
            tempsSurvie[iNouvelInfecte] = dureeSurvie
            # On infecte les nouveaux infect�s
            nInfectes += nNouveauxInfectes
            # On ajuste le compteur d'infect�s
        
        tempsSurvie[iInfecte] -= 1
        # On diminue le temps de survie possible
        if tempsSurvie[iInfecte] == 0:
            etat[iInfecte] = 2
            # On tue le malade
            nMorts += (etat[iInfecte] == 2).size
            nInfectes -= (etat[iInfecte] == 2).size
            # On ajuste les compteurs de morts et d'infect�s

    vivants = np.append(vivants, nMarcheurs - nMorts)
    infectes = np.append(infectes, nInfectes)
    # On ajoute les valeurs correspondantes dans les ndarray pour le graphique
    iteration = np.append(iteration, iteration[-1] + 1)
    print("It�ration {}: {} malades, {} morts.".format(iteration[-1],
nInfectes, nMorts))
    if iteration[-1] == 300:
        # On prend un instantan� de la population apr�s 300 it�rations
        instantane(x, y, etat)

fig, axe1 = plt.subplots()
axe1.plot(iteration, infectes, '-r')

axe1.set_xlabel('Nombre d\'it�rations �coul�es')
axe1.set_ylabel('Nombre d\'infect�s (en rouge)')
# On modifie les options esth�tiques

axe2 = axe1.twinx()
axe2.plot(iteration, vivants, '-k')

axe2.set_ylabel('Nombre de vivants (en noir)')

plt.savefig('Laboratoire10-figureQ1-5.png')
plt.show()