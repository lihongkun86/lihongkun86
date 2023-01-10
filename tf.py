# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:53:55 2023

@author: lihongkun
"""

import numpy as np
import matplotlib.pyplot as plt
import time
####signal
fe=20e6
fc=1e6
bw=1
detat=1/fe
N=200
t=np.arange(0,N*detat,detat)
arf=np.pi/np.log(2)*(bw*fc/2)**2
sj=np.sin(2*np.pi*fc*t)*np.exp(-arf*t**2)
plt.figure(1)
plt.plot(t,sj)
plt.ylabel('amplitude')
plt.xlabel('t(s)')
plt.title('signal(t)')
####TF
k=np.arange(N)
sk=np.zeros(k.shape,dtype=complex)
for k in range(N):
    for i in range(N):
        sk[k]+=sj[i]*np.exp(1j*2*np.pi*i*k/N)
f=np.linspace(-fe/2,fe/2,N)
plt.figure(2)
plt.plot(f,np.abs(sk))
plt.ylabel('amplitude')
plt.xlabel('f(Hz)')
plt.title('s[k]-f')
sj2=np.sum(np.abs(sj)**2)
sk2=np.sum(np.abs(sk)**2)
ran=2*np.random.random(N)-1
sk_ran=np.zeros(sk.shape,dtype=complex)
for k in range(N):
    for i in range(N):
        sk_ran[k]+=ran[i]*np.exp(1j*2*np.pi*i*k/N)
f=np.linspace(-fe/2,fe/2,N)
plt.figure(3)
plt.plot(f,np.abs(sk_ran))
plt.ylabel('amplitude')
plt.xlabel('f(Hz)')
plt.title('s_random[k]-f')
###1ère approche
t_initial=[]
for n in range(10,31): 
    print('n=',n)
    t=np.arange(0,detat*n**2,detat)
    arf=np.pi/np.log(2)*(bw*fc/2)**2
    sj=np.sin(2*np.pi*fc*t)*np.exp(-arf*t**2)
    sk_ini=np.zeros(n**2,dtype=complex)
    ini_time=time.time()
    for k in range(n**2):
        for i in range(n**2):
            sk_ini[k]+=sj[i]*np.exp(1j*2*np.pi*i*k/n**2)
    t=time.time()-ini_time
    t_initial.append(t)
t_1app=[]
for n in range(10,31):
    print('n=',n)
    t=np.arange(0,detat*n**2,detat)
    arf=np.pi/np.log(2)*(bw*fc/2)**2
    sj=np.sin(2*np.pi*fc*t)*np.exp(-arf*t**2)
    w=np.exp(1j*2*np.pi/n**2)
    ini_time=time.time()
    s1=np.zeros(n**2,dtype=complex)
    for k0 in range(n):
        for j0 in range(n):
            for j1 in range(n):
                s1[k0*n+j0]+=sj[j1*n+j0]*w**(j1*k0*n)
    sk_1app=np.zeros(n**2,dtype=complex)
    for k0 in range(n):
        for k1 in range(n):
            for j0 in range(n):
                sk_1app[k1*n+k0]+=s1[k0*n+j0]*w**(j0*(k1*n+k0))
    t=time.time()-ini_time
    t_1app.append(t)
plt.figure(4)
nn=np.arange(10,31)
plt.plot(nn,t_initial,label='initial')
plt.plot(nn,t_1app,label='first approch')
plt.xlabel('n')
plt.ylabel('t(s)')
plt.legend()
plt.figure(5)
f=np.linspace(-fe/2,fe/2,900)
plt.plot(f,abs(sk_ini),label='initial')
plt.plot(f,abs(sk_1app),label='first approch')
plt.ylabel('amplitude')
plt.xlabel('f(Hz)')
plt.title('n=30')
plt.legend()
####Cooley-Tukey
N=900
t=np.arange(0,N*detat,detat)
arf=np.pi/np.log(2)*(bw*fc/2)**2
sj=np.sin(2*np.pi*fc*t)*np.exp(-arf*t**2)
sk_ct=np.fft.fft(sj)
plt.figure(6)
f=np.linspace(-fe/2,fe/2,N)
plt.plot(f,abs(sk_ini),label='initial')
plt.plot(f,abs(sk_1app),label='first approch')
plt.plot(f,abs(sk_ct),label='Cooley-Tukey')
plt.ylabel('amplitude')
plt.xlabel('f(Hz)')
plt.legend()
####convolution
def door(t):
    if t>=0 and t<=1/2:
        return 1
    else:
        0
N=900
t=np.arange(0,N*detat,detat)
arf=np.pi/np.log(2)*(bw*fc/2)**2
sj=np.sin(2*np.pi*fc*t)*np.exp(-arf*t**2)
do=door(t)
cov=np.fft.ifft(np.fft.fft(sj)*np.fft.fft(do))