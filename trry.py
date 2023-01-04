# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:27:51 2022

@author: lihongkun
"""

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
def pdf(x,N):
    return N*np.exp(-x)*(1- np.exp(-x))**(N-1)

# x=np.linspace(0,10,100)

# plt.plot(x,pdf(x,1),'-',label='N='+str(1))
# plt.plot(x,pdf(x,2),'--',label='N='+str(2))
# plt.plot(x,pdf(x,3),'*',label='N='+str(3))
# plt.plot(x,pdf(x,4),'.',label='N='+str(4))
# plt.xlabel('y')
# plt.ylabel('qn(y)')
# plt.legend()
def g_pdf(z):
    return np.exp(-z-np.exp(-z))

x=np.linspace(-10,10,100)

plt.plot(x,g_pdf(x))
plt.xlabel('z')
plt.ylabel(chr(960)+'(z)')
plt.show()
# def expdf(x,lamda):
#     return lamda*np.exp(-lamda*x)
# lam=np.arange(1,5)
# x=np.zeros((4,10000))
# for j in range(1,5):
#     x[j-1,:]=np.random.exponential(1/j,10000)
# x=np.min(x,axis=0)
# n,bins,patches=plt.hist(x,bins=100,density=True)
# y=expdf(bins,10)
# plt.plot(bins,y,label=chr(960)+'(x)=10exp(-10x)')
# plt.xlabel('x')
# plt.ylabel('pdf')
# plt.legend()