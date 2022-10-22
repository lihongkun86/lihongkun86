# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 18:04:50 2022

@author: lihongkun
"""

from brownian1 import Simul_brownian
from brownian2 import Simul_brownian2
import numpy as np
import matplotlib.pyplot as plt
ensemble=100
time=5
interval=0.5
MSD=[0]
for i in np.arange(interval,time+interval,interval):
    print(i)
    msd_c=0
    for j in range(ensemble):
        #for problem1:
        # simulation = Simul_brownian(n=50,sample_time=i, sigma_small=0.02,sigma_big=0.1)
        #for problem2:
        simulation = Simul_brownian2(n=50,sample_time=i, sigma_small=0.01,sigma_big=0.2)
        _,msd=simulation.md_step()
        msd_c+=msd
    msd_c=msd_c/ensemble
    MSD.append(msd_c)
t=np.arange(0,time+interval,interval) 
parameter = np.polyfit(t, MSD, 1) 
plt.plot(t,MSD,'ro',label='original data')
plt.plot(t,parameter[0]*t+parameter[1],label='fitting')
correlation = np.corrcoef(MSD, parameter[0]*t+parameter[1])[0,1]
plt.xlabel('t')
plt.ylabel('MSD')
plt.legend()