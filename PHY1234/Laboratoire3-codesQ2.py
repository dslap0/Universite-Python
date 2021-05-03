# -.- coding:latin1 -.-
# @author: Nicolas
"""
Ce code sert à montrer graphiquement la trajectoire d'un hypotrochoïde
(figure tracée par un point d'un cercle en rotation dans un autre
cercle plus grand) en fonction de ses différents paramètres.
"""

import numpy as np

import matplotlib.pyplot as plt

def traceurHypotrocoide(R,r,d,phi0=0,couleur='k'):
    """
    Trace la trajectoire d'un hypotrochoïde, soit une figure 
    tracée par un point d'un cercle en rotation à l'intérieur d'un
    autre cercle plus grand.

    Les valeurs acceptées pour r, R et d vont de 0 à 1000 et la
    fonction ne prend en compte que la partie entière du nombre.

    Paramètres de la fonction:
    R : rayon du grand cercle
    r : rayon du petit cercle 
    d : distance entre le point de tracage et le centre du petit cercle
    phi0 : valeur du paramètre phi quand thêta est égal à 0
    couleur : définit la couleur de la courbe tracée
    """
    n = r / (r + R) #Nombre de tour de la grande roue selon celui de la petite
    m = 1 #Nombre de tour de la petite roue
    
    while n % 1 != 0: 
        """On continue la boucle tant que le nombre de tour de la grande roue
        n'est pas un entier"""
        if 0 > r > 1000 or 0 > R > 1000 or 0 > d >1000 or not \
        isinstance(r,int) or not isinstance(R,int) or not isinstance(d,int):
            """On s'assure de ne pas lancer le programme dans des calculs 
            trop long pour trover n en limitant r, R et d à des nombres 
            entiers entre 0 et 1000"""
            break
        m += 1 #On fait toutes les valeurs de m jusqu'à ce que n soit entier
        n = (r / (r + R)) * m #On calcule le nombre de tour de la grande roue

    phi0 = phi0 * 360 / (2 * np.pi) #On transforme phi0 en radians
    theta = np.linspace(0,np.pi * 2 * n,10000)
    """On crée un ndarray numpy qui prend l'ensemble des valeurs de theta pour
    tracer le graphique de l'hypotrocoïde dont les bords sont fermés, avec 
    assez d'éléments pour conserver l'allure générale de la figure"""

    x = (R - r) * np.cos(theta) + d * \
        np.cos(- ((R - r) / r) * theta + phi0)
    y = (R - r) * np.sin(theta) + d * \
        np.sin(- ((R - r) / r) * theta + phi0)
    """On fait le calcul des valeurs de x et de y pour chaque valeur de theta
    qui va nous permettre de tracer l'hypotrocoïde"""
    
    if 0 < r < 1000 and 0 < R < 1000 and 0 < d < 1000 and \
    isinstance(r,int) and isinstance(R,int) and isinstance(d,int):
        """On s'assure ici de ne pas montrer le graphique incomplet si n n'a
        pas été calculé correctement parce que les valeurs entrés par 
        l'utilisateur n'étaient pas toutes valides"""
        plt.plot(x,y,'-',color=couleur)
    else:
        print('Erreur, un nombre n\'est pas compris dans l\'intervalle de \
validité!')

traceurHypotrocoide(264,110,80,couleur='midnightblue')
traceurHypotrocoide(252,105,80,20,couleur='royalblue')
traceurHypotrocoide(240,100,80,40,couleur='yellowgreen')
traceurHypotrocoide(252,105,80,60,couleur='royalblue')
traceurHypotrocoide(60,35,20,couleur='olive')
traceurHypotrocoide(70,15,10,couleur='midnightblue')
"""On demande au programme de tracer une série de courbes
selon certain paramètres"""

plt.axis('off')
plt.savefig('Laboratoire3-figureQ2-1.png')
plt.show()