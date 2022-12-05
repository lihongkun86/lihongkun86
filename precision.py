# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 09:20:07 2022

@author: lihongkun
"""

from mpmath import *
import time
from math import * 
import numpy as np
import matplotlib.pyplot as plt
print(mp)

#print(mp.pi)
######first######
for i in [1.,10**3,10**6,10**9]:
    x=mpf(i)
    n=0
    while True:
        x_=x+2**(-n)
        if x_==x:
            print(n)
            break
        n+=1
########second##########

n=0
while True:
    a=mpf(10**(n))
    b=mpf(-10**(n))
    c=mpf(1.)
    
    if (a+b)+c!=a+(b+c):
        print(n)
        break
    n+=1
########third#########
n=20

x21=mpf((0.5-10.**(-n))/(1.-10.**(-n)))
x22=mpf((1.-0.5*10.**(n))/(1.-10.**(n)))
print(x21,x22,x22-x21)
    

#########
# def factor(n):
#     if n==0:
#         return 1
#     if n>0:
#         return n*factor(n-1)

# def u(x,n):
#     return x**(2*n)/(factor(2*n))
# def S(x,N):
#     s=0
#     for i in range(N+1):
#         s+=((-1)**i)*u(x,i)
#     return(s)
# x=1.5
# nn=[k for k in range(85)]
# t=[]
# for j in nn:
#     start=time.time()
#     s=S(x,j)
#     end=time.time()
#     t.append(end-start)
# plt.plot(nn,t)
# plt.xlabel('N')
# plt.ylabel('t')
############

def S(x,N):
    s=1
    ss=1
    for i in range(1,N+1):
        s=(x**2/((2*(i-1)+2)*(2*(i-1)+1)))*s
        ss+=((-1)**i)*s
    return(ss)
x=1
long=85
nn=[k for k in range(long)]
cst=np.ones(long)*np.cos(x)
ss=[]
for j in nn:
    s=S(x,j)
    
    ss.append(s)
plt.plot(nn,ss)
plt.plot(nn,cst)
plt.xlabel('N')
plt.ylabel('S')