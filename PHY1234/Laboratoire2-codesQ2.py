# -*- coding: latin-1 -*-
#@author: Nicolas Levasseur
"""
Ce code sert à calculer une suite de Syracuse, qui est sous la forme
n+1=n/2 si n est pair et n+1=3n+1 si n est impair.
"""

nombreDebut = int(input('Entrez un nombre entier entre 0 et 100:')) 
while nombreDebut != 0: 
    """On répète le programme tant que le nombre entré n'égale pas 0, et 
    lorsqu'il est égal à 0 on termine le programme"""
    n = nombreDebut 
    """On définit n qui servira à arrêter la deuxième boucle et on garde nn 
    pour s'assurer que l'instruction break ne se produit pas quand les nombres
    de la suite produite sont plus haut que 100"""
    if nombreDebut > 0 and nombreDebut < 100: 
        """On s'assure d'imprimer seulement le message d'erreur en cas de non
        respect de l'intervalle établi""" 
        print(str(nombreDebut))
    while n != 1: 
        """On sait que la suite de Syracuse finit toujours par 1, on \
        demande donc au programme d'arrêter à 1"""
        if nombreDebut > 100 or nombreDebut < 0: 
            """On affiche un message d'erreur à l'utilisateur si le nombre entré
            n'est pas dans l'intervalle de validité, puis on lui redemande
            d'entrer un nombre entre 0 et 100."""
            print('Erreur, le nombre n\'est pas compris dans l\'intervalle \
            de validité.')
            break
        if n % 2 == 1: 
            """On donne les instructions pour faire une suite de Syracuse 
            avec un nombre impair"""
            n = 3 * n + 1
        else: 
            """On demande au programme de calculer la suite de Syracuse pour
            les nombres pairs"""
            n //= 2
        print(str(n))
    nombreDebut = int(input('Entrez un autre nombre entier entre 0 et 100:'))
    #On redemande un autre nombre à l'utilisateur

print('Fermeture du programme en cours...')