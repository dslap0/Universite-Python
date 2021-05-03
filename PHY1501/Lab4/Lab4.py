# -.- coding:latin1 -.-
# @author: Nicolas
""" Ce code produit les résultats et les graphiques voulus pour le
laboratoire 4, portant sur les circuits RLC.
"""

import numpy as np
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

def traitement(nomDuFichier):
    """ Fichier qui lis un document texte contenant les résultats d'une 
    expérience et retourne le temps et la pression p1 après l'avoir lu.
    nomDuFichier : Nom du fichier à lire (string).
    """
    t = []
    p1 = []
    # On crée les trois listes vides t, p1 et p2

    fichier = open(nomDuFichier, 'r')
    for ligne in fichier:
        if not ligne.startswith('#'):
            # On ne prend en compte que les lignes qui ne commencent pas par #
            tempsPression = fichier.read().replace('\n', '	').split('	')
            # Chaque élément du fichier est contenu dans cette liste
    fichier.close()

    # On enlève les éléments vides de la liste
    tempsPression = list(filter(None, tempsPression))

    for i in range(0, len(tempsPression)):

        # On crée une boucle qui met les éléments dans 3 listes différentes 
        # (t, p1 ou p2) selon leur position dans la liste tempsPosition

        if i % 3 == 0:
            t.append(float(tempsPression[i]))
        elif i % 3 == 1:
            p1.append(float(tempsPression[i]))

    # On transforme les listes en array
    t = np.array(t, dtype='float64')
    p1 = np.array(p1, dtype='float64')

    # On transforme la pression en Pa au lieu d'en kPa
    p1 *= 1e3

    return t, p1

def erreur(t, p):
    """ Fonction qui trouve l'incertitude sur la pression en se servant
    de la pression la plus haute lors de l'expérience c) 2-.
    t : Temps (ndarray de float).
    p : Pression la plus éléevée enregistrée (ndarray de float).
    """
    # On trouve à quel indice la pression stagne
    i = (np.abs(t - 200)).argmin()
    j = (np.abs(t - 300)).argmin()

    # On fait la moyenne entre ces points dans p1
    moy = np.mean(p[i:j])

    # On trouve l'incertitude sur la pression
    errP = max(moy - p[i:j].min(), p[i:j].max() - moy)

    return errP

def question1(nomDuFichier, d, errP):
    """ Ce code vise à obtenir le libre-parcours moyen et la pression 
    moyenne moyenne (ainsi que leurs incertitudes repectives) à partir 
    d'un fichier texte regroupant les mesures prises lors de 
    l'expérience.
    nomDuFichier : Nom du fichier à analyser (string).
    d : Diamètre efficace des molécules (float, en m)
    """
    t = []
    p1 = []
    p2 = []
    # On crée les trois listes vides t, p1 et p2

    fichier = open(nomDuFichier, 'r')
    for ligne in fichier:
        if not ligne.startswith('#'):
            # On ne prend en compte que les lignes qui ne commencent pas par #
            tempsPression = fichier.read().replace('\n', '	').split('	')
            # Chaque élément du fichier est contenu dans cette liste
    fichier.close()

    # On enlève les éléments vides de la liste
    tempsPression = list(filter(None, tempsPression))

    for i in range(0, len(tempsPression)):

        # On crée une boucle qui met les éléments dans 3 listes différentes 
        # (t, p1 ou p2) selon leur position dans la liste tempsPosition

        if i % 3 == 0:
            t.append(float(tempsPression[i]))
        elif i % 3 == 1:
            p1.append(float(tempsPression[i]))
        else:
            p2.append(float(tempsPression[i]))

    # On transforme les listes en array
    t = np.array(t, dtype='float64')
    p1 = np.array(p1, dtype='float64')
    p2 = np.array(p2, dtype='float64')

    # On transforme les pressions en Pa au lieu d'en kPa
    p1 *= 1e3
    p2 *= 1e3

    # On trouve la pression moyenne à chaque point
    pm = (p1 + p2) / 2

    # On trouve la moyenne des pressions moyennes et son erreur
    pmm = np.mean(pm)
    errPmm = np.std(pm)

    # On trouve le libre parcours moyen et son erreur
    l = (293.15 * 1.38e-23) / (np.pi * d ** 2 * pmm * np.sqrt(2))
    errL = (293.15 * 1.38e-23 * errP) / (np.pi * d ** 2 * pmm ** 2 * 
    np.sqrt(2))

    # On trouve tous les (p1(t) - pm) / (p1(0) - pm) et leur erreur
    y = (p1 - pmm) / (p1[0] - pmm)
    errY = np.sqrt((errP / (p1[0] - pmm)) ** 2 + ((p1[0] - p1) * 
    errPmm / (p1[0] - pmm) ** 2) ** 2 + ((p1 - pmm) * errP / (p1[0] - 
    pmm) ** 2) ** 2)
    
    return l, errL, pmm, errPmm, t, y, errY

def theo2(t, tau):
    """ Fonction qui trouve la valeur de (p1(t) - pm) / (p1(0) - pm) à
    l'aide de la constante de temps et du temps.
    t : Temps (ndarray de float).
    tau : Constante de temps (ndarray de float).
    """
    return np.exp(-t / tau)

def question2(nomFig, numFig, *args):
    """ On trace les graphiques de la question 2, soit 
    (p1(t) - pm) / (p1(0) - pm) en fonction de t, et on renvoie les taus
    produit par curve_fit.
    nomFig : Nom de la figure (string).
    numFig : Numéro de la figure (int).
    *args : Contient un nombre indéterminé de tuple dont le premier 
    élément est le titre de la courbe (string), le deuxième élément est 
    la couleur de la courbe (string), le troisième élément est les temps 
    (ndarray de float), le quatrième élément est les 
    (p1(t) - pm) / (p1(0) - pm) (ndarray de floats) et les deux derniers 
    éléments sont les temps à partir desquels il faut tracer la courbe 
    théorique (float).
    """
    # On ouvre la figure
    plt.figure(numFig)
    
    # On déclare l'array où on mettera les autres taus et celui des erreurs
    arrTau = np.array([])
    errArrTau = np.array([])

    for arg in args:
        # On déballe les arguments
        titre, couleur, t, y, errY, t1, t2 = arg

        # On trouve la position d'où raccourcir les arrays au début
        i = (np.abs(t - t1)).argmin()

        # On enlève les premières secondes d'inaction
        t = t[i:]
        t -= t[0]
        y = y[i:]
        errY = errY[i:]

        # On met les barres d'erreurs à 25 points
        t10 = np.array([])
        y10= np.array([])
        errY10 = np.array([])
        saut = int(len(y) / 10)
        i = 0
        while i < len(y):
            t10 = np.append(t10, t[i])
            y10 = np.append(y10, y[i])
            errY10 = np.append(errY10, errY[i])
            i += saut

        # On met les points sur le graphique et leurs incertitudes
        plt.plot(t, y, '.', color=couleur, ms=2, label=titre)
        plt.errorbar(t10, y10, errY10, ls='None', color=couleur)

        # On trouve la position d'où on doit arrêter de tracer curve_fit
        i = (np.abs(t - t2)).argmin()

        # On trouve le paramètre optimisé et son incertitude
        tau, cov = curve_fit(theo2, t[:i], y[:i], sigma=errY[:i])
        errTau = np.sqrt(cov)

        # On trouve la courbe curve_fit résultante
        ytheo = theo2(t[:i], tau)

        plt.plot(t[:i], ytheo[:i], color=couleur)

        # On emballe les taus pour les passer en dehors de la boucle
        arrTau = np.append(arrTau, tau)
        errArrTau = np.append(errArrTau, errTau)
    
    # On modifie les paramètres esthétiques de la fonction    
    plt.xlabel('Temps écoulé (s)')
    plt.ylabel(r'$\frac{p_1(t)-p_{moy}}{p_1(0)-p_{moy}}$')
    plt.yscale('log')
    plt.legend()

    plt.savefig(nomFig)

    return arrTau, errArrTau

def theo3(var, cste1, cste2):
    """ Cette fonction nous donne la valeur théorique de la constante de
    temps en fonction d'un certain paramètre.
    var : Paramètre étudié (ndarray de floats).
    cste1 : Facteur de proportionnalité entre 1 / pmm et tau (float).
    cste2 : Ordonnée à l'origine de la droite (float).
    """
    return cste1 * var + cste2

def question3(nomFig, numFig, tau, errTau, var, errVar, legende, xTitre):
    """ Ce code permet de tracer tous les graphiques nécessaires pour 
    répondre à la question 3.
    nomFig : Nom de la figure (string).
    numFig : Numéro de la figure (int).
    tau : Constantes de temps obtenues avec curve_fit à la question 2 
    (ndarray de floats).
    errTau : Erreur sur les constantes de temps obtenues avec curve_fit
    à la question 2 (ndarray de floats).
    var : Variable étudiée en rapport avec tau (ndarray de floats).
    errVar : Erreur sur la variable étudiée en rapport avec tau (ndarray 
    de floats ou string)
    legende : Légende des points du graphique (string).
    xTitre : Titre de l'axe des x (string).
    """
    plt.figure(numFig)

    plt.plot(var, tau, '.b', label=legende)
    
    # On trouve la constante de proportionnalité et son erreur
    if errVar.any() == False:
        cstes, cov = curve_fit(theo3, var, tau)
    else: 
        cstes, cov =  curve_fit(theo3, var, tau, sigma=errVar)
    cste1, cste2 = cstes
    errCste1, errCste2 = np.sqrt(np.diag(cov))

    # On trace la courbe théorique
    tauTheo = theo3(var, cste1, cste2)
    plt.plot(var, tauTheo, '-b', label='Courbe théorique curve_fit', markersize=2)

    # On modifie les options esthétiques du graphiques
    if errVar.any() == False:
        plt.errorbar(var, tau, errTau, ls='None')
    else:
        plt.errorbar(var, tau, errTau, errVar, ls='None')
    plt.xlabel(xTitre)
    plt.ylabel('Constante de temps (s)')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.legend()
    
    plt.savefig(nomFig)

    return cste1, errCste1, cste2, errCste2


# On fixe des constantes
dN = 3.15e-10
dAr = 2.88e-10
dCO_2 = 3.34e-10

# On trouve l'incertitude sur la pression
tC2, p1C2 = traitement('labo005.txt')
errP = erreur(tC2, p1C2)

# On trouve tous les parcours libres moyens et les pressions moyennes
lA1, errLA1, pmmA1, errPmmA1, tA1, yA1, errYA1 = \
    question1('Emilie001.txt', dN, errP)
lA2, errLA2, pmmA2, errPmmA2, tA2, yA2, errYA2 = \
    question1('Emilie002.txt', dN, errP)
lA3, errLA3, pmmA3, errPmmA3, tA3, yA3, errYA3 = \
    question1('Emilie003.txt', dN, errP)
lA4, errLA4, pmmA4, errPmmA4, tA4, yA4, errYA4 = \
    question1('Emilie004.txt', dN, errP)
lB1, errLB1, pmmB1, errPmmB1, tB1, yB1, errYB1 = \
    question1('labo001.txt', dN, errP)
lB2, errLB2, pmmB2, errPmmB2, tB2, yB2, errYB2 = \
    (lA2, errLA2, pmmA2, errPmmA2, tA2, yA2, errYA2)
lB3, errLB3, pmmB3, errPmmB3, tB3, yB3, errYB3 = \
    question1('labo002.txt', dN, errP)
lC1, errLC1, pmmC1, errPmmC1, tC1, yC1, errYC1 = \
    question1('labo006.txt', dN, errP)
lC2, errLC2, pmmC2, errPmmC2, tC2, yC2, errYC2 = \
    question1('labo005.txt', dN, errP)
lC3, errLC3, pmmC3, errPmmC3, tC3, yC3, errYC3 = \
    question1('labo004.txt', dN, errP)
lC4, errLC4, pmmC4, errPmmC4, tC4, yC4, errYC4 = \
    question1('labo003.txt', dN, errP)
lD1, errLD1, pmmD1, errPmmD1, tD1, yD1, errYD1 = \
    question1('Emilie005.txt', dAr, errP)
lD2, errLD2, pmmD2, errPmmD2, tD2, yD2, errYD2 = \
    (lA2, errLA2, pmmA2, errPmmA2, tA2, yA2, errYA2)
lD3, errLD3, pmmD3, errPmmD3, tD3, yD3, errYD3 = \
    question1('Emilie006.txt', dCO_2, errP)

# On montre les libres parcours moyens et les pressions moyennes
print("      l (m)                                        Pmoy (Pa)")
print("a) 1- " + str(lA1) + " +/- " + str(errLA1) + " " + str(pmmA1) + 
" +/- " + str(errPmmA1))
print("a) 2- " + str(lA2) + " +/- " + str(errLA2) + " " + str(pmmA2) +
" +/- " + str(errPmmA2))
print("a) 3- " + str(lA3) + " +/- " + str(errLA3) + " " + str(pmmA3) +
" +/- " + str(errPmmA3))
print("a) 4- " + str(lA4) + " +/- " + str(errLA4) + " " + str(pmmA4) +
" +/- " + str(errPmmA4))
print("b) 1- " + str(lB1) + " +/- " + str(errLB1) + " " + str(pmmB1) +
" +/- " + str(errPmmB1))
print("b) 2- " + str(lB2) + " +/- " + str(errLB2) + " " + str(pmmB2) +
" +/- " + str(errPmmB2))
print("b) 3- " + str(lB3) + " +/- " + str(errLB3) + " " + str(pmmB3) +
" +/- " + str(errPmmB3))
print("c) 1- " + str(lC1) + " +/- " + str(errLC1) + " " + str(pmmC1) +
" +/- " + str(errPmmC1))
print("c) 2- " + str(lC2) + " +/- " + str(errLC2) + " " + str(pmmC2) +
" +/- " + str(errPmmC2))
print("c) 3- " + str(lC3) + " +/- " + str(errLC3) + " " + str(pmmC3) +
" +/- " + str(errPmmC3))
print("c) 4- " + str(lC4) + " +/- " + str(errLC4) + " " + str(pmmC4) +
" +/- " + str(errPmmC4))
print("d) 1- " + str(lD1) + " +/- " + str(errLD1) + " " + str(pmmD1) +
" +/- " + str(errPmmD1))
print("d) 2- " + str(lD2) + " +/- " + str(errLD2) + " " + str(pmmD2) +
" +/- " + str(errPmmD2))
print("d) 3- " + str(lD3) + " +/- " + str(errLD3) + " " + str(pmmD3) +
" +/- " + str(errPmmD3))
print("")

# On prépare les données pour la fonction qui trace les graphiques
argsA1 = (r'$P_1=2.5$ kPa et $P_2=0.1$ kPa', 'b', tA1, yA1, errYA1, 0, 150)
argsA2 = (r'$P_1=5.0$ kPa et $P_2=2.5$ kPa', 'r', tA2, yA2, errYA2, 0, 50)
argsA3 = (r'$P_1=7.5$ kPa et $P_2=5.0$ kPa', 'g', tA3, yA3, errYA3, 0, 100)
argsA4 = (r'$P_1=12.5$ kPa et $P_2=10$ kPa', 'y', tA4, yA4, errYA4, 1.5, 60)
argsB1 = (r'$r_0=2.00$ mm', 'b', tB1, yB1, errYB1, 0, 60)
argsB2 = (r'$r_0=1.55$ mm', 'r', tB2, yB2, errYB2, 0, 50)
argsB3 = (r'$r_0=0.81$ mm', 'g', tB3, yB3, errYB3, 0, 500)
argsC1 = (r'$P_1=2.5$ kPa et $P_2=0.1$ kPa', 'b', tC1, yC1, errYC1, 0, 150)
argsC2 = (r'$P_1=5.0$ kPa et $P_2=2.5$ kPa', 'r', tC2, yC2, errYC2, 0, 150)
argsC3 = (r'$P_1=7.5$ kPa et $P_2=5.0$ kPa', 'g', tC3, yC3, errYC3, 0, 150)
argsC4 = (r'$P_1=12.5$ kPa et $P_2=10$ kPa', 'y', tC4, yC4, errYC4, 0, 150)
argsD1 = ('Argon', 'b', tD1, yD1, errYD1, 3, 75)
argsD2 = ('Air (~ Azote)', 'r', tD2, yD2, errYD2, 0, 50)
argsD3 = (r'$CO_2$', 'g', tD3, yD3, errYD3, 1.2, 50)

# On trace les graphiques et on prend les taus et leurs incertitudes
tauA, errTauA = question2('Lab4_Fig2A.png', 1, argsA1, argsA2, argsA3, argsA4)
tauB, errTauB = question2('Lab4_Fig2B.png', 2, argsB1, argsB2, argsB3)
tauC, errTauC = question2('Lab4_Fig2C.png', 3, argsC1, argsC2, argsC3, argsC4)
tauD, errTauD = question2('Lab4_Fig2D.png', 4, argsD1, argsD2, argsD3)

# On donne les résultats des pentes des graphiques de la question 2
print("Voici les résultats de la question 2:")
print("      tau (s)")
for i in range(0, len(tauA)):
    print("a) " + str(i + 1) + "- " + str(tauA[i]) + " +/- " + str(errTauA[i]))
for i in range(0, len(tauB)):
    print("b) " + str(i + 1) + "- " + str(tauB[i]) + " +/- " + str(errTauB[i]))
for i in range(0, len(tauC)):
    print("c) " + str(i + 1) + "- " + str(tauC[i]) + " +/- " + str(errTauC[i]))
for i in range(0, len(tauD)):
    print("d) " + str(i + 1) + "- " + str(tauD[i]) + " +/- " + str(errTauD[i]))
print("")

# On emballe les paramètres et leur incertitude pour la question 3 et on les 
# prépare
pmmA = np.array([pmmA1, pmmA2, pmmA3, pmmA4])
errPmmA = np.array([errPmmA1, errPmmA2, errPmmA3, errPmmA4])
pmmAMod = 1 / pmmA
errPmmAMod = errPmmA / pmmA ** 2
r0B = np.array([2e-3, 1.55e-3, 0.81e-3])
r0BMod = 1 / r0B ** 4
errR0BMod = np.array([False])
pmmC = np.array([pmmC1, pmmC2, pmmC3, pmmC4])
errPmmC = np.array([errPmmC1, errPmmC2, errPmmC3, errPmmC4])
pmmCMod = 1 / pmmC
errPmmCMod = errPmmC / pmmC ** 2
etaD = np.array([22.2e-6, 17.2e-6, 14.7e-6])
errEtaD = np.array([False])

# On trace les graphiques de la question 3
csteA1, errCsteA1, csteA2, errCsteA2 = question3('Lab4_Fig3A.png', 5, tauA, 
errTauA, pmmAMod, errPmmAMod, r"$\tau$ en fonction de $\frac{1}{p_m}$", 
r"$\frac{1}{p_m}$ ($kPa^{-1}$)")
csteB1, errCsteB1, csteB2, errCsteB2 = question3('Lab4_Fig3B.png', 6, tauB, 
errTauB, r0BMod, errR0BMod, r"$\tau$ en fonction de $\frac{1}{{r_0}^4}$", 
r"$\frac{1}{{r_0}^4}$ ($m^{-4}$)")
csteC1, errCsteC1, csteC2, errCsteC2 = question3('Lab4_Fig3C.png', 7, tauC, 
errTauC, pmmCMod, errPmmCMod, r"$\tau$ en fonction de $\frac{1}{p_m}$", 
r"$\frac{1}{p_m}$ ($kPa^{-1}$)")
csteD1, errCsteD1, csteD2, errCsteD2 = question3('Lab4_Fig3D.png', 8, tauD, 
errTauD, etaD, errEtaD, r"$\tau$ en fonction de $\eta$", r"$\eta$ (Pa s)")

print("Voici les résultats de la question 3:")
print("    Taux de variation (unités à trouver)     Ordonnée à l'origine (s)")
print("a) " + str(csteA1) + " +/- " + str(errCsteA1) + " " + str(csteA2) + 
" +/- " + str(errCsteA2))
print("b) " + str(csteB1) + " +/- " + str(errCsteB1) + " " + str(csteB2) + 
" +/- " + str(errCsteB2))
print("c) " + str(csteC1) + " +/- " + str(errCsteC1) + " " + str(csteC2) + 
" +/- " + str(errCsteC2))
print("d) " + str(csteD1) + " +/- " + str(errCsteD1) + " " + str(csteD2) + 
" +/- " + str(errCsteD2))
print("")

plt.show()
