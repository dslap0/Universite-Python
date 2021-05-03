# -*- coding: latin-1 -*-
#@author: Nicolas
"""
Code incomplet visant à passer par une boucle for au lieu de while pour 
trouver la somme de contrôle de l'algorithme de Luhn.
"""

liste = list(((input('Entrez un code à vérifier:')).\
replace(' ','')).replace('-',''))
i = 0

for x in (0,len(liste)): #On change tous les éléments de la liste en int
    x = int(x)
    for x in (0,len(liste),2): #On change un nombre sur deux
        x *= 2
        if x > 9: 
            """Lorsqu'on arrive avec une solution à deux chiffres, 
            on soustrait 9 pour ne garder qu'un seul chiffre"""
            x  -= 9
    liste[i] = x
    i += 1

somme = sum(liste) #On produit la somme de contrôle
print(somme)

if somme % 10 == 0: 
    #Si la somme de contrôle est un multiple de 10, alors le code est valide
    print('Le code semble être valide.')
else: 
    """Si la somme de contrôle n'est pas divisible par 10, alors 
    le code est invalide"""
    print('Le code est invalide.')