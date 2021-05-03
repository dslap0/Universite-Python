# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code simule la propagation d'une maladie mortelle et contagieuse
dans une population de marcheurs de densit� de population variable. Il
montre ensuite quelques graphiques pour repr�senter la situation."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 5000
dureeSurvie = 20
nIterationsMax = 5000
# On d�finit des param�tres de d�part

densitePop = np.arange(0.15, 0.51, 0.05)
tailleReseau = np.sqrt(nMarcheurs / densitePop)
# On trouve la bonne taille de r�seau pour chaque densit� de population

tauxMortaliteMoyen = np.array([])
deviationTauxMortaliteMoyen = np.array([])
dureeEpidemieMoyenne = np.array([])
deviationDureeEpidemieMoyenne = np.array([])

"""On d�finit une s�rie de ndarray qui contiendront des valeurs calcul�es en
vue de produire les graphiques"""

couleur = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'tab:brown']
# On d�finit toutes les couleurs pour tracer le nuage de point

for i in range(0, tailleReseau.size):
    # On ex�cute la simulation pour chaque densit� de population

    tauxMortalite = np.array([])
    dureeEpidemie = np.array([])
    
    """On d�finit d'autres ndarray qui contiendront des valeurs calcul�es pour
    tracer un graphique, mais qui dervront �tre effac�s apr�s chaque changement
    de taille le r�seau"""

    for K in range(1, 11):
        # On effectue chaque simulation 10 fois
        
        np.random.seed() 
        # On fait l'initialisation du germe du generateur al�atoire

        x = np.random.randint(1, tailleReseau[i] + 1, nMarcheurs)
        y = np.random.randint(1, tailleReseau[i] + 1, nMarcheurs)
        # On d�finit les positions initiales des marcheurs

        etat = np.zeros(nMarcheurs, dtype='int')
    
        """On d�finit un ndarray d'�tat des marcheurs (0: sant�, 1: infect�,
        2: mort)"""

        tempsSurvie = np.zeros(nMarcheurs, dtype='int')

        """On d�finit un ndarray qui stockera le temps de survie restant (si
        infect�)"""

        premierInfecte = np.random.randint(0, nMarcheurs)
        # On s�lectionne le premier infect�
        etat[premierInfecte] = 1
        tempsSurvie[premierInfecte] = dureeSurvie
        # On l'infecte et on indique son temps de survie restant

        nInfectes = 1
        nMorts = 0
        nIterations = 0
        # On d�finit les compteurs d'infect�s, de morts et d'it�rations

        while (nInfectes > 0) and (nIterations < nIterationsMax):
    
            """On ex�cute tant que le temps n'est pas �coul� ou que tout le
            monde n'est pas infect�"""

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
        
            """On fait les test de direction du pas et le d�placement qui en
            d�coule"""

            x[iVivant] = np.clip(x[iVivant], 1, tailleReseau[i])
            y[iVivant] = np.clip(y[iVivant], 1, tailleReseau[i])
            # On s'assure que les marcheurs ne sortent pas de la grille

            for iInfecte in (etat == 1).nonzero()[0]:
                # On fait une boucle sur tous les marcheurs infect�s

                iNouvelInfecte, = ((x == x[iInfecte]) & (y == y[iInfecte]) &
(etat == 0)).nonzero()
                # On trouve les indices des marcheurs qui seront infect�s
                nNouveauxInfectes = iNouvelInfecte.size
                # On trouve le nombre de marcheurs qui seront infect�s

                if nNouveauxInfectes > 0:

                    """La contagion n'a lieu que si au moins un nouveau
                    marcheur est infect�"""

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

            nIterations += 1

        tauxMortalite = np.append(tauxMortalite, nMorts / nMarcheurs)
        dureeEpidemie = np.append(dureeEpidemie, nIterations)

        """On calcule des valeurs 10 fois � chaque densit� pour faire des
        moyennes et tracer un graphique"""

        plt.figure(0)

        plt.scatter(dureeEpidemie, tauxMortalite, c=str(couleur[i]))

    tauxMortaliteMoyen = np.append(tauxMortaliteMoyen, np.mean(tauxMortalite))
    deviationTauxMortaliteMoyen = np.append(deviationTauxMortaliteMoyen,
np.std(tauxMortalite))
    # On trouve les valeurs pour tracer le graphique li� aux taux de mortalit�

    dureeEpidemieMoyenne = np.append(dureeEpidemieMoyenne,
np.mean(dureeEpidemie))
    deviationDureeEpidemieMoyenne = np.append(deviationDureeEpidemieMoyenne,
np.std(dureeEpidemie))
    
    """On trouve les valeurs pour tracer le graphique li� aux dur�es de
    l'�pid�mie"""

plt.figure(0)

plt.xlabel('Dur�e de l\'�pid�mie (en it�rations)')
plt.ylabel('Taux de mortalit� (en morts/marcheurs)')
# On modifie les options esth�tiques du graphique de nuage de points

plt.savefig('Laboratoire10-figureQ2-3.png')

plt.ylim(-0.01, 0.05)
plt.xlim(-20, 350)
# On effectue un agrandissement sur la figure pr�c�dente

plt.savefig('Laboratoire10-figureQ2-4.png')

plt.figure(1)

plt.plot(densitePop, tauxMortaliteMoyen, '-')

plt.xlabel('Densit� de la population sur le territoire')
plt.ylabel('Taux de mortalit� moyen (en morts/marcheurs)')
plt.errorbar(densitePop, tauxMortaliteMoyen, yerr=deviationTauxMortaliteMoyen)
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire10-figureQ2-1.png')

plt.figure(2)

plt.plot(densitePop, dureeEpidemieMoyenne, '-')

plt.xlabel('Densit� de la population sur le territoire')
plt.ylabel('Dur�e moyenne de l\'�pid�mie (en it�rations)')
plt.errorbar(densitePop, dureeEpidemieMoyenne,
yerr=deviationDureeEpidemieMoyenne)
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire10-figureQ2-2.png')

plt.show()