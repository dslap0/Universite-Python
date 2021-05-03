# -*- coding: latin-1 -*-
#@author: Nicolas Levasseur
"""
Ce code sert à vérifier si le nombre entré par l'utilisateur est 
valide ou non selon l'algorithme de Luhn, qui stipule qu'un nombre 
est valide si sa somme de contrôle est divisible par 10 entièrement.
Cette somme de contrôle est obtenue en faisant la somme de chaque 
nombre d'un autre code, obtenu grâce à certaines manipulations sur 
le précédent. Ces manipulations sont la multiplication de chacun des
chiffres du code entré par l'utilisateur par 2 et la soustraction de 9
à ceux dont le produit donnait un nombre supérieur à 9.
"""

liste = list(((input('Entrez un code à vérifier:')).\
    replace(' ','')).replace('-',''))
position =- 1
"""On met l'indice de l'élément à changer négatif, puisqu'on va de la 
gauche vers la droite"""

while position >= -len(liste): 
    """La boucle se répète jusqu'à ce que l'indice du nombre à changer soit
    plus petit que le nombre d'éléments de la liste (à cause du négatif)"""
    element = int(liste[position]) 
    """On doit changer chaque élément de la liste en nombre pour pouvoir en
    faire la somme plus tard"""
    if -position % 2 == 1: 
        """On doit seulement modifier un chiffre sur 2, et le premier chiffre
        à partir de la gauche doit être modifié"""
        element *= 2
        if element > 9: 
            #On s'assure de ne pas avoir d'éléments de la liste à 2 chiffres
            element -= 9
    liste[position] = element 
    #On modifie l'élément d'indice y dans la suite au profit du nouveau nombre
    position -= 1  #On refait la même procédure pour les nombres suivants

somme = sum(liste) #On produit la somme de contrôle
print(somme)

if somme % 10 == 0: 
    #Si la somme de contrôle est un multiple de 10, alors le code est valide
    print('Le code semble être valide.')
else: 
    """Si la somme de contrôle n'est pas divisible par 10, alors le code
    est invalide"""
    print('Le code est invalide.')