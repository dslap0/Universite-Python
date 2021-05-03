# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code simule la propagation d'une maladie mortelle et contagieuse
dans une population de marcheurs vacinn�s � certains taux variables. Il
montre ensuite quelques graphiques pour repr�senter la situation d'un
point de vue �conomique et humain."""

import numpy as np

import matplotlib.pyplot as plt

nMarcheurs = 5000
dureeInfection = 20
dureeInfectionCadavre = 5
nIterationsMax = 5000
densitePop = 0.5
pMort = 0.6
pNouvelleSouche = 0.0001
tailleReseau = np.sqrt(nMarcheurs / densitePop)
# On d�finit des param�tres de d�part

coutMoyen = np.array([])
deviationCoutMoyen = np.array([])
erreurProportionVaccine = np.array([])
tauxMortaliteMoyen = np.array([])
deviationTauxMortaliteMoyen = np.array([])
dureeEpidemieMoyenne = np.array([])
deviationDureeEpidemieMoyenne = np.array([])

"""On d�finit une s�rie de ndarray qui contiendront des valeurs calcul�es en
vue de produire les graphiques"""

proportionVaccine = np.linspace(0, 1, 11)

"""On fait un ndarray qui parcourt l'ensemble du domaine des proportions de
vaccination possible"""

for i in range(0, proportionVaccine.size):
    # On ex�cute la simulation pour chaque densit� de population

    cout = np.array([])
    tauxMortalite = np.array([])
    dureeEpidemie = np.array([])
    
    """On d�finit un autre ndarray qui contiendra des valeurs calcul�es pour
    tracer un graphique, mais qui devra �tre effac� apr�s chaque changement
    de pourcentage de vaccination"""
    
    nVaccines = nMarcheurs * proportionVaccine[i]
    # On trouve le nombre de marcheurs vaccin�s

    for K in range(1, 6):
        # On effectue chaque simulation 10 fois
        
        np.random.seed() 
        # On fait l'initialisation du germe du generateur al�atoire

        x = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        y = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        # On d�finit les positions initiales des marcheurs

        etat = np.zeros(nMarcheurs, dtype='int')
    
        """On d�finit un ndarray d'�tat des marcheurs (0: sant�, 1: infect�
mobile, 2: mort contagieux et 3: mort non-contagieux)"""

        tempsVivant = np.zeros(nMarcheurs, dtype='int')
        tempsMort = np.zeros(nMarcheurs, dtype='int')
        # On d�finit deux ndarrays qui stockeront le temps d'infection restant

        premierInfecte = np.random.randint(0, nMarcheurs)
        # On s�lectionne le premier infect�
        etat[premierInfecte] = 1
        tempsVivant[premierInfecte] = dureeInfection
        # On l'infecte et on indique son temps d'infection restant

        nInfectes = 1
        nDejaInfecte = 1
        nIterations = 0
        nMorts = 0
        # On d�finit les compteurs d'infect�s, d'it�rations et de morts

        immunise = np.zeros(nMarcheurs, dtype='bool')
        immunise[:int(nVaccines) + 1] = True
        # On vaccine la proportion de population voulue

        while (nInfectes > 0) and (nIterations < nIterationsMax):
    
            """On ex�cute tant que le temps n'est pas �coul� ou qu'il ne reste
            plus d'infect�s"""

            iMobile, = (etat < 2).nonzero()
            # On trouve les indices des marcheurs vivants
            nMobile = iMobile.size
            # On trouve le nombre de marcheurs vivants

            rdm = np.random.randint(0, 4, nMobile)
            # On trouve des valeurs pour faire le test de direction du pas

            x[iMobile] = np.where(rdm == 0, x[iMobile] + 1, x[iMobile])
            y[iMobile] = np.where(rdm == 1, y[iMobile] + 1, y[iMobile])
            x[iMobile] = np.where(rdm == 2, x[iMobile] - 1, x[iMobile])
            y[iMobile] = np.where(rdm == 3, y[iMobile] - 1, y[iMobile])
        
            """On fait les test de direction du pas et le d�placement qui en
            d�coule"""

            x[iMobile] = np.clip(x[iMobile], 1, tailleReseau)
            y[iMobile] = np.clip(y[iMobile], 1, tailleReseau)
            # On s'assure que les marcheurs ne sortent pas de la grille

            for iInfecte in (np.logical_and(etat != 0, etat != 3)).nonzero()[0]:
                # On fait une boucle sur tous les marcheurs infect�s

                iPotentielNouvelInfecte, = ((x == x[iInfecte]) & (y == 
y[iInfecte]) & (etat == 0) & (immunise == False)).nonzero()
                
                """On trouve les indices des marcheurs qui seront peut-�tre
                infect�s"""

                rdm = np.random.random(iPotentielNouvelInfecte.size)
                iNouvelInfecte = iPotentielNouvelInfecte[(rdm <= 0.5).nonzero(
)[0]]
                """On fait le test d'infection pour chaque nouvel infect�
                potentiel"""

                nNouveauxInfectes = iNouvelInfecte.size
                # On trouve le nombre de marcheurs qui seront infect�s

                if nNouveauxInfectes > 0:

                    """La contagion n'a lieu que si au moins un nouveau
                    marcheur est infect�"""

                    etat[iNouvelInfecte] = 1
                    tempsVivant[iNouvelInfecte] = dureeInfection
                    # On infecte les nouveaux infect�s

                    nInfectes += nNouveauxInfectes
                    nDejaInfecte += nNouveauxInfectes
                    # On ajuste les compteurs d'infect�s
        
                tempsVivant[iInfecte] -= 1
                tempsMort[iInfecte] -= 1
                # On diminue le temps restant

                if tempsVivant[iInfecte].any() == 0:
                    # On v�rifie si le marcheur meurt ou s'en sort

                    iTempsVivant, = np.nonzero(tempsVivant[iInfecte] == 0)
                    
                    rdm = np.random.random(iTempsVivant.size)
                    # On a un ndarray qui servira au test de survie

                    iSurvie, = np.nonzero(rdm >= pMort)
                    nSurvies = iSurvie.size
                    iTue, = np.nonzero(rdm < pMort)
                    nTues = iTue.size

                    """On trouve quels marcheurs survivent et quels marcheurs
                    meurent et le nombre de chaque cat�gorie"""

                    if nSurvies != 0:
                        etat[iTempsVivant[iSurvie]] = 0
                        immunise[iTempsVivant[iSurvie]] = True
                        # On gu�rit le malade et on l'immunise

                    if nTues != 0:
                        etat[iTempsVivant[iTue]] = 2
                        tempsMort[iTempsVivant[iTue]] = dureeInfectionCadavre
                        nMorts += nTues
                        # On tue le marcheur et on le laisse �tre infect�

                    nInfectes -= nSurvies + nTues
                    # On ajuste le compteur d'infect�s

                if tempsMort[iInfecte].any() == 0:
                    etat[(tempsMort[iInfecte]).nonzero()[0]] = 3

            rdm = np.random.random()
            if rdm < pNouvelleSouche:
                # On teste si une nouvelle souche ne serait pas apparue
                immunise = np.zeros(nMarcheurs, dtype='bool')

            nIterations += 1

        cout = np.append(cout, nDejaInfecte * 100 + nVaccines * 50)
        tauxMortalite = np.append(tauxMortalite, nMorts / nMarcheurs)
        dureeEpidemie = np.append(dureeEpidemie, nIterations)

        """On trouve les valeurs pertinentes � ajouter aux ndarrays en vue
        des graphiques � tracer"""

    coutMoyen = np.append(coutMoyen, np.mean(cout))
    deviationCoutMoyen = np.append(deviationCoutMoyen, np.std(cout))
    tauxMortaliteMoyen = np.append(tauxMortaliteMoyen, np.mean(tauxMortalite))
    deviationTauxMortaliteMoyen = np.append(deviationTauxMortaliteMoyen,
np.std(tauxMortalite))
    dureeEpidemieMoyenne = np.append(dureeEpidemieMoyenne,
np.mean(dureeEpidemie))
    deviationDureeEpidemieMoyenne = np.append(deviationDureeEpidemieMoyenne,
np.std(dureeEpidemie))

    """On trouve les valeurs de moyennes et d'�cart standard pour chaque
    ndarray qui vont nous �tre utile pour tracer le graphique"""

    erreurProportionVaccine = np.append(erreurProportionVaccine,
abs(nVaccines - int(nVaccines)) / nMarcheurs)

plt.figure(0)

plt.plot(proportionVaccine, coutMoyen)

plt.xlabel('Proportion de la population vaccin�e')
plt.ylabel('Co�t moyen au gouvernement (en dollars)')
plt.errorbar(proportionVaccine, coutMoyen, yerr=deviationCoutMoyen,
xerr=erreurProportionVaccine)
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire10-figureQ4-1.png')

plt.figure(1)

plt.plot(proportionVaccine, tauxMortaliteMoyen, '-')

plt.xlabel('Proportion de la population vaccin�e')
plt.ylabel('Taux de mortalit� moyen (en morts/marcheurs)')
plt.errorbar(proportionVaccine, tauxMortaliteMoyen,
yerr=deviationTauxMortaliteMoyen, xerr=erreurProportionVaccine)
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire10-figureQ4-2.png')

plt.figure(2)

plt.plot(proportionVaccine, dureeEpidemieMoyenne, '-')

plt.xlabel('Proportion de la population vaccin�e')
plt.ylabel('Dur�e moyenne de l\'�pid�mie (en it�rations)')
plt.errorbar(proportionVaccine, dureeEpidemieMoyenne,
yerr=deviationDureeEpidemieMoyenne, xerr=erreurProportionVaccine)
# On modifie les param�tres esth�tiques du graphique

plt.savefig('Laboratoire10-figureQ4-3.png')

plt.show()