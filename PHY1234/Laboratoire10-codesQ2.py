# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code simule la propagation d'une maladie mortelle et contagieuse
dans une population de marcheurs de densité de population variable. Il
montre ensuite quelques graphiques pour représenter la situation."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 5000
dureeSurvie = 20
nIterationsMax = 5000
# On définit des paramètres de départ

densitePop = np.arange(0.15, 0.51, 0.05)
tailleReseau = np.sqrt(nMarcheurs / densitePop)
# On trouve la bonne taille de réseau pour chaque densité de population

tauxMortaliteMoyen = np.array([])
deviationTauxMortaliteMoyen = np.array([])
dureeEpidemieMoyenne = np.array([])
deviationDureeEpidemieMoyenne = np.array([])

"""On définit une série de ndarray qui contiendront des valeurs calculées en
vue de produire les graphiques"""

couleur = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'tab:brown']
# On définit toutes les couleurs pour tracer le nuage de point

for i in range(0, tailleReseau.size):
    # On exécute la simulation pour chaque densité de population

    tauxMortalite = np.array([])
    dureeEpidemie = np.array([])
    
    """On définit d'autres ndarray qui contiendront des valeurs calculées pour
    tracer un graphique, mais qui dervront être effacés après chaque changement
    de taille le réseau"""

    for K in range(1, 11):
        # On effectue chaque simulation 10 fois
        
        np.random.seed() 
        # On fait l'initialisation du germe du generateur aléatoire

        x = np.random.randint(1, tailleReseau[i] + 1, nMarcheurs)
        y = np.random.randint(1, tailleReseau[i] + 1, nMarcheurs)
        # On définit les positions initiales des marcheurs

        etat = np.zeros(nMarcheurs, dtype='int')
    
        """On définit un ndarray d'état des marcheurs (0: santé, 1: infecté,
        2: mort)"""

        tempsSurvie = np.zeros(nMarcheurs, dtype='int')

        """On définit un ndarray qui stockera le temps de survie restant (si
        infecté)"""

        premierInfecte = np.random.randint(0, nMarcheurs)
        # On sélectionne le premier infecté
        etat[premierInfecte] = 1
        tempsSurvie[premierInfecte] = dureeSurvie
        # On l'infecte et on indique son temps de survie restant

        nInfectes = 1
        nMorts = 0
        nIterations = 0
        # On définit les compteurs d'infectés, de morts et d'itérations

        while (nInfectes > 0) and (nIterations < nIterationsMax):
    
            """On exécute tant que le temps n'est pas écoulé ou que tout le
            monde n'est pas infecté"""

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
        
            """On fait les test de direction du pas et le déplacement qui en
            découle"""

            x[iVivant] = np.clip(x[iVivant], 1, tailleReseau[i])
            y[iVivant] = np.clip(y[iVivant], 1, tailleReseau[i])
            # On s'assure que les marcheurs ne sortent pas de la grille

            for iInfecte in (etat == 1).nonzero()[0]:
                # On fait une boucle sur tous les marcheurs infectés

                iNouvelInfecte, = ((x == x[iInfecte]) & (y == y[iInfecte]) &
(etat == 0)).nonzero()
                # On trouve les indices des marcheurs qui seront infectés
                nNouveauxInfectes = iNouvelInfecte.size
                # On trouve le nombre de marcheurs qui seront infectés

                if nNouveauxInfectes > 0:

                    """La contagion n'a lieu que si au moins un nouveau
                    marcheur est infecté"""

                    etat[iNouvelInfecte] = 1
                    tempsSurvie[iNouvelInfecte] = dureeSurvie
                    # On infecte les nouveaux infectés
                    
                    nInfectes += nNouveauxInfectes
                    # On ajuste le compteur d'infectés
        
                tempsSurvie[iInfecte] -= 1
                # On diminue le temps de survie possible

                if tempsSurvie[iInfecte] == 0:
                    etat[iInfecte] = 2
                    # On tue le malade

                    nMorts += (etat[iInfecte] == 2).size
                    nInfectes -= (etat[iInfecte] == 2).size
                    # On ajuste les compteurs de morts et d'infectés

            nIterations += 1

        tauxMortalite = np.append(tauxMortalite, nMorts / nMarcheurs)
        dureeEpidemie = np.append(dureeEpidemie, nIterations)

        """On calcule des valeurs 10 fois à chaque densité pour faire des
        moyennes et tracer un graphique"""

        plt.figure(0)

        plt.scatter(dureeEpidemie, tauxMortalite, c=str(couleur[i]))

    tauxMortaliteMoyen = np.append(tauxMortaliteMoyen, np.mean(tauxMortalite))
    deviationTauxMortaliteMoyen = np.append(deviationTauxMortaliteMoyen,
np.std(tauxMortalite))
    # On trouve les valeurs pour tracer le graphique lié aux taux de mortalité

    dureeEpidemieMoyenne = np.append(dureeEpidemieMoyenne,
np.mean(dureeEpidemie))
    deviationDureeEpidemieMoyenne = np.append(deviationDureeEpidemieMoyenne,
np.std(dureeEpidemie))
    
    """On trouve les valeurs pour tracer le graphique lié aux durées de
    l'épidémie"""

plt.figure(0)

plt.xlabel('Durée de l\'épidémie (en itérations)')
plt.ylabel('Taux de mortalité (en morts/marcheurs)')
# On modifie les options esthétiques du graphique de nuage de points

plt.savefig('Laboratoire10-figureQ2-3.png')

plt.ylim(-0.01, 0.05)
plt.xlim(-20, 350)
# On effectue un agrandissement sur la figure précédente

plt.savefig('Laboratoire10-figureQ2-4.png')

plt.figure(1)

plt.plot(densitePop, tauxMortaliteMoyen, '-')

plt.xlabel('Densité de la population sur le territoire')
plt.ylabel('Taux de mortalité moyen (en morts/marcheurs)')
plt.errorbar(densitePop, tauxMortaliteMoyen, yerr=deviationTauxMortaliteMoyen)
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire10-figureQ2-1.png')

plt.figure(2)

plt.plot(densitePop, dureeEpidemieMoyenne, '-')

plt.xlabel('Densité de la population sur le territoire')
plt.ylabel('Durée moyenne de l\'épidémie (en itérations)')
plt.errorbar(densitePop, dureeEpidemieMoyenne,
yerr=deviationDureeEpidemieMoyenne)
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire10-figureQ2-2.png')

plt.show()