# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:28:01 2022

@author: lihongkun
"""

import numpy as np
import mpmath as mp
import matplotlib.pyplot as plt
N=1000
ecart=np.pi/2/N
#####rectangle left
fx=np.array([n for n in range(N)])*ecart
inte=ecart*np.sum(np.sin(fx))
print(inte)
#####rectangle right
fx=np.array([n for n in range(1,N+1)])*ecart
inte=ecart*np.sum(np.sin(fx))
print(inte)
#####rectangle middle
fx=np.array([n for n in range(N)])*ecart
inte=ecart*np.sum(np.sin(fx+ecart/2))
print(inte)
#####trapeze
fx=np.array([n for n in range(1,N)])*ecart
inte=ecart*((np.sin(0)+np.sin(np.pi/2))/2+np.sum(np.sin(fx)))
print(inte)
#####simpson
fx=np.array([n for n in range(N)])*ecart
inte=ecart/6*(np.sin(0)+np.sin(np.pi/2)+2*np.sum(np.sin(fx[1:]))+4*np.sum(np.sin(fx+ecart/2)))
print(inte)
mp.prec=50

ecart=mpf(mp.pi/2/N)
fx1=[mp.sin(mpf(n)*ecart) for n in range(1,N)]
fx2=[mp.sin(mpf(n)*ecart+mpf(ecart/2)) for n in range(N)]
inte=ecart/6*(mp.sin(0)+mp.sin(mp.pi/2)+2*sum(fx1)+4*sum(fx2))
print(inte)
######
ecart=np.pi*2/N
def f(x,n):
    return x+np.sin(x)*10**n
def I(n):
    fx=np.array([n for n in range(N)])*ecart
    inte=ecart/6*(f(0,n)+f(np.pi/2,n)+2*np.sum(f(fx[1:],n))+4*np.sum(f(fx+ecart/2,n)))
    return(inte)
print(I(1))
######
mp.prec=20
def f(x,n):
    return mpf(x)+mp.sin(x)*10**n
def I(n):
    fx1=[f(i*ecart,n) for i in range(1,N)]
    fx2=[f(i*ecart+ecart/2,n) for i in range(N)]
    inte=mpf(ecart)/6*(f(0,n)+f(mp.pi/2,n)+2*sum(fx1)+4*sum(fx2))
    return inte
print(I(1))
######

def f(x):
    return 1/np.sqrt(1-x**2)
def I(episilon):
    ecart=(2-2*episilon)/N
    fx=np.array([n for n in range(N)])*ecart-1+episilon
    inte=ecart/6*(f(-1+episilon)+f(1-episilon)+2*np.sum(f(fx[1:]))+4*np.sum(f(fx+ecart/2)))
    return(inte)
epi=[10**(-n) for n in range(1,11)]

ii=[I(i)-np.pi for i in epi]
plt.plot([n for n in range(1,11)],ii)
plt.xlabel('-log(episilon)')
plt.ylabel('ecart')