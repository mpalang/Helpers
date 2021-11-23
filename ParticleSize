import numpy as np

L=[430,449,469,490,514,544,579,620,665] # Positions of Maxima

def Calcd(l1,l2):
    l1=float(l1)
    l2=float(l2)
    n=l2/(l2-l1)
    d=n*l2
    return d

D=[] #Diameter in 1E-6m
for n in range(len(L)-1):
    D.append(round(Calcd(L[n],L[n+1])/1000,2))

N=0
for i in D:
    N=N+i
avg=N/len(D)

D.append(avg)

np.savetxt('Particle Sizes.txt',D,fmt='%1.2f',header='Particle Sizes in Mycrometer. Last one is Average.')

