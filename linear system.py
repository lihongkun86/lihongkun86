# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 13:31:46 2023

@author: lihongkun
"""
import numpy as np
import matplotlib.pyplot as plt
import time
import copy
#####temps de calcul
plt.figure(1)
det=[]
tt=[]
for N in range(1,101):
    
    A=np.random.randint(100,size=(N,N))
    b=np.random.randint(100,size=(N,1))
    t0=time.time_ns()
    for i in range(60):
        Ainv=np.linalg.inv(A)
    t=time.time_ns()-t0
    x=Ainv.dot(b)
    line=A.dot(x)-b
    
    det.append(np.log(np.linalg.norm(line,ord=2)))
    tt.append(t)
N=np.arange(1,101)
plt.subplot(311)
plt.plot(N,det)
plt.xlabel('N')
plt.ylabel('err')
plt.subplot(312)
plt.plot(N,tt)
plt.xlabel('N')
plt.ylabel('time')
n=np.shape(N)[0]
N=np.log(N)
tt=np.log(np.array(tt))
a=(np.sum(N)*np.sum(tt)-n*np.sum(N*tt))/(np.sum(N)**2-n*np.sum(N**2))
b=(np.sum(tt)-a*np.sum(N))/n
plt.subplot(313)
plt.plot(N,tt,label='real')
plt.plot(N,a*N+b,label='fit')
plt.xlabel('log(N)')
plt.ylabel('log(time)')
plt.legend()
#####Inversion d'une matrice de Van der Monde
plt.figure(2)
det=[]
tt=[]
for N in range(1,101):
    
    A=2*np.random.random((N,N))-1
    b=np.random.randint(100,size=(N,1))
    Ainv=np.linalg.inv(A)
    x=Ainv.dot(b)
    line=A.dot(x)-b
    
    det.append(np.log(np.linalg.norm(line,ord=2)))
    tt.append(t)
N=np.arange(1,101)
plt.plot(N,det)
plt.xlabel('N')
plt.ylabel('err')
#####Inversion d'une matrice de Van der Monde par les polynômes de Lagrange

plt.figure(3)
def A(j,N,x_random):
    x_r=np.delete(copy.deepcopy(x_random),j)
    x_rd=x_r-x_random[j]
    a=1
    for i in range(np.shape(x_rd)[0]):
        a*=x_rd[i]
    P=np.poly1d(x_r/a,True)
    return(P.coeffs)
def P(x,j,N,x_random):
    P=np.poly1d(A(j,N,x_random))
    return(P(x))
tt=[]
err=[]
for N in range(1,101):
    t0=time.time()
    x=np.zeros((N+1,N+1))
    x_random=2*np.random.random(N+1)-1
    for i in range(N+1):
        x[i,:]=x_random**i
    q=2*np.random.random((N+1,1))-1
    w=np.zeros(q.shape)
    for j in range(N+1):
        w[j]=np.sum(q*A(j,N,x_random)[::-1])
    t=time.time()-t0
    line=x.dot(w)-q  
    err.append(np.log(np.linalg.norm(line,ord=2)))
    tt.append(t)
N=np.arange(1,101)
plt.subplot(211)
plt.plot(N,err)
plt.xlabel('N')
plt.ylabel('err')
plt.subplot(212)
plt.plot(N,tt)
plt.xlabel('N')
plt.ylabel('time')