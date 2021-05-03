# -.- coding:latin1 -.-
# @author: Nicolas
"""
Ce code sert à répliquer la fonction tortue du language LOGO original,
où une tortue trace un graphique selon des instructions données par 
l'utilisateur en une seule entrée.
"""

import matplotlib.pyplot as plt

instructions = list(input('Entrez une suite d\'instructions pour la tortue:'))
x = 0
y = 0
direction = 0
tracage = '-'
"""On commence à (0,0), en regardant vers les y positifs et avec le 
traçage activé"""

for i in instructions:
    """On effectue les opérations à la chaine sur tous les éléments de la 
    chaine entrée par l'utilisateur"""
    x1 = x
    y1 = y
    """On donne ces valeurs pour tracer à partir de celles-ci jusqu'aux 
    nouvelles valeurs (voir ligne )"""
    if i == 'A':
        """On donne les instructions lorsqu'on avance, ce qui dépend 
        de l'orientation actuelle de la tortue"""
        if direction % 4 == 0:
            y += 1
        elif direction % 4 == 1:
            x += 1
        elif direction % 4 == 2:
            y -= 1
        elif direction % 4 == 3:
            x -= 1
    elif i == 'D':
        """La direction est en fonction de son reste lors de la division par
        4, elle influence donc l'avancée de la tortue de manière cyclique, et
        on détermine à partir des règles utilisées pour définir x et y du 
        sens de la modification qu'on doit effectuer sur la direction.
        En gros, on remarque que si direction += 1, alors on passe de y += 1
        à x += 1, ce qui correspond à une rotation vers la droite (le même 
        raisonnement s'applique aux autres modifications possibles."""
        direction += 1
    elif i == 'G':
        """On applique la règle inverse à la règle pour la droite, puisque
        l'opérateur % est cyclique, dans le sens que -1 % 4 == 3 % 4"""
        direction -= 1
    elif i == 'T':
        #On inverse la valeur de tracage quand T apparait
        if tracage == '-':
            """Le T définit si on doit tracer ou non la prochaine séquence
            d'instruction et entre dans le paramètre linestyle de la fonction
            plt.plot, il doit donc correspondre au format attendu pour ce 
            paramètre"""
            tracage = ''
        elif tracage == '':
            tracage = '-'
    deltax = [x,x1]
    deltay = [y,y1]
    """On définit les deux listes qui vont nous permettre de tracer nos 
    lignes, où x1 et y1 sont les dernières position de x et y"""
    plt.plot(deltax,deltay,linestyle=tracage,color='k')
    """On ajoute un segment au graphique (qui peut être invisible, mais
    est ajouté dans tous les cas"""
    
plt.show()