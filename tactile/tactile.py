# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 14:37:36 2023

@author: lihongkun
"""

import numpy as np
import matplotlib.pyplot as plt
np.seterr(divide='ignore',invalid='ignore')
a=0.15
b=0.10
l=2*a#length
w=2*b#width
c=2400#velocity
rx=0.8#reflection coefficient of x
ry=0.9#reflection coefficient of y

fe=20e6# sample frequence
fc=1e6#central frequence
#position of the source
x_source=-0.1
y_source=-0.05
#positions of two receptors
x_r1=0
y_r1=0
x_r2=0.05
y_r2=0
bw=1#relative bandwidth
detat=1/fe
N=12000
# t=np.arange(0,N*detat,detat)
arf=np.pi/np.log(2)*(bw*fc/2)**2
def signal(t):
    sj=np.sin(2*np.pi*fc*t)*np.exp(-arf*t**2)
    return sj
def xm(x_order,x_s):#xm
   return 2*x_order*a+((-1)**x_order)*x_s
def yn(y_order,y_s):#yn
   return 2*y_order*b+((-1)**y_order)*y_s
def recept(order,t,x_s,y_s,fre_cental):
    k=2*np.pi*fre_cental/c
    if order==0:
        rmn10=np.sqrt((xm(0,x_s)-x_r1)**2+(yn(0,y_s)-y_r1)**2)
        s_recept1=np.exp(-1j*k*rmn10)/rmn10*signal(t-rmn10/c)
        rmn20=np.sqrt((xm(0,x_s)-x_r2)**2+(yn(0,y_s)-y_r2)**2)
        s_recept2=np.exp(-1j*k*rmn20)/rmn20*signal(t-rmn20/c)
    else:
        s_recept1=0
        s_recept2=0
        for i in range(order+1):
            j=order-i
            if i==0 or j==0:               
                rmn1_positive=np.sqrt((xm(i,x_s)-x_r1)**2+(yn(j,y_s)-y_r1)**2)
                rmn1_negative=np.sqrt((xm(-i,x_s)-x_r1)**2+(yn(-j,y_s)-y_r1)**2)
                s_recept1+=np.exp(-1j*k*rmn1_positive)/rmn1_positive*(rx**i)*(ry**j)*signal(t-rmn1_positive/c)+\
                    np.exp(-1j*k*rmn1_negative)/rmn1_negative*(rx**i)*(ry**j)*signal(t-rmn1_negative/c)
                rmn2_positive=np.sqrt((xm(i,x_s)-x_r2)**2+(yn(j,y_s)-y_r2)**2)
                rmn2_negative=np.sqrt((xm(-i,x_s)-x_r2)**2+(yn(-j,y_s)-y_r2)**2)
                s_recept2+=np.exp(-1j*k*rmn2_positive)/rmn2_positive*(rx**i)**(ry**j)*signal(t-rmn2_positive/c)+\
                    np.exp(-1j*k*rmn2_negative)/rmn2_negative*(rx**i)*(ry**j)*signal(t-rmn2_negative/c)
            else:
                rmn1_1=np.sqrt((xm(i,x_s)-x_r1)**2+(yn(j,y_s)-y_r1)**2)
                rmn1_2=np.sqrt((xm(-i,x_s)-x_r1)**2+(yn(-j,y_s)-y_r1)**2)
                rmn1_3=np.sqrt((xm(i,x_s)-x_r1)**2+(yn(-j,y_s)-y_r1)**2)
                rmn1_4=np.sqrt((xm(-i,x_s)-x_r1)**2+(yn(j,y_s)-y_r1)**2)
                s_recept1+=np.exp(-1j*k*rmn1_1)/rmn1_1*(rx**i)*(ry**j)*signal(t-rmn1_1/c)+\
                    np.exp(-1j*k*rmn1_2)/rmn1_2*(rx**i)*(ry**j)*signal(t-rmn1_2/c)+\
                    np.exp(-1j*k*rmn1_3)/rmn1_3*(rx**i)*(ry**j)*signal(t-rmn1_3/c)+\
                    np.exp(-1j*k*rmn1_4)/rmn1_4*(rx**i)*(ry**j)*signal(t-rmn1_4/c)
                rmn2_1=np.sqrt((xm(i,x_s)-x_r2)**2+(yn(j,y_s)-y_r2)**2)
                rmn2_2=np.sqrt((xm(-i,x_s)-x_r2)**2+(yn(-j,y_s)-y_r2)**2)
                rmn2_3=np.sqrt((xm(i,x_s)-x_r2)**2+(yn(-j,y_s)-y_r2)**2)
                rmn2_4=np.sqrt((xm(-i,x_s)-x_r2)**2+(yn(j,y_s)-y_r2)**2)
                s_recept2+=np.exp(-1j*k*rmn2_1)/rmn2_1*(rx**i)**(ry**j)*signal(t-rmn2_1/c)+\
                    np.exp(-1j*k*rmn2_2)/rmn2_2*(rx**i)*(ry**j)*signal(t-rmn2_2/c)+\
                    np.exp(-1j*k*rmn2_3)/rmn2_3*(rx**i)*(ry**j)*signal(t-rmn2_3/c)+\
                    np.exp(-1j*k*rmn2_4)/rmn2_4*(rx**i)*(ry**j)*signal(t-rmn2_4/c)
    return([s_recept1,s_recept2])
def corr(s1,s2):#correlation coefficient
    e1=np.sum(np.abs(s1)**2)
    e2=np.sum(np.abs(s2)**2)
    return 1/np.sqrt(e1*e2)*np.max(np.abs(np.fft.ifft(np.fft.fft(s1)*np.conjugate(np.fft.fft(s2)))))
def phasecorr(s1,s2):#phase correlation coefficient
    medium0=np.fft.fft(s1)*np.conjugate(np.fft.fft(s2))
    module=medium0/np.abs(medium0)
    module[np.isnan(module)]=0
    medium=np.fft.ifft(module)
    return np.max(np.abs(medium))
tt=np.arange(0,N*detat,detat)
recept10=recept(0,tt,x_source,y_source,fc)[0]#order0
recept11=recept(1,tt,x_source,y_source,fc)[0]#order1
recept12=recept(2,tt,x_source,y_source,fc)[0]#order2

plt.figure(1)
plt.plot(tt,recept10,label='receptor1,order 0')
plt.plot(tt,recept11,label='receptor1,order 1')
plt.plot(tt,recept12,label='receptor1,order 2')
plt.ylabel('amplitude')
plt.xlabel('t(s)')
plt.title('signal(t) received by receptors')
plt.legend()
y_serie=np.arange(-0.1,0.11,0.02)
sig=signal(tt)
plt.figure(2)
for fc1 in np.arange(1e6,1.5e6,1e5):
    cor=[]
    for y in y_serie:
        recept1=0
        recept2=0
        for i in range(5):
            recept1+=recept(i,tt,x_source,y,fc1)[0]
            recept2+=recept(i,tt,x_source,y,fc1)[1]
        corr1=corr(recept1,sig)
        corr2=corr(recept2,sig)
        corr_mean=(corr1+corr2)/2#mean coefficients of two receptors
        cor.append(corr_mean)
    plt.plot(y_serie,cor,label='frequence='+str(fc1/1e6)+'MHz')
plt.ylabel('C')
plt.xlabel('y/m (x_source={}m)'.format(x_source))
plt.legend()

plt.figure(3)
for fc1 in np.arange(1e6,1.5e6,1e5):
    cor=[]
    for y in y_serie:
        recept1=0
        recept2=0
        for i in range(5):
            recept1+=recept(i,tt,x_source,y,fc1)[0]
            recept2+=recept(i,tt,x_source,y,fc1)[1]
        corr1=phasecorr(recept1,sig)
        corr2=phasecorr(recept2,sig)
        corr_mean=(corr1+corr2)/2
        cor.append(corr_mean)
    plt.plot(y_serie,cor,label='frequence='+str(fc1/1e6)+'MHz')
plt.ylabel('phase correlation')
plt.xlabel('y/m (x_source={}m)'.format(x_source))
plt.legend()