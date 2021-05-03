# -*- coding: latin-1 -*-
#@author: Nicolas Levasseur
"""
Ce code sert à calculer le rendement d'un placement à taux fixe après n années
"""

A,p,n=input('Veuillez entrer en chiffres le montant initial du placement \
(en dollars, noté A), le taux annuel \ndu placement (en poucentage, noté \
p) et la durée (en année, noté n), le tout séparé par des \
tirets (A-p-n):').split('-')
"""On demande à l'utilisateur d'entrer toutes les informations nécessaires en 
une entrée, qu'on subdivise grâce à l'opérateur split() qui nous permet 
d'associer à chaque variable sa valeur correspondante"""

A=int(A)
p=int(p)
n=int(n)
#On convertit les entrées str en int pour les calculs

F=A*(1+p/100)**n 
#Le programme calcul F, soit le rendement final après n années
F=round(F,2) 
#On arrondit ici F pour ne pas perdre l'information après la deuxième décimale
d=str(int(F%1*100)) 
#On trouve le reste en cents, appelé d, et on le convertit en str
F=str(int(F)) 
#On doit fixer la valeur de F en int et ensuite transformer ce int en str

print('La valeur finale du placement est de '+F+' dollars et '+d+' cents.')