# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:02:27 2022

@author: lihongkun
"""

import numpy as np
import itertools
import copy
class Simul_brownian:
    """ 
    This is the prototype of the simulation code
    It moves the particles with at _velocity, using a vector notation: numpy should be used.
    """
    def __init__(self, n,sample_time, sigma_small,sigma_big,m_h=20):
        # np.random.seed(1)
        # print("Simul init")
        self.n=n
        self.position = np.zeros((self.n+1,2))  # starting positions
        self.bord_large=1
        self.bord_small=0
        self.sigma_big=sigma_big
        self.sigma_small = sigma_small  # particle radius
        self.m_l=1
        self.m_h=m_h
        self.position[0,:]=np.random.rand(1,2)*(self.bord_large-2*self.sigma_big)+self.sigma_big
        if np.sqrt(self.n)==int(np.sqrt(self.n)):
            number=int(np.sqrt(self.n))

        else:
            number=int(np.sqrt(self.n))+1

        ecart=(self.bord_large-self.bord_small)/(number+1)
        self.position[1:,0]=(np.arange(self.n)%number+1)*ecart
        self.position[1:,1]=(np.arange(self.n)//number+1)*ecart
        ind=np.where(np.sum((self.position[1:,:]-self.position[0,:])**2,axis=1)<=(self.sigma_small+self.sigma_big)**2)
        ecart1=(self.bord_large-self.bord_small)/(np.shape(ind[0])[0]+1)
        self.position[ind[0]+1,0]=(np.arange(np.shape(ind[0])[0])+1)*ecart1
        self.position[ind[0]+1,1]=self.bord_large-2*self.sigma_small
        self.sigma=np.ones((self.n+1,1))*self.sigma_small
        self.sigma[0]=self.sigma_big
        self.m=np.ones((self.n+1,1))*self.m_l
        self.m[0]=self.m_h
        self._velocity = np.random.normal(size=self.position.shape)  # random velocities
        self._velocity[0,:]=np.zeros((1,2))
        self._i, self._j = np.triu_indices(self.position.shape[0], k=1)  # all pairs of indices between particles
        self._sample_time=sample_time
        
        

    
    def _wall_time(self):
        velocity=copy.deepcopy(self._velocity)
        velocity[np.where(velocity==0)]+=1e-8
        t=np.where(velocity>0,(self.bord_large-self.sigma-self.position)/velocity,\
                   (self.bord_small+self.sigma-self.position)/velocity)
        disk,direction=np.unravel_index(t.argmin(),t.shape)
        return t[disk,direction],disk,direction
       
    def _pair_time(self):
        rij = self.position[self._i]-self.position[self._j]  # set of all 6 separation vectors
        vij = self._velocity[self._i]-self._velocity[self._j]
        
        rij_sq = (rij**2).sum(1)
        vij_sq = (vij**2).sum(1)
        b=2*(rij[:,0]*vij[:,0]+rij[:,1]*vij[:,1])
        c=rij_sq-((self.sigma[self._i,0]+self.sigma[self._j,0])**2)    
        t=np.where((b**2-4*vij_sq*c>0)&(b<0)&(c>0),(-b-np.sqrt(abs(b**2-4*vij_sq*c)))/(2*vij_sq),2*self._sample_time)
        
        pair=t.argmin()
        
        t_pair=t.min()
        return t_pair,self._i[pair],self._j[pair]
        
    def md_step(self):
        # print('Simul::md_step')
        momentum = 0
        time = 0#total time
        position0=copy.deepcopy(self.position[0,:])
        while True:
            next_wall_time,disk,direction=self._wall_time()
            next_pair_time,pair1,pair2=self._pair_time()
            t = min(next_wall_time,next_pair_time)

            if time+t > self._sample_time:
                break
            
            time+=t
            self.position += t * self._velocity
            if next_pair_time>next_wall_time:
                momentum += 2*self.m*self._velocity[disk,direction]
                self._velocity[disk,direction]  *=  -1
        
            else:
                rij = self.position[pair1]-self.position[pair2]
                rij_sq = np.sum(rij**2)
                rij_unit = rij/np.sqrt(rij_sq)
                v1=copy.deepcopy(self._velocity[pair1])
                v2=copy.deepcopy(self._velocity[pair2])
                m1=self.m[pair1,0]
                m2=self.m[pair2,0]
                self._velocity[pair1] = v1-2*m2/(m1+m2)*rij_unit*(np.sum(rij_unit*(v1-v2)))
                self._velocity[pair2] = v2+2*m1/(m1+m2)*rij_unit*(np.sum(rij_unit*(v1-v2)))
                
                
        time_to_sample=self._sample_time-time
        self.position += time_to_sample * self._velocity
        msd=((self.position[0,:]-position0)**2).sum()
        pressure = momentum/self._sample_time
        return pressure,msd

    def __str__(self):   # this is used to print the position and velocity of the particles
        p = np.array2string(self.position)
        v = np.array2string(self._velocity)
        return 'pos= '+p+'\n'+'vel= '+v+'\n'
# simulation = Simul_brownian(n=3,sample_time=1, sigma_small=0.02,sigma_big=0.12)
# print(simulation.m)