# -.- coding:latin1 -.-
# @author: Nicolas
""" Ce code produit les résultats et les graphiques voulus pour le
laboratoire 1, portant sur les circuits RLC.
"""
import numpy as np

import matplotlib.pyplot as plt


def moyEtIncert(array):
    """ Cette fonction calcule la moyenne et la déviation standard des
    valeurs sur celle-ci dans un array de minimum 2D.
    array : ndarray 2D (ou plus) dont il faut trouver la moyenne et la
    déviation standard.
    """
    # On fait les calculs demandés
    moy = np.mean(array, axis=0)
    incert = np.std(array, axis=0)

    # On donne ces valeurs à l'utilisateur
    return moy, incert

def calculVSurE(V, E, incertV, incertE):
    """ Cette fonction calcule la chute de tension sur la tension et son
    incertitude.
    V : Chute de tension du circuit (ndarray de float, en V).
    E : Tension du circuit (ndarray de float, en V).
    incertV : Incertitude sur la chute de tension (ndarray de float, en
    V).
    incertE : Incertitude sur la tension (float, en V).
    """
    VSurE = V / E
    incertVSurE = np.sqrt((incertV / E) ** 2 + (incertE * V / E ** 2) ** 2)

    return VSurE, incertVSurE

def calculPhi(deltaT, periode, incertDeltaT, incertPeriode):
    """ Cette fonction permet de calculer le déphasage du circuit et son
    incertitude.
    deltaT : Différence de temps entre deux crêtes (ndarray de float, en 
    s).
    periode : Temps entre deux crêtes (ndarray de float, en s).
    incertDeltaT : Incertitude sur la différence de temps entre deux 
    crêtes (ndarray de float, en s).
    incertPeriode : Incertitude sur le temps entre deux crêtes (ndarray 
    de float, en s).
    """
    phi = -2 * np.pi * deltaT / periode
    incertPhi = np.sqrt((-2 * np.pi * incertDeltaT / periode) ** 2 + 
    (-2 * np.pi * incertPeriode * deltaT / periode ** 2) ** 2)

    return phi, incertPhi

def calculPeriode(f, incertF):
    """ Cette fonction sert à calculer des périodes et leurs 
    incertitudes.
    f : Fréquence du système (ndarray de float, en Hz).
    incertF : Incertitude sur la fréquence (ndarray de float, en Hz).
    """
    periode = 1 / f
    incertPeriode = incertF / f ** 2

    return periode, incertPeriode

def calculOmega(f, incertF):
    """ Cette fonction sert à trouver la fréquence angulaire d'un
    système.
    f : Fréquence du système (ndarray de float, en Hz).
    incertF : Incertitude sur la fréquence (ndarray de float, en Hz).
    """
    omega = 2 * np.pi * f
    incertOmega = 2 * np.pi * incertF
    
    return omega, incertOmega

def traceGraph(omega, phi, VSurE, incertOmega, incertPhi, incertVSurE, VSurETh,
phiTh):
    """ Cette fonction trace le graphique d'un circuit RLC avec le
    déphasage en fonction de la fréquence angulaire sur un axe et la 
    chute de tension sur la tension en fonction de la fréquence 
    angulaire sur l'autre axe.
    omega : Fréquence angulaire du système (ndarray de float, en rad/s).
    phi : Déphasage du circuit (ndarray de float, en rad).
    VSurE : Chute de tension sur la tension dans le circuit (ndarray de
    float).
    incertOmega : Incertitude sur la fréquence angulaire (ndarray de 
    float, en rad/s).
    incertPhi : Incertitude sur le déphasage (ndarray de float, en rad)
    incertVSurE : Incertitude de la chute de tension sur la tension dans
    le circuit (ndarray de float).
    VSurETh : Chute de tension sur la tension théorique (ndarray de
    float).
    phiTh : Déphasage théorique (ndarray de float).
    """
    # On trace le déphasage par rapport à omega et on ajuste les paramètres
    # graphiques
    plt.plot(omega, phi, 'dr', label=r'$\varphi$ expérimental')
    plt.plot(omega, phiTh, 'r', label=r'$\varphi$ théorique')
    plt.xscale('log')
    plt.xlabel(r'$\omega$ (rad)')
    plt.ylabel(r'$\varphi$')
    plt.errorbar(omega, phi, incertPhi, incertOmega, ls='None', color='r')
    plt.legend(loc='center right')
    
    plt.twinx()

    # On trace la chute de tension sur la tension par rapport à omega et on
    # ajuste les paramètres graphiques
    plt.plot(omega, VSurE, 'db', label=r'$\frac{V}{E}$ expérimental')
    plt.plot(omega, VSurETh, '-b', label=r'$\frac{V}{E}$ théorique')
    plt.ylabel(r'$\frac{V}{E}$')
    plt.errorbar(omega, VSurE, incertVSurE, incertOmega, ls='None', color='b')
    plt.legend(loc='center left')
    

"""On déclare ici les données expérimentales et leurs incertitudes:"""

# On trouve les fréquences expérimentale et leurs incertitudes
fMesureCircRC = np.array([[99.5, 142.9, 208.3, 294.1, 416.7, 625, 877.2, 1282, 
1786, 2609, 3731, 5319, 7813, 11110, 16030, 22730, 31390, 46300, 67570, 92590],
[100.5, 147.1, 199.5, 297.6, 423.7, 641, 892.9, 1316, 1818, 2688, 3788, 5935,
7937, 11290, 16390, 23580, 33330, 48080, 69990, 109200]])
fCircRC, incertFCircRC = moyEtIncert(fMesureCircRC)
fCircRL1 = np.append(fCircRC[:11], fCircRC[-1])
incertFCircRL1 = np.append(incertFCircRC[:11], incertFCircRC[-1])
fCircRL2 = np.append(fCircRC[:17], fCircRC[-1])
incertFCircRL2 = np.append(incertFCircRC[:17], incertFCircRC[-1])
fCircRLC1 = np.array([100., 143.8, 206.9, 297.6, 428.1, 615.8, 885.9, 1274.3, 
1833., 2429., 2529., 2629., 2729., 2829., 2929., 3029., 3129., 3229., 3329., 
3429., 3529., 3629., 3729., 3829., 3929., 4029., 4129., 4229., 4329., 4429., 
5456., 7848., 11288., 16238., 23357., 100000])
incertFCircRLC1 = np.append(incertFCircRC[: 9], np.ones(21) * 
incertFCircRC[11])
incertFCircRLC1 = np.append(incertFCircRLC1, incertFCircRC[-6:])
fCircRLC2 = np.array([100., 144., 207., 298., 428., 616., 886., 1274., 1471., 
1571., 1671., 1771., 1871., 1971., 2071., 2171., 2271., 2371., 2471., 2571., 
2671., 2771., 2871., 2971., 3071., 3171., 3271., 3371., 3471., 3793., 5456., 
7848.,  11288., 16238., 23357., 33598., 48329., 69519., 100000.])
incertFCircRLC2 = np.append(incertFCircRC[: 8], np.ones(21) * 
incertFCircRC[10])
print(incertFCircRC[11])
incertFCircRLC2 = np.append(incertFCircRLC2, incertFCircRC[-10:])

# On déclare les tensions et leurs incertitudes
ECircRC = np.array([[3.5326, 3.5325, 3.5322, 3.5313, 3.5296, 3.5265, 5.5205,
3.5095, 3.4911, 3.4651, 3.4347, 3.4060, 3.3852, 3.3736, 3.3686, 3.3666, 3.3660,
3.3662, 3.3670, 3.3679], [3.5324, 3.5324, 3.5323, 3.5321, 3.5316, 3.5307,
3.5291, 3.5269, 3.5248, 3.5231, 3.5207, 3.5168, 3.5135, 3.5123, 3.5130, 3.5138, 
3.5146, 3.5159, 3.5169, 3.5181]])
ECircRL1 = np.array([3.864, 3.3979, 3.4165, 3.4422, 3.4703, 3.4947, 3.5119,
3.5226, 3.5292, 3.5331, 3.5341, 3.5356])
ECircRL2 = np.array([3.513, 3.513, 3.513, 3.5131, 3.5132, 3.5135, 3.5137, 
3.5145, 3.5159, 3.5179, 3.5189, 3.5190, 3.5195, 3.5222, 3.5250, 3.5285, 3.5301, 
3.5317])
ECircRLC1 = np.array([7.0626, 7.0269, 7.0628, 7.0627, 7.0629, 7.0631, 7.0636,
7.0646, 7.0657, 7.0632, 7.0617, 7.0593, 7.056, 7.051, 7.0426, 7.0281, 7.0011, 
6.9479, 6.8554, 6.7916, 6.8478, 6.9273, 6.9788, 7.0083, 7.0257, 7.0365, 7.0434, 
7.0481, 7.0514, 7.0538, 7.06, 7.0575, 7.0569, 7.0587, 7.0608, 7.0718])
ECircRLC2 = np.array([7.062, 7.0621, 7.0621, 7.0621, 7.062, 7.0617, 7.0605, 
7.0559, 7.0502, 7.0455, 7.0387, 7.0288, 7.0136, 6.9891, 6.9486, 6.8781, 6.7589, 
6.5957, 6.5007, 6.5832, 6.7262, 6.8342, 6.9032, 6.9470, 6.9754, 6.9953, 7.0095, 
7.0197, 7.0272, 7.0426, 7.0566, 7.0557, 7.0558, 7.0581, 7.0602, 7.0623, 7.0652, 
7.0680, 7.0712])
incertE = 0.01

# On déclare les chutes de tension et leurs incertitudes
VCircRC = np.array([[0.11028, 0.15869, 0.22781, 0.32712, 0.46748, 0.66600, 
0.93853, 1.2968, 1.7330, 2.2002, 2.6204, 2.9318, 3.1276, 3.2383, 3.2972,
3.3276, 3.3428, 3.3510, 3.3554, 3.3582], [0.21837, 0.31374, 0.44906, 0.64073, 
0.90406, 1.2566, 1.6931, 2.1749, 2.6283, 2.9801, 3.2095, 3.3386, 3.4048,
3.4403, 3.4580, 3.4677, 3.4735, 3.4761, 3.4789, 3.4809]])
incertVCircRC = np.array([[5e-6, 5e-6, 5e-6, 5e-6, 5e-6, 5e-6, 5e-6, 5e-5,
5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5], 
[5e-6, 5e-6, 5e-6, 5e-6, 5e-6, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 
5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5]])
VCircRL1 = np.array([3.0436, 2.9228, 2.7150, 2.3976, 1.9926, 1.5569, 1.13086, 
0.83882, 0.59467, 0.41696, 0.28992, 0.67905])
VCircRL2 = np.array([3.5035, 3.5031, 3.5025, 3.5013, 3.4988, 3.4919, 3.4817, 
3.4607, 3.4183, 3.3342, 3.1747, 2.8969, 2.4770, 1.9357, 1.3428, 0.7630,
0.21863, 0.92579])
incertVCircRL1 = np.array([5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-6, 5e-6,
5e-6, 5e-6, 5e-6, 5e-6]) 
incertVCircRL2 = np.array([5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5,
5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-6, 5e-6, 5e-6])
VCircRLC1 = np.array([0.018357, 0.026446, 0.038067, 0.055007, 0.079632, 
0.116512, 0.17347, 0.26909, 0.46321, 0.86251, 0.97499, 1.11270, 1.2852, 1.5080,
1.8058, 2.2218, 2.8297, 3.7353, 4.9038, 5.5528, 4.9648, 3.9883, 3.1923, 2.6177, 
2.2048, 1.8994, 1.6675, 1.4863, 1.3414, 1.2231, 0.65733, 0.33147, 0.193, 
0.11067, 0.515, 0.15225])
VCircRLC2 = np.array([0.044403, 0.064052, 0.092401, 0.13397, 0.19529, 0.29017, 
0.44742, 0.75593, 0.98374, 1.13113, 1.3099, 1.5304, 1.8116, 2.1798, 2.6765,
3.3559, 4.2524, 5.2136, 5.684, 5.2641, 4.439, 3.6848, 3.1039, 2.6661, 2.3322,
2.0725, 1.8656, 1.6980, 1.5588, 1.2404, 0.61322, 0.37843, 0.23795, 0.14528, 
0.0769, 0.0202, 0.0322, 0.0895, 0.15881])
incertVCircRLC1 = np.array([5e-7, 5e-7, 5e-7, 5e-7, 5e-7, 5e-7, 5e-6, 5e-6,
5e-6, 5e-6, 5e-6, 5e-6, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 
5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-6, 5e-6, 5e-3, 5e-3, 
5e-3, 5e-3])
incertVCircRLC2 = np.array([5e-7, 5e-7, 5e-7, 5e-6, 5e-6, 5e-6, 5e-6, 5e-6, 
5e-6, 5e-6, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 
5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-5, 5e-6, 5e-6, 5e-6, 5e-6, 
5e-4, 5e-4, 5e-4, 5e-4, 5e-6])

# On trouve les delta temporels entre les crêtes et leurs incertitudes
deltaTMesureCircRC = -1e-6 * np.array([[[2480, 1800, 1320, 920, 500, 340, 208, 
142, 86, 54, 28, 16.8, 7.6, 4.2, 1.8, 1.1, 0.4, 0.2, 0.1, 0.04], [2880, 2000,
1120, 840, 620, 410, 252, 154, 100, 66, 35, 20, 11.2, 6.4, 2.4, 1.4, 0.8, 0.3, 
0.2, 0.08]], [[2700, 1660, 1040, 760, 440, 320, 216, 104, 58, 26, 19, 9, 3.6, 
2, 0.6, 0.3, 0.2, 0.08, 0.04, 0], [2840, 1780, 1140, 820, 520, 360, 240, 136,
62, 38, 22, 11, 5.2, 3.2, 0.9, 0.4, 0.3, 0.12, 0.06, 0.02]]])
deltaTCircRC, incertDeltaTCircRC = moyEtIncert(deltaTMesureCircRC)
deltaTMesureCircRL1 = 1e-6 * np.array([[360., 520., 380., 390., 310., 250.,
220., 150., 112., 84., 66., 2.68], [400., 560., 460., 420., 370., 270., 230., 
190., 132., 100., 70., 2.8]])
deltaTCircRL1, incertDeltaTCircRL1 = moyEtIncert(deltaTMesureCircRL1)
deltaTMesureCircRL2 = 1e-6 * np.array([[200., 100.0, 60., 40., 30., 28.0, 
22.0, 22.0, 22.0, 21.0, 19.0, 18.0, 16.40, 14.40, 12.40, 10.10, 7.7, 1.080], 
[240., 120., 100., 60., 40., 30., 30., 32., 24., 24., 20., 20.4, 17.60, 15.20, 
13.20, 10.40, 8.1, 1.180]])
deltaTCircRL2, incertDeltaTCircRL2 = moyEtIncert(deltaTMesureCircRL2)
deltaTMesureCircRLC1 = 1e-6 * np.array([[-2280., -1560., -1140., -800., -560., 
-396., -280., -178., -130., -86., -90., -84., -78., -72., -66., -62., -52., 
-39., -23.2, 0., 20., 34., 41.6, 44.8, 46.80, 48.4, 48.4, 49.2, 49.6, 48., 42., 
30., 24.2, 15.2, 10.2, 2.24], [-2560., -1800., -1240., -860., -600., -404., 
-284., -190., -136., -96., -92., -90., -80., -78., -72., -64., -60., -43., 
-25.8, -0.8, 22., 34.80, 42.0, 46.0, 48., 49.6, 49.6, 49.6, 50., 49.20, 43.6, 
30.8, 21.6, 16.4, 10.6, 2.36]])
deltaTMesureCircRLC2 = 1e-6 * np.array([[-2560., -1680., -1170., -820., -540., 
-372., -272., -176., -153., -140., -130., -118., -109., -95., -85., -51.6, 
-51.6, -30., -0.8, 24., 41.20, 50., 56., 58., 60.4, 60.1, 60.4, 59.6, 59.2, 
54.8, 41.2, 30.4, 20.6, 14.9, 10.3, 6.5, 4.68, 3.38, 2.4], [-2320., -1800., 
-1210, -860., -680., -404., -280., -186., -156., -142., -133., -121., -111., 
-99., -88., -56.8, -56.8, -33.2, -1.8, 24.80, 42.4, 52., 57.2, 59.2, 61.2, 
61.6, 62., 60.8, 61.2, 57.2, 42.8, 31.6, 22.6, 15.1, 10.5, 7.3, 5.04, 3.5, 
2.425]])
deltaTCircRLC1, incertDeltaTCircRLC1 = moyEtIncert(deltaTMesureCircRLC1)
deltaTCircRLC2, incertDeltaTCircRLC2 = moyEtIncert(deltaTMesureCircRLC2)

# On donne les résistances et leurs incertitudes
RCircRC = np.array([1, 10]) * 1e3
RCircRL = np.array([1, 10]) * 1e3
RL = np.array([62.479, 24.2605])
RCircRLC = np.array([1, 0.5]) * 1e3

# On donne les capacitance et leurs incertitudes
CCircRC = np.array([50, 10]) * 1e-9
CCircRLC = np.array([4, 20]) * 1e-9

# On donne les inductances et leurs incertitudes
L = np.array([500, 200]) * 1e-3

"""On fait ici les manipulations des données expérimentales:"""

# On trouve les rapports chute de tension sur tension et leurs incertitudes
VSurECircRC, incertVSurECircRC = calculVSurE(VCircRC, ECircRC, incertVCircRC,
incertE)
VSurECircRL1, incertVSurECircRL1 = calculVSurE(VCircRL1, ECircRL1, 
incertVCircRL1, incertE)
VSurECircRL2, incertVSurECircRL2 = calculVSurE(VCircRL2, ECircRL2, 
incertVCircRL2, incertE)
VSurECircRLC1, incertVSurECircRLC1 = calculVSurE(VCircRLC1, ECircRLC1, 
incertVCircRLC1, incertE)
VSurECircRLC2, incertVSurECircRLC2 = calculVSurE(VCircRLC2, ECircRLC2, 
incertVCircRLC2, incertE)

# On trouve les périodes d'oscillation et leurs incertitudes
periodeCircRC, incertPeriodeCircRC = calculPeriode(fCircRC, incertFCircRC)
periodeCircRL1, incertPeriodeCircRL1 = calculPeriode(fCircRL1, incertFCircRL1)
periodeCircRL2, incertPeriodeCircRL2 = calculPeriode(fCircRL2, incertFCircRL2)
periodeCircRLC1, incertPeriodeCircRLC1 = calculPeriode(fCircRLC1, 
incertFCircRLC1)
periodeCircRLC2, incertPeriodeCircRLC2 = calculPeriode(fCircRLC2, 
incertFCircRLC2)

# On trouve la différence de phase dans le circuit et leurs incertitudes
phiCircRC, incertPhiCircRC = calculPhi(deltaTCircRC, periodeCircRC, 
incertDeltaTCircRC, incertPeriodeCircRC)
phiCircRL1, incertPhiCircRL1 = calculPhi(deltaTCircRL1, periodeCircRL1, 
incertDeltaTCircRL1, incertPeriodeCircRL1)
phiCircRL2, incertPhiCircRL2 = calculPhi(deltaTCircRL2, periodeCircRL2, 
incertDeltaTCircRL2, incertPeriodeCircRL2)
phiCircRLC1, incertPhiCircRLC1 = calculPhi(deltaTCircRLC1, periodeCircRLC1, 
incertDeltaTCircRLC1, incertPeriodeCircRLC1)
phiCircRLC2, incertPhiCircRLC2 = calculPhi(deltaTCircRLC2, periodeCircRLC2, 
incertDeltaTCircRLC2, incertPeriodeCircRLC2)

# On trouve la pulsation du circuit et son incertitude
omegaCircRC, incertOmegaCircRC = calculOmega(fCircRC, incertFCircRC)
omegaCircRL1, incertOmegaCircRL1 = calculOmega(fCircRL1, incertFCircRL1)
omegaCircRL2, incertOmegaCircRL2 = calculOmega(fCircRL2, incertFCircRL2)
omegaCircRLC1, incertOmegaCircRLC1 = calculOmega(fCircRLC1, incertFCircRLC1)
omegaCircRLC2, incertOmegaCircRLC2 = calculOmega(fCircRLC2, incertFCircRLC2)

"""On fait les calculs afin de trouver les données théoriques:"""

# On cherche les rapports chute de tension sur tension théoriques
VSurECircRCTh1 = 1 / np.sqrt(1 + (1 / (omegaCircRC * CCircRC[0] * 
RCircRC[0])) ** 2)
VSurECircRCTh2 = 1 / np.sqrt(1 + (1 / (omegaCircRC * CCircRC[1] * 
RCircRC[1])) ** 2)
VSurECircRLTh1 = 1 / np.sqrt(1 + (omegaCircRL1 * L[0] / (RCircRL[0] + 
RL[0])) ** 2)
VSurECircRLTh2 = 1 / np.sqrt(1 + (omegaCircRL2 * L[1] / (RCircRL[1] + 
RL[1])) ** 2)
VSurECircRLCTh1 = 1 / np.sqrt(1 + ((1 / (omegaCircRLC1 * CCircRLC[0] * 
(RCircRLC[0] + RL[0]))) - (omegaCircRLC1 * L[0] / (RCircRLC[0] + RL[0]))) ** 2)
VSurECircRLCTh2 = 1 / np.sqrt(1 + ((1 / (omegaCircRLC2 * CCircRLC[1] * 
(RCircRLC[1] + RL[1]))) - (omegaCircRLC2 * L[1] / (RCircRLC[1] + RL[1]))) ** 2)

# On cherche les déphasages théoriques
phiCircRCTh1 = np.arctan((omegaCircRC * CCircRC[0] * RCircRC[0]) ** -1)
phiCircRCTh2 = np.arctan((omegaCircRC * CCircRC[1] * RCircRC[1]) ** -1)
phiCircRLTh1 = -np.arctan(omegaCircRL1 * L[0] / (RCircRL[0] + RL[0]))
phiCircRLTh2 = -np.arctan(omegaCircRL2 * L[1] / (RCircRL[1] + RL[1]))
phiCircRLCTh1 = np.arctan((1 / (omegaCircRLC1 * CCircRLC[0] * 
(RCircRLC[0] + RL[0]))) - (omegaCircRLC1 * L[0] / (RCircRLC[0] + RL[0])))
phiCircRLCTh2 = np.arctan((1 / (omegaCircRLC2 * CCircRLC[1] * 
(RCircRLC[1] + RL[1]))) - (omegaCircRLC2 * L[1] / (RCircRLC[1] + RL[1])))

"""On trace ici les graphiques nécessaires :"""

# On trace le graphique RC avec R = 1k et C = 50n
plt.figure(0)

traceGraph(omegaCircRC, phiCircRC[0, :], VSurECircRC[0, :], incertOmegaCircRC, 
incertPhiCircRC[0, :], incertVSurECircRC[0, :], VSurECircRCTh1, phiCircRCTh1)

plt.savefig('Lab1_FigRC150.png')

# On trace le graphique RC avec R = 10k et C = 10n
plt.figure(1)

traceGraph(omegaCircRC, phiCircRC[1, :], VSurECircRC[1, :], incertOmegaCircRC, 
incertPhiCircRC[1, :], incertVSurECircRC[1, :], VSurECircRCTh2, phiCircRCTh2)

plt.savefig('Lab1_FigRC1010.png')

# On trace le graphique RL avec R = 1k et L = 500m
plt.figure(2)

traceGraph(omegaCircRL1, phiCircRL1, VSurECircRL1, incertOmegaCircRL1, 
incertPhiCircRL1, incertVSurECircRL1, VSurECircRLTh1, phiCircRLTh1)

plt.savefig('Lab1_FigRL1500.png')

# On trace le graphique RL avec R = 10k et L = 200m
plt.figure(3)

traceGraph(omegaCircRL2, phiCircRL2, VSurECircRL2, incertOmegaCircRL2, 
incertPhiCircRL2, incertVSurECircRL2, VSurECircRLTh2, phiCircRLTh2)

plt.savefig('Lab1_FigRL10200.png')

# On trace le graphique RLC avec R = 1k, L = 500m et C = 4n
plt.figure(4)

traceGraph(omegaCircRLC1, phiCircRLC1, VSurECircRLC1, incertOmegaCircRLC1, 
incertPhiCircRLC1, incertVSurECircRLC1, VSurECircRLCTh1, phiCircRLCTh1)

plt.savefig('Lab1_FigRLC12004.png')

# On trace le graphique RLC avec R = 500, L = 200m et C = 20n
plt.figure(5)

traceGraph(omegaCircRLC2, phiCircRLC2, VSurECircRLC2, incertOmegaCircRLC2, 
incertPhiCircRLC2, incertVSurECircRLC2, VSurECircRLCTh2, phiCircRLCTh2)

plt.savefig('Lab1_FigRLC50020020.png')

plt.show()