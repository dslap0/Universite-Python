# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule la position en 2 dimensions d'un objet suivant
un mouvement parabolique et affiche ce mouvement sur un graphique, puis
il affiche un autre graphique qui représente la distance entre le
projectile et son origine en fonction du temps normalisé. Le programme
affiche ensuite une série de carctéristiques de la trajectoire du 
projectile. Ce programme fonctionne aussi pour tracer plusieurs
trajectoires et donner les caractéristiques de plus d'une 
trajectoire à la fois."""

import numpy as np

import matplotlib.pyplot as plt

def trajectoire(v0, theta, npt):
    """Cette fonction trouve la trajectoire d'un projectile en fonction
    de la vitesse du lancer au départ et de l'angle de celui-ci.
    
    v0 : Vitesse initale en m/s
    theta : Angle du lancer par rapport au sol en degrés
    npt : Nombre de pas à calculer par la fonction
    """
    theta = np.radians(theta)

    tf = 2 * v0 / 9.8 * np.sin(theta)
    """On calcule le moment où l'objet atterrit, qui sera la limite supérieure
    de l'array temps"""

    t, dt = np.linspace(0, tf, npt, retstep=True)
    """On crée l'ndarray temps, qui nous permet de calculer les ndarrays x et
    y représentants la position en x et en y du projectile"""
    
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 9.8 / 2 * t ** 2
    """On trouve la position en x et en y du projectile pour toutes les 
    valeurs de temps jusqu'à ce que le projectile touche le sol"""

    return t, x, y, dt, tf

def derive(fDiscrete, pas, npt):
    """Fonction servant à dériver une fonction mathématique à partir de
    sa forme discrète.
    
    fDiscrete : Fonction à dérivée discrétisée
    pas : Taille du pas de la maille (ou le pas doit être égal à 
    n * len(tempsNormal) / npt)
    npt : Valeur du nombre de pas donné à l'autre fonction trajectoire
    """
    element = 0
    croissance = True

    if pas * npt % 1 != 0:
        print('Erreur, le pas entré n\'est pas valide.')
    else:
        pasD = int(pas * npt)
        """Si aucune valeur de df n'est décroissante, alors la fonction est 
        toujours croissante"""
        while element < len(d):
            """On tente de calculer la derivée en un point avec une 
            boucle while"""
            if element == 0:
                # On calcule sans la valeur précédente pour la première valeur
                df = (fDiscrete[element + pasD] - fDiscrete[element]) / pas
            elif element == len(d) - 1:
                # On calcule sans la valeur suivante pour la dernière valeur
                df = (fDiscrete[element] - fDiscrete[element - pasD]) / pas
            else:
                """On applique la formule de dérivation normale pour les 
                autres éléments à calculer"""
                df = (fDiscrete[element + pasD] - fDiscrete[element - pasD]) / (2 * pas)
             if df < 0:
                """Si on rencontre un df négatif, la fonction n'est pas toujours
                croissante"""
                croissance = False
                break
            element += 1
        return croissance

thetaTab = np.arange(25, 85.1, 5)
# On définit un tableau avec toutes les valeurs de theta que l'on désire

for theta in thetaTab:
    """On calcule toutes les valeurs de x et y pour chaque theta dans thetaTab
    et on trace les graphiques associés"""
    npt = 500
    t, x, y, dt, tf = trajectoire(20, theta, npt)
    plt.figure(1)
    # On trace le premier graphique, celui de la position en 2D
    plt.plot(x, y)
    xtop = x[y.argmax()]
    # On trouve la valeur de x associée au y max
    plt.text(xtop, y.max(), s='theta: ' + str(theta))
    # On pose l'identificateur au sommet de la courbe
    plt.figure(2)
    """On trace le deuxième graphique, celui de la distance du projectile par 
    rapport à son origine"""
    tempsNormal = t / tf
    d = np.sqrt(x ** 2 + y ** 2)
    """On calcule le temps normalisé et la distance entre l'origine et le 
    projectile à un certain x et y"""
    plt.plot(tempsNormal, d)
    pas = 1 / 500
    """On donne à la taille du pas de maille la valeur de n * len(tempsNormal)
    sur la valeur attribuée à npt, ce qui nous donne en substituant, pour
    n = 1 : 1 / 500"""
    croissance = derive(d, pas, npt)
    print('theta : ' + str(theta) + ', temps de vol : ' + str(tf) + \
', portée : ' + str(x.max()) + ', hauteur maximale : ' + str(y.max()) + \
', \ncroissance de la distance par rapport à l\'origine sur l\'ensemble du \
vol du projectile : ' + str(croissance) + '\n')

plt.figure(1)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
# On ajuste les paramètres esthétiques du premier graphique
plt.savefig('Laboratoire4-figureQ3-1.png')

plt.figure(2)
plt.xlabel('t / tf')
plt.ylabel('d (m)')
# On ajuste les paramètres esthétiques du deuxième graphique
plt.savefig('Laboratoire4-figureQ3-2.png')

plt.show()