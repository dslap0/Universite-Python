# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code simule la propagation d'une maladie bénigne et contagieuse
dans une population de marcheurs vacinnés à certains taux variables. Il
montre ensuite quelques graphiques pour représenter la situation d'un
point de vue économique."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 5000
dureeInfection = 25
nIterationsMax = 5000
densitePop = 0.5
tailleReseau = np.sqrt(nMarcheurs / densitePop)
# On définit des paramètres de départ

coutMoyen = np.array([])
deviationCoutMoyen = np.array([])
erreurProportionVaccine = np.array([])

"""On définit une série de ndarray qui contiendront des valeurs calculées en
vue de produire les graphiques"""

proportionVaccine = np.linspace(0, 1, 21)

"""On fait un ndarray qui parcourt l'ensemble du domaine des proportions de
vaccination possible"""

for i in range(0, proportionVaccine.size):
    # On exécute la simulation pour chaque densité de population

    cout = np.array([])
    
    """On définit un autre ndarray qui contiendra des valeurs calculées pour
    tracer un graphique, mais qui devra être effacé après chaque changement
    de pourcentage de vaccination"""
    
    nVaccines = nMarcheurs * proportionVaccine[i]
    # On trouve le nombre de marcheurs vaccinés

    for K in range(1, 11):
        # On effectue chaque simulation 10 fois
        
        np.random.seed() 
        # On fait l'initialisation du germe du generateur aléatoire

        x = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        y = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        # On définit les positions initiales des marcheurs

        etat = np.zeros(nMarcheurs, dtype='bool')
    
        """On définit un ndarray d'état des marcheurs (False: santé, 
        True: infecté)"""

        tempsInfecte = np.zeros(nMarcheurs, dtype='int')

        """On définit un ndarray qui stockera le temps d'infection restant (si
        infecté)"""

        premierInfecte = np.random.randint(0, nMarcheurs)
        # On sélectionne le premier infecté
        etat[premierInfecte] = 1
        tempsInfecte[premierInfecte] = dureeInfection
        # On l'infecte et on indique son temps d'infection restant

        nInfectes = 1
        nDejaInfecte = 1
        nIterations = 0
        # On définit les compteurs d'infectés et d'itérations

        immunise = np.zeros(nMarcheurs, dtype='bool')
        immunise[:int(nVaccines) + 1] = True
        # On vaccine la proportion de population voulue

        while (nInfectes > 0) and (nIterations < nIterationsMax):
    
            """On exécute tant que le temps n'est pas écoulé ou qu'il ne reste
            plus d'infectés"""

            rdm = np.random.randint(0, 4, nMarcheurs)
            # On trouve des valeurs pour faire le test de direction du pas

            x = np.where(rdm == 0, x + 1, x)
            y = np.where(rdm == 1, y + 1, y)
            x = np.where(rdm == 2, x - 1, x)
            y = np.where(rdm == 3, y - 1, y)
        
            """On fait les test de direction du pas et le déplacement qui en
            découle"""

            x = np.clip(x, 1, tailleReseau)
            y = np.clip(y, 1, tailleReseau)
            # On s'assure que les marcheurs ne sortent pas de la grille

            for iInfecte in etat.nonzero()[0]:
                # On fait une boucle sur tous les marcheurs infectés
                iPotentielNouvelInfecte, = ((x == x[iInfecte]) & (y == 
y[iInfecte]) & (etat == False) & (immunise == False)).nonzero()
                
                """On trouve les indices des marcheurs qui seront peut-être
                infectés"""

                rdm = np.random.random(iPotentielNouvelInfecte.size)
                iNouvelInfecte = iPotentielNouvelInfecte[(rdm < 0.5).nonzero(
)[0]]
                """On fait le test d'infection pour chaque nouvel infecté
                potentiel"""

                nNouveauxInfectes = iNouvelInfecte.size
                # On trouve le nombre de marcheurs qui seront infectés

                if nNouveauxInfectes > 0:

                    """La contagion n'a lieu que si au moins un nouveau
                    marcheur est infecté"""

                    etat[iNouvelInfecte] = True
                    tempsInfecte[iNouvelInfecte] = dureeInfection
                    # On infecte les nouveaux infectés

                    nInfectes += nNouveauxInfectes
                    nDejaInfecte += nNouveauxInfectes
                    # On ajuste les compteurs d'infectés
        
                tempsInfecte[iInfecte] -= 1
                # On diminue le temps d'infection possible

                if tempsInfecte[iInfecte] == 0:
                    etat[iInfecte] = False
                    immunise[iInfecte] = True
                    # On guérit le malade et on l'immunise

                    nInfectes -= (etat[iInfecte] == 2).size
                    # On ajuste le compteur d'infectés

            nIterations += 1

        cout = np.append(cout, nDejaInfecte * 100 + nVaccines * 50)
        # On définit ce que la situation a coûtée au gouvernement

    coutMoyen = np.append(coutMoyen, np.mean(cout))
    deviationCoutMoyen = np.append(deviationCoutMoyen, np.std(cout))

    """On trouve le coût moyen et la déviation standard de ce coût pour chaque
    proportion de population vaccinée"""

    erreurProportionVaccine = np.append(erreurProportionVaccine,
abs(nVaccines - int(nVaccines)) / nMarcheurs)

plt.plot(proportionVaccine, coutMoyen)

plt.xlabel('Proportion de la population vaccinée')
plt.ylabel('Coût moyen au gouvernement (en dollars)')
plt.errorbar(proportionVaccine, coutMoyen, yerr=deviationCoutMoyen,
xerr=erreurProportionVaccine)

plt.savefig('Laboratoire10-figureQ3.png')
plt.show()