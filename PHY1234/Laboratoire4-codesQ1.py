# -.- coding:latin1 -.-
# @author: Nicolas
"""Ce programme calcule la position en 2 dimensions d'un objet suivant
un mouvement parabolique et les affiche dans un fichier."""

import numpy as np

vitesseInitiale, angleTrajectoire = [20,np.radians(60)]

tempsFinal = 2 * vitesseInitiale / 9.8 * np.sin(angleTrajectoire)
"""On calcule le moment où l'objet atterrit, qui sera la limite supérieure
de l'array temps"""

temps = np.arange(0, tempsFinal, 0.01)
"""On crée l'ndarray temps, qui nous permet de calculer les arrays x et y,
représentant la position en x et en y du projectile"""

x = vitesseInitiale * np.cos(angleTrajectoire) * temps
y = vitesseInitiale * np.sin(angleTrajectoire) * temps - 9.8 / 2 * temps ** 2
"""On trouve la position en x et en y du projectile pour toutes les valeurs de
temps jusqu'à ce que le projectile touche le sol"""

fichier = open('Trajectoire du projectile.txt', 'w')
fichier.write('#Ce document recueille la position d\'un projectile, lancé \
à ' + str(vitesseInitiale) + ' mètres par \n#seconde et à ' + \
str(angleTrajectoire) + ' degrés par rapport au sol. En \
ordre, on a le temps, la \n#position horizontale et la position verticale du \
projectile (t, x, y):\n\n')
# On fait une entête pour le document produit
i = 0
while i != len(temps):
    # On crée une boucle d'écriture pour afficher nos données à la chaîne
    fichier.write('{0:.2f} {1:.4f} {2:.4f} \n'.format(temps[i],x[i],y[i]))
    i += 1
fichier.close()