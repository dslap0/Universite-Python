# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code simule la propagation d'une maladie b�nigne et contagieuse
dans une population de marcheurs vacinn�s � certains taux variables. Il
montre ensuite quelques graphiques pour repr�senter la situation d'un
point de vue �conomique."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 5000
dureeInfection = 25
nIterationsMax = 5000
densitePop = 0.5
tailleReseau = np.sqrt(nMarcheurs / densitePop)
# On d�finit des param�tres de d�part

coutMoyen = np.array([])
deviationCoutMoyen = np.array([])
erreurProportionVaccine = np.array([])

"""On d�finit une s�rie de ndarray qui contiendront des valeurs calcul�es en
vue de produire les graphiques"""

proportionVaccine = np.linspace(0, 1, 21)

"""On fait un ndarray qui parcourt l'ensemble du domaine des proportions de
vaccination possible"""

for i in range(0, proportionVaccine.size):
    # On ex�cute la simulation pour chaque densit� de population

    cout = np.array([])
    
    """On d�finit un autre ndarray qui contiendra des valeurs calcul�es pour
    tracer un graphique, mais qui devra �tre effac� apr�s chaque changement
    de pourcentage de vaccination"""
    
    nVaccines = nMarcheurs * proportionVaccine[i]
    # On trouve le nombre de marcheurs vaccin�s

    for K in range(1, 11):
        # On effectue chaque simulation 10 fois
        
        np.random.seed() 
        # On fait l'initialisation du germe du generateur al�atoire

        x = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        y = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        # On d�finit les positions initiales des marcheurs

        etat = np.zeros(nMarcheurs, dtype='bool')
    
        """On d�finit un ndarray d'�tat des marcheurs (False: sant�, 
        True: infect�)"""

        tempsInfecte = np.zeros(nMarcheurs, dtype='int')

        """On d�finit un ndarray qui stockera le temps d'infection restant (si
        infect�)"""

        premierInfecte = np.random.randint(0, nMarcheurs)
        # On s�lectionne le premier infect�
        etat[premierInfecte] = 1
        tempsInfecte[premierInfecte] = dureeInfection
        # On l'infecte et on indique son temps d'infection restant

        nInfectes = 1
        nDejaInfecte = 1
        nIterations = 0
        # On d�finit les compteurs d'infect�s et d'it�rations

        immunise = np.zeros(nMarcheurs, dtype='bool')
        immunise[:int(nVaccines) + 1] = True
        # On vaccine la proportion de population voulue

        while (nInfectes > 0) and (nIterations < nIterationsMax):
    
            """On ex�cute tant que le temps n'est pas �coul� ou qu'il ne reste
            plus d'infect�s"""

            rdm = np.random.randint(0, 4, nMarcheurs)
            # On trouve des valeurs pour faire le test de direction du pas

            x = np.where(rdm == 0, x + 1, x)
            y = np.where(rdm == 1, y + 1, y)
            x = np.where(rdm == 2, x - 1, x)
            y = np.where(rdm == 3, y - 1, y)
        
            """On fait les test de direction du pas et le d�placement qui en
            d�coule"""

            x = np.clip(x, 1, tailleReseau)
            y = np.clip(y, 1, tailleReseau)
            # On s'assure que les marcheurs ne sortent pas de la grille

            for iInfecte in etat.nonzero()[0]:
                # On fait une boucle sur tous les marcheurs infect�s
                iPotentielNouvelInfecte, = ((x == x[iInfecte]) & (y == 
y[iInfecte]) & (etat == False) & (immunise == False)).nonzero()
                
                """On trouve les indices des marcheurs qui seront peut-�tre
                infect�s"""

                rdm = np.random.random(iPotentielNouvelInfecte.size)
                iNouvelInfecte = iPotentielNouvelInfecte[(rdm < 0.5).nonzero(
)[0]]
                """On fait le test d'infection pour chaque nouvel infect�
                potentiel"""

                nNouveauxInfectes = iNouvelInfecte.size
                # On trouve le nombre de marcheurs qui seront infect�s

                if nNouveauxInfectes > 0:

                    """La contagion n'a lieu que si au moins un nouveau
                    marcheur est infect�"""

                    etat[iNouvelInfecte] = True
                    tempsInfecte[iNouvelInfecte] = dureeInfection
                    # On infecte les nouveaux infect�s

                    nInfectes += nNouveauxInfectes
                    nDejaInfecte += nNouveauxInfectes
                    # On ajuste les compteurs d'infect�s
        
                tempsInfecte[iInfecte] -= 1
                # On diminue le temps d'infection possible

                if tempsInfecte[iInfecte] == 0:
                    etat[iInfecte] = False
                    immunise[iInfecte] = True
                    # On gu�rit le malade et on l'immunise

                    nInfectes -= (etat[iInfecte] == 2).size
                    # On ajuste le compteur d'infect�s

            nIterations += 1

        cout = np.append(cout, nDejaInfecte * 100 + nVaccines * 50)
        # On d�finit ce que la situation a co�t�e au gouvernement

    coutMoyen = np.append(coutMoyen, np.mean(cout))
    deviationCoutMoyen = np.append(deviationCoutMoyen, np.std(cout))

    """On trouve le co�t moyen et la d�viation standard de ce co�t pour chaque
    proportion de population vaccin�e"""

    erreurProportionVaccine = np.append(erreurProportionVaccine,
abs(nVaccines - int(nVaccines)) / nMarcheurs)

plt.plot(proportionVaccine, coutMoyen)

plt.xlabel('Proportion de la population vaccin�e')
plt.ylabel('Co�t moyen au gouvernement (en dollars)')
plt.errorbar(proportionVaccine, coutMoyen, yerr=deviationCoutMoyen,
xerr=erreurProportionVaccine)

plt.savefig('Laboratoire10-figureQ3.png')
plt.show()