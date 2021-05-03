# -.- coding:latin1 -.-
# @author: Nicolas
"""
Code traçant le graphique d'un carré de dimenson 1x1 centré en (0,0)
à l'aide de matplotlib.pyplot
"""

import matplotlib.pyplot as plt

x = [0.5,0.5,-0.5,-0.5,0.5]
y = [0.5,-0.5,-0.5,0.5,0.5]
#On a définit des points qui forment un carré 1x1 centré en (0,0)

plt.plot(x,y,'-') #On trace le carré avec un trait plein
plt.scatter(x,y,marker='o',color=('b','g','y','r','b'))
"""On donne une valeur à la couleur de chaque point (même
si le 5e est aussi le 1er)"""

plt.xlabel('x')
plt.ylabel('y')
#On donne le titre des axes

plt.xlim(-0.6,0.6)
plt.ylim(-0.6,0.6)
#On donne les valeurs limites des axes du graphique

plt.savefig('Laboratoire3-figureQ1.png')
plt.show()