# -*- coding: utf-8 -*-

#coding = utf8!

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

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
#on obtient l'observationà l'état 0

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
#on obtient toutes les observations nécessaires 

    #identique aux deux 
Transmi = np.array([[0.7 , 0.3],[0.4 , 0.6]])

if obs[0] == 'Normal' : 
    O = np.array([[0.7 , 0] , [0 , 0.1]])
elif obs[0] == 'Rhume' : 
    O = np.array([[0.2 , 0] , [0 , 0.4]])
else : 
    O = np.array([[0.1 , 0] , [0 , 0.5]])

    #FORWARD
PinitF = [0.6 , 0.4]
PF = np.zeros([N,2])
OF = O

PF[0,:] = np.dot(PinitF,OF)

for k in range(N-1):
    if obs[k+1] == 'Normal' : 
        OF = np.array([[0.7 , 0] , [0 , 0.1]])
    elif obs[k+1] == 'Rhume' : 
        OF = np.array([[0.2 , 0] , [0 , 0.4]])
    else : 
        OF = np.array([[0.1 , 0] , [0 , 0.5]])
    PF[k+1,:] = np.dot(PF[k,:],np.dot(Transmi,OF))
    
print(PF)
    
    #BACKWARD
PinitB = [1 , 1]
PB = np.zeros([N,2])

if obs[N-1] == 'Normal' : 
    OB = np.array([[0.7 , 0] , [0 , 0.1]])
elif obs[N-1] == 'Rhume' : 
    OB = np.array([[0.2 , 0] , [0 , 0.4]])
else : 
    OB = np.array([[0.1 , 0] , [0 , 0.5]])
    
PB[N-1,:] = np.dot(Transmi, np.dot(OB,PinitB))

for k in range(N-2,-1,-1):
    if obs[k+1] == 'Normal' : 
        OB = np.array([[0.7 , 0] , [0 , 0.1]])
    elif obs[k+1] == 'Rhume' : 
        OB = np.array([[0.2 , 0] , [0 , 0.4]])
    else : 
        OB = np.array([[0.1 , 0] , [0 , 0.5]])
    PB[k,:] = np.dot(Transmi, np.dot(OB,PB[k+1]))
    
print(PB)

    #BACKWARD-FORWARD
PBF = PF * PB
print(PBF)    
etatfinal = list()

if PBF[0,0] > PBF[0,1] : 
    etatfinal.append('sain')
else :
    etatfinal.append('malade')

for k in range(N-1):
    if PBF[k,0] > PBF[k,1] : 
        etatfinal.append('sain')
    else :
        etatfinal.append('malade')

print(etatfinal)                
                
    #VITERBI
if obs[0] == 'Normal' : 
    OV = np.array([[0.7 , 0] , [0 , 0.1]])
elif obs[0] == 'Rhume' : 
    OV = np.array([[0.2 , 0] , [0 , 0.4]])
else : 
    OV = np.array([[0.1 , 0] , [0 , 0.5]])

PinitV = [0.6 , 0.4]
PV = np.zeros([N,2])
ProbaMax = np.zeros([N,1])

PV[0,:] = np.dot(PinitV,Transmi)
ProbaMax[0] = max(PV[0,0],PV[0,1])

Stockage = np.zeros([N,2])

    #proba
for k in range(N-1):
    if obs[k+1] == 'Normal' : 
        OV = np.array([[0.7 , 0] , [0 , 0.1]])
    elif obs[k+1] == 'Rhume' : 
        OV = np.array([[0.2 , 0] , [0 , 0.4]])
    else : 
        OV = np.array([[0.1 , 0] , [0 , 0.5]])
    PV[k+1,0] = max(np.dot(PV[k,0],(np.dot(Transmi[0,0], OV[0,0]))),np.dot(PV[k,1],(np.dot(Transmi[0,1], OV[0,0]))))
    PV[k+1,1] = max(np.dot(PV[k,0],(np.dot(Transmi[1,0], OV[1,1]))),np.dot(PV[k,1],(np.dot(Transmi[1,1], OV[1,1]))))
    ProbaMax[k+1] = max(PV[k+1,0],PV[k+1,1])
    
    Stockage[k,0] = np.argmax([np.dot(PV[k-1,0],(np.dot(Transmi[0,0], OV[0,0]))),np.dot(PV[k-1,1],(np.dot(Transmi[0,1], OV[0,0])))])
    Stockage[k,1] = np.argmax([np.dot(PV[k-1,1],(np.dot(Transmi[1,0], OV[1,1]))),np.dot(PV[k-1,1],(np.dot(Transmi[1,1], OV[1,1])))])
            
print(PV)
print(ProbaMax)

print(Stockage)

etatsanterieur = list() 
etatsanterieurM = list() 

#sain    
for k in range(N):
    if Stockage[k,0] == 1 : 
        etatsanterieur.append('Malade')
    else : 
        etatsanterieur.append('Sain')
print(etatsanterieur)

#malade
for k in range(N):
    if Stockage[k,1] == 1 : 
        etatsanterieurM.append('Malade')
    else : 
        etatsanterieurM.append('Sain')
print(etatsanterieurM)

      #etats precedants
etats_probables = np.zeros([N,1])
etatspp = list()

#son état à la fin : 
if PV[N-1,0] > PV[N-1,1] : 
    etats_probables[N-1] = 0
else :
    etats_probables[N-1] = 1

for k in range(N-2,-1,-1) :
    if etats_probables[k+1] == 1 : 
        etats_probables[k] = Stockage[k+1,1]
        if etats_probables[k] == 0 : 
            etatspp.append('Sain')
        else : 
            etatspp.append('Malade')
    else : 
        etats_probables[k] = Stockage[k+1,0]
        if etats_probables[k] == 0:
            etatspp.append('Sain')
        else : 
            etatspp.append('Malade')
            
if etats_probables[0] == 0:
    etatspp.append('Sain')
else : 
    etatspp.append('Malade')
        
print(etats_probables)
print(etatspp)


     

