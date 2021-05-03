# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code simule la propagation d'une maladie mortelle et contagieuse
dans une population de marcheurs vacinnés à certains taux variables. Il
montre ensuite quelques graphiques pour représenter la situation d'un
point de vue économique et humain."""

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
# On définit des paramètres de départ

coutMoyen = np.array([])
deviationCoutMoyen = np.array([])
erreurProportionVaccine = np.array([])
tauxMortaliteMoyen = np.array([])
deviationTauxMortaliteMoyen = np.array([])
dureeEpidemieMoyenne = np.array([])
deviationDureeEpidemieMoyenne = np.array([])

"""On définit une série de ndarray qui contiendront des valeurs calculées en
vue de produire les graphiques"""

proportionVaccine = np.linspace(0, 1, 11)

"""On fait un ndarray qui parcourt l'ensemble du domaine des proportions de
vaccination possible"""

for i in range(0, proportionVaccine.size):
    # On exécute la simulation pour chaque densité de population

    cout = np.array([])
    tauxMortalite = np.array([])
    dureeEpidemie = np.array([])
    
    """On définit un autre ndarray qui contiendra des valeurs calculées pour
    tracer un graphique, mais qui devra être effacé après chaque changement
    de pourcentage de vaccination"""
    
    nVaccines = nMarcheurs * proportionVaccine[i]
    # On trouve le nombre de marcheurs vaccinés

    for K in range(1, 6):
        # On effectue chaque simulation 10 fois
        
        np.random.seed() 
        # On fait l'initialisation du germe du generateur aléatoire

        x = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        y = np.random.randint(1, tailleReseau + 1, nMarcheurs)
        # On définit les positions initiales des marcheurs

        etat = np.zeros(nMarcheurs, dtype='int')
    
        """On définit un ndarray d'état des marcheurs (0: santé, 1: infecté
mobile, 2: mort contagieux et 3: mort non-contagieux)"""

        tempsVivant = np.zeros(nMarcheurs, dtype='int')
        tempsMort = np.zeros(nMarcheurs, dtype='int')
        # On définit deux ndarrays qui stockeront le temps d'infection restant

        premierInfecte = np.random.randint(0, nMarcheurs)
        # On sélectionne le premier infecté
        etat[premierInfecte] = 1
        tempsVivant[premierInfecte] = dureeInfection
        # On l'infecte et on indique son temps d'infection restant

        nInfectes = 1
        nDejaInfecte = 1
        nIterations = 0
        nMorts = 0
        # On définit les compteurs d'infectés, d'itérations et de morts

        immunise = np.zeros(nMarcheurs, dtype='bool')
        immunise[:int(nVaccines) + 1] = True
        # On vaccine la proportion de population voulue

        while (nInfectes > 0) and (nIterations < nIterationsMax):
    
            """On exécute tant que le temps n'est pas écoulé ou qu'il ne reste
            plus d'infectés"""

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
        
            """On fait les test de direction du pas et le déplacement qui en
            découle"""

            x[iMobile] = np.clip(x[iMobile], 1, tailleReseau)
            y[iMobile] = np.clip(y[iMobile], 1, tailleReseau)
            # On s'assure que les marcheurs ne sortent pas de la grille

            for iInfecte in (np.logical_and(etat != 0, etat != 3)).nonzero()[0]:
                # On fait une boucle sur tous les marcheurs infectés

                iPotentielNouvelInfecte, = ((x == x[iInfecte]) & (y == 
y[iInfecte]) & (etat == 0) & (immunise == False)).nonzero()
                
                """On trouve les indices des marcheurs qui seront peut-être
                infectés"""

                rdm = np.random.random(iPotentielNouvelInfecte.size)
                iNouvelInfecte = iPotentielNouvelInfecte[(rdm <= 0.5).nonzero(
)[0]]
                """On fait le test d'infection pour chaque nouvel infecté
                potentiel"""

                nNouveauxInfectes = iNouvelInfecte.size
                # On trouve le nombre de marcheurs qui seront infectés

                if nNouveauxInfectes > 0:

                    """La contagion n'a lieu que si au moins un nouveau
                    marcheur est infecté"""

                    etat[iNouvelInfecte] = 1
                    tempsVivant[iNouvelInfecte] = dureeInfection
                    # On infecte les nouveaux infectés

                    nInfectes += nNouveauxInfectes
                    nDejaInfecte += nNouveauxInfectes
                    # On ajuste les compteurs d'infectés
        
                tempsVivant[iInfecte] -= 1
                tempsMort[iInfecte] -= 1
                # On diminue le temps restant

                if tempsVivant[iInfecte].any() == 0:
                    # On vérifie si le marcheur meurt ou s'en sort

                    iTempsVivant, = np.nonzero(tempsVivant[iInfecte] == 0)
                    
                    rdm = np.random.random(iTempsVivant.size)
                    # On a un ndarray qui servira au test de survie

                    iSurvie, = np.nonzero(rdm >= pMort)
                    nSurvies = iSurvie.size
                    iTue, = np.nonzero(rdm < pMort)
                    nTues = iTue.size

                    """On trouve quels marcheurs survivent et quels marcheurs
                    meurent et le nombre de chaque catégorie"""

                    if nSurvies != 0:
                        etat[iTempsVivant[iSurvie]] = 0
                        immunise[iTempsVivant[iSurvie]] = True
                        # On guérit le malade et on l'immunise

                    if nTues != 0:
                        etat[iTempsVivant[iTue]] = 2
                        tempsMort[iTempsVivant[iTue]] = dureeInfectionCadavre
                        nMorts += nTues
                        # On tue le marcheur et on le laisse être infecté

                    nInfectes -= nSurvies + nTues
                    # On ajuste le compteur d'infectés

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

        """On trouve les valeurs pertinentes à ajouter aux ndarrays en vue
        des graphiques à tracer"""

    coutMoyen = np.append(coutMoyen, np.mean(cout))
    deviationCoutMoyen = np.append(deviationCoutMoyen, np.std(cout))
    tauxMortaliteMoyen = np.append(tauxMortaliteMoyen, np.mean(tauxMortalite))
    deviationTauxMortaliteMoyen = np.append(deviationTauxMortaliteMoyen,
np.std(tauxMortalite))
    dureeEpidemieMoyenne = np.append(dureeEpidemieMoyenne,
np.mean(dureeEpidemie))
    deviationDureeEpidemieMoyenne = np.append(deviationDureeEpidemieMoyenne,
np.std(dureeEpidemie))

    """On trouve les valeurs de moyennes et d'écart standard pour chaque
    ndarray qui vont nous être utile pour tracer le graphique"""

    erreurProportionVaccine = np.append(erreurProportionVaccine,
abs(nVaccines - int(nVaccines)) / nMarcheurs)

plt.figure(0)

plt.plot(proportionVaccine, coutMoyen)

plt.xlabel('Proportion de la population vaccinée')
plt.ylabel('Coût moyen au gouvernement (en dollars)')
plt.errorbar(proportionVaccine, coutMoyen, yerr=deviationCoutMoyen,
xerr=erreurProportionVaccine)
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire10-figureQ4-1.png')

plt.figure(1)

plt.plot(proportionVaccine, tauxMortaliteMoyen, '-')

plt.xlabel('Proportion de la population vaccinée')
plt.ylabel('Taux de mortalité moyen (en morts/marcheurs)')
plt.errorbar(proportionVaccine, tauxMortaliteMoyen,
yerr=deviationTauxMortaliteMoyen, xerr=erreurProportionVaccine)
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire10-figureQ4-2.png')

plt.figure(2)

plt.plot(proportionVaccine, dureeEpidemieMoyenne, '-')

plt.xlabel('Proportion de la population vaccinée')
plt.ylabel('Durée moyenne de l\'épidémie (en itérations)')
plt.errorbar(proportionVaccine, dureeEpidemieMoyenne,
yerr=deviationDureeEpidemieMoyenne, xerr=erreurProportionVaccine)
# On modifie les paramètres esthétiques du graphique

plt.savefig('Laboratoire10-figureQ4-3.png')

plt.show()