# -.- coding:latin1 -.-
# @author: Nicolas

import numpy as np
import matplotlib.pyplot as plt

xp = np.array([0.0003822, 0.000689, 0.0013598, 0.0029614])
errXp = np.array([1.0925e-06, 6.6250e-06, 1.3075e-05, 2.8475e-05])
xth = np.array([0.00037418, 0.00072872, 0.00136403, 0.0028327])
errXth = np.array([3.60630843e-06, 7.01724014e-06, 1.3165239e-05, 2.75598966e-05])

b = np.array([0.0001738864088546033, 0.00010023593708034936, 4.654286617244804e-05,
2.25296757664884e-05])
errB = np.array([1.2745074345618943e-05 * 4, 1.2745074345618943e-05 * 2, 
1.2745074345618943e-05, 1.2745074345618943e-05 / 2])

plt.plot(b, xp, '.b', label='Premiers minimums expérimentaux')
plt.plot(b, xth, '.r', label='Premiers minimums théoriques')

plt.xlabel('Largeur d\'une fente (m)')
plt.ylabel('Position relative du premier minimum sur le détecteur (m)')
plt.errorbar(b, xp, yerr=errB, xerr=errXp, ls='None', color='b')
plt.errorbar(b, xth, yerr=errB, xerr=errXth, ls='None', color='r')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.legend()

plt.savefig('Lab6.png')
plt.show()