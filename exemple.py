#coding = utf8!

import numpy as np

N = 5 # nombre d'états à generer

etats = []
obs = []

#initialisation

#60% de chance d'être sain
if  np.random.rand() < 0.6:
	etats.append('Sain')
else:
	etats.append('Malade')
	
tmp = np.random.rand()

#sain : 70% normal, 20% rhume et 10% fievre
if etats[0] == 'Sain':
	if tmp < 0.7:
		obs.append('Normal')
	elif tmp < 0.9:
		obs.append('Rhume')
	else:
		obs.append('Fièvre')
#malade : 10% normal, 40% rhume et 50% fievre
else:
	if tmp < 0.1:
		obs.append('Normal')
	elif tmp < 0.5:
		obs.append('Rhume')
	else:
		obs.append('Fièvre')


for k in range(N-1):
	
	if etats[k] == 'Sain':
		if np.random.rand() < 0.7:
			etats.append('Sain')
		else:
			etats.append('Malade')
	else:
		if np.random.rand() < 0.6:
			etats.append('Malade')
		else:
			etats.append('Sain')
		
	if etats[k+1] == 'Sain':
		if tmp < 0.7:
			obs.append('Normal')
		elif tmp < 0.9:
			obs.append('Rhume')
		else:
			obs.append('Fièvre')
	else:
		if tmp < 0.1:
			obs.append('Normal')
		elif tmp < 0.4:
			obs.append('Rhume')
		else:
			obs.append('Fièvre')
	
		
print('Etats :', etats)
print('Observations :', obs)

    
