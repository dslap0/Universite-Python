import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy import *
from pylab import *
from scipy.optimize import curve_fit

def f1(x, xm, b, L):
	""" Fonction pour trouver l'intensité relative avec divers paramètres expérimentaux
	"""
	resolution  = 5.2e-6
	lambd		= 532e-9

	xcal = (x - xm) * resolution                    		# crée un veteur xt en m 
	theta 		= np.arctan(xcal/L) 						# calculer theta selon la figure 6.1
	alpha 		= np.pi*b*np.sin(theta)/lambd				# calculer alpha selon 6.2
	theo  		= (sin(alpha)/alpha)**2

	return theo

def traceGraph(xcal, L, b, lambd, label):
	""" On trace le curve_fit et la courbe théorique avec cette fonction.
	"""
	theta 		= np.arctan(xcal/L) 							# calculer theta selon la figure 6.1
	alpha 		= np.pi*b*np.sin(theta)/lambd				# calculer alpha selon 6.2
	theo  		= (sin(alpha)/alpha)**2				# patron d’interférence selon 6.1
	plt.plot(xcal,theo, '-r', label=label)

	return theo

#Définitions
#imagename   = 'C:/Utilisateurs/utilisateur labo/Bureau/diff 0.04mm 2h08.tif'# image à évaluer
#bruitdefond = 'C:/Utilisateurs/utilisateur labo/Bureau/bruit 2h08.tif'# image du bruit de fond associé
imagename   = '1_fente_0.02R.tif'# image à évaluer
bruitdefond = 'bruit_de_fond.tif'# image du bruit de fond associé
L          	= 11.69e-2 - 0.17e-2 - 1.3e-2	        # distance focale de la lentille en m
lambd		= 532e-9			# longueur d'onde du laser (Rouge: 632.8e-9l vert: 532e-9)
b           = 0.04e-3			# largeur de la fente en mètre
d           = 0.5e-3			# distance entre les fentes
N           = 1				    # nombre defentes
resolution  = 5.2e-6			# résolution du numériseur
erreurResolution = 0.05e-6

# Lire les images
image1      = mpimg.imread(imagename)		#lire l'image imagename
image1      = image1[:,:,0]
image1      = np.float64(image1)			# la convertir en format double

bkgnd       = mpimg.imread(bruitdefond)		# lire l'image de bruit de fond
bkgnd       = bkgnd[:,:,0]
bkgnd       = np.float64(bkgnd)				# la convertir en format double

#Vérifie qu'il n'y a pas de données saturées dans l'image
if (np.max(image1) == 255):
	print("\n ATTENTION: votre image comprend des données saturées.")
	print("Il serait préférable de reprendre de nouvelles données.\n")

cimage1     = image1-bkgnd					# corriger l'image
plt.imshow(cimage1)							# montrer l'image

# Choisir la région d’interêt pour sommer le signal du patron selon les colonnes
print("Cliquez une premiere fois n'importe où sur la fenêtre pour l'activer")
print("Cliquez ensuite deux fois (haut et bas) pour sélectionner la région de l'image à intégrer")

pts 		= ginput(2)						# extrait deux points sur l'image
pts_y		= [x[1] for x in pts]  			# extrait les valeurs y de l'image
y1 			= int(round(float(min(pts_y))))	# la plus petite 
y2			= int(round(float(max(pts_y))))	# la plus grande 

#sommation sur la dimension 0 (lignes)
y 			= np.sum(cimage1[y1:y2,:],axis=0)
y 		   /= max(y)							# normaliser le patron à 1

plt.close()								# ferme la fenêtre précédente
ncol		= y.shape[0]				# détermine le nombre de colonnes dans l'image
x 			= np.arange(ncol)			# crée un vecteur de valeurs comprises entre 0 et ncol -1 
fig 		= plt.figure()
plt.plot(x,y)							# affiche le patron
plt.ylabel('Instensité relative')
plt.xlabel('Position sur le détecteur (pixel)')

#déterminer le centre du patron
print('Cliquez deux fois à mi-hauteur (y~0.5) de chaque côté du patron')
pts 		= ginput(2)				# on demande deux points
pts_x 		= [x[0] for x in pts]  	# extrait les valeurs x de l'image
x1 			= int(round(float(min(pts_x))))	# la plus petite
x2 			= int(round(float(max(pts_x))))	# la plus grande
xm 			= (x1 + x2) / 2					# le centre est la moyenne des deux points
xcal = (x - xm) * resolution
erreurXcal = abs((x - xm) * erreurResolution)

#affiche le nouveau patron calibré
plt.close()									# ferme la fenêtre précédente
fig 		= plt.figure()
plt.plot(xcal,y,label='Points expérimentaux')							# affiche le patron calibré  
plt.ylabel('Instensité relative')
plt.xlabel('Position relative sur le détecteur (m)')

#On trace le curve_fit et on trouve les erreurs sur celui-ci
param, covar = curve_fit(f1, x, y, p0=(xm, b, L), bounds=(np.array([x1, 0, L - 1.3e-2]), 
np.array([x2, 2 * b, L + 1.3e-2])))

xm1, b1, L1 = param
erreurXm1, erreurB1, erreurL1 = np.sqrt(np.diag(covar))

xcal1 = (x - xm1) * resolution
erreurXcal1 = np.sqrt((-resolution * erreurXm1) ** 2 + ((x - xm1) * erreurResolution) ** 2)

theo = traceGraph(xcal1, L1, b1, lambd, 'Courbe curve_fit')

#On trouve le premier minimum
i = (np.abs(xcal + 0.003)).argmin()
j = (np.abs(xcal)).argmin()
iminExp = np.where(y == np.amin(y[i:j]))
xminExp = xcal[iminExp]
erreurXminExp = erreurXcal[iminExp]
iminTh = np.where(theo == np.amin(theo[i:j]))
xminTh = xcal1[iminTh]
erreurXminTh = erreurXcal1[iminTh]

print(b1, L1)
print(erreurB1, erreurL1)
print(xminExp)
print(erreurXminExp)
print(xminTh)
print(erreurXminTh)

plt.legend()
plt.savefig('Lab6_FigG.png')
plt.show()