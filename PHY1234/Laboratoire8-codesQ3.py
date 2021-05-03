# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce code trace l'orbite de deux exoplan�tes calcul�es num�riquement 
par la m�thode de Heun. � noter que u et v sont toujours calcul�s dans
une seule et m�me fonction �tant donn� que les deux formules se
ressemblent (et donc que beaucoup de valeurs reviennent dans les deux
calculs), ce qui permet d'�conomiser de la puissance de calcul en ne
faisant qu'une seule fonction. On a suivi le m�me raisonnement pour 
le calcul de x et de y."""

import numpy as np

import matplotlib.pyplot as plt

def uv1(x1, y1, u1, v1, GM0):
    """Calcule la valeur de la deriv�e de x et de la d�riv�e de y selon
    le temps et quelques param�tres initiaux gr�ce � la m�thode de
    Heun.
    x1 : Position en x avant l'int�gration de la super-Jupiter (float).
    y1 : Position en y avant l'int�gration de la super-Jupiter (float).
    u1 : Vitesse en x avant l'int�gration de la super-Jupiter (float).
    v1 : Vitesse en y avant l'int�gration de la super-Jupiter (float)..
    GM0 : Constante gravitationnelle multipli�e par la masse de
    l'�toile (float).
    """
    x = x1 + h / 2 * u1
    y = y1 + h / 2 * v1
    # On trouve les valeurs de x et de y utilis�es pour la m�thode de Heun
    
    u = u1 - h * (GM0 * x / (x ** 2 + y ** 2) ** (3 / 2))
    v = v1 - h * (GM0 * y / (x ** 2 + y ** 2) ** (3 / 2))
    # On trouve les prochaines vitesses avec la m�thode de Heun
    
    return u, v

def xy(x1, x2, y1, y2, u2, v2, GM0, GM1):
    """Calcule la valeur de x et de y selon le temps et quelques
    param�tres initiaux gr�ce � la m�thode de Heun.
    x1 : Position en x avant l'int�gration de la super-Jupiter (float).
    x2 : Position en x avant l'int�gration de la deuxi�me exoplan�te 
    (float).
    y1 : Position en y avant l'int�gration de la super-Jupiter (float).
    y2 : Position en y avant l'int�gration de la deuxi�me exoplan�te 
    (float).
    u1 : Vitesse en x avant l'int�gration de la super-Jupiter (float).
    v1 : Vitesse en y avant l'int�gration de la super-Jupiter (float).
    GM0 : Constante gravitationnelle multipli�e par la masse de
    l'�toile (float).
    GM1 : Constante gravitationnelle multipli�e par la masse de la
    super-Jupiter (float).
    """
    r0 = (x2 ** 2 + y2 ** 2) ** (3 / 2)
    r1 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (3 / 2)
    
    """On trouve les distances entre l'exoplan�te et ses attracteurs et on les
    expose au cube"""

    x = x2 + h * (u2 - h / 2 * (GM0 * x2 / r0 + GM1 * (x2 - x1) / r1))
    y = y2 + h * (v2 - h / 2 * (GM0 * y2 / r0 + GM1 * (y2 - y1) / r1))
    # On trouve les prochaines positions avec la m�thode de Heun

    return x, y

def uv2(x1, x2, y1, y2, u1, u2, v1, v2, GM0, GM1):
    """Calcule la valeur de x et de y selon le temps et quelques
    param�tres initiaux gr�ce � la m�thode de Heun.
    x1 : Position en x avant l'int�gration de la super-Jupiter (float).
    x2 : Position en x avant l'int�gration de la deuxi�me exoplan�te 
    (float).
    y1 : Position en y avant l'int�gration de la super-Jupiter (float).
    y2 : Position en y avant l'int�gration de la deuxi�me exoplan�te 
    (float).
    u1 : Vitesse en x avant l'int�gration de la super-Jupiter (float).
    u2 : Vitesse en x avant l'int�gration de la deuxi�me exoplan�te 
    (float).
    v1 : Vitesse en y avant l'int�gration de la super-Jupiter (float).
    v2 : Vitesse en y avant l'int�gration de la deuxi�me exoplan�te 
    (float).
    GM0 : Constante gravitationnelle multipli�e par la masse de
    l'�toile (float).
    GM1 : Constante gravitationnelle multipli�e par la masse de la
    super-Jupiter (float).
    """
    
    x = x2 + h / 2* u2
    y = y2 + h / 2 * v2
    # On trouve les valeurs de x et de y utilis�es pour la m�thode de Heun

    r0 = (x ** 2 + y ** 2) ** (3 / 2)
    r1 = ((x - x1) ** 2 + (y - y1) ** 2) ** (3 / 2)
    
    """On trouve les distances entre l'exoplan�te et ses attracteurs et on les
    expose au cube"""

    u = u2 - h * (GM0 * x / r0 + GM1 * (x - x1) / r1)
    v = v2 - h * (GM0 * y / r0 + GM1 * (y - y1) / r1)
    # On trouve les prochaines vitesses avec la m�thode de Heun

    return u, v

G = 4 * np.pi ** 2
M0 = 1
M1 = 0.02 * M0
GM0 = G * M0
GM1 = G * M1
R1 = 1
R2 = 1.4
q = 0.9
h = 0.0002
temps = np.arange(0, 50, h)
# On d�finit les param�tres qui ne changeront pas

x1 = np.empty_like(temps)
x2 = np.empty_like(temps)
y1 = np.empty_like(temps)
y2 = np.empty_like(temps)
u1 = np.empty_like(temps)
u2 = np.empty_like(temps)
v1 = np.empty_like(temps)
v2 = np.empty_like(temps)
# On d�finit les ndarrays o� on placera les valeurs calcul�es dans la boucle

x1[0] = 0
x2[0] = 0
y1[0] = - R1
y2[0] = - R2
u1[0] = q * 2 * np.pi * np.sqrt(M0 / R1)
u2[0] = 2 * np.pi * np.sqrt(M0 / R2)
v1[0] = 0
v2[0] = 0
# On sp�cifie les conditions initiales

for i in range(0, temps.shape[0] - 1):
    x1[i + 1] = x1[i] + h * (u1[i] - h / 2 * (GM0 * x1[i] / ((x1[i] ** 2 + 
y1[i] ** 2) ** (3 / 2))))
    y1[i + 1] = y1[i] + h * (v1[i] - h / 2 * (GM0 / ((x1[i] ** 2 + y1[i] ** 
2) ** (3 / 2)) * y1[i]))
    u1[i + 1], v1[i + 1] = uv1(x1[i], y1[i], u1[i], v1[i], GM0)
    # On trouve les valeurs de positions en x et en y pour la super-Jupiter

    x2[i + 1], y2[i + 1] = xy(x1[i], x2[i], y1[i], y2[i], u2[i], v2[i], GM0,
GM1)
    u2[i + 1], v2[i + 1] = uv2(x1[i], x2[i], y1[i], y2[i], u1[i], u2[i],
v1[i], v2[i], GM0, GM1)

    """On trouve les valeurs de position en x et en y pour la deuxi�me
    exoplan�te"""

plt.figure(0)

plt.plot(x1, y1, '-b')
# On trace l'orbite de la super-Jupiter

plt.plot(x2, y2, '-r')
# On trace l'orbite de la deuxi�me exoplan�te

plt.xlabel('Position en x (en UA)')
plt.ylabel('Position en y (en UA)')
plt.axvline(0, linestyle='--')
plt.axhline(0, linestyle='--')
plt.axis('scaled')
# On modifie les param�tres esth�tiques du graphique

plt.plot(0, 0, '*y')
# On positionne l'�toile sur le graphique

plt.savefig('Laboratoire8-graphiqueQ3-1.png')

plt.figure(1)

plt.plot(x1, y1, '-b')
# On trace l'orbite de la super-Jupiter

plt.plot(x2, y2, '-r')
# On trace l'orbite de la deuxi�me exoplan�te

plt.xlabel('Position en x (en UA)')
plt.ylabel('Position en y (en UA)')
plt.axvline(0, linestyle='--')
plt.axhline(0, linestyle='--')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
# On modifie les param�tres esth�tiques du graphique

plt.plot(0, 0, '*y')
# On positionne l'�toile sur le graphique

plt.savefig('Laboratoire8-graphiqueQ3-2.png')

plt.show()