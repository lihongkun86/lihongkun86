# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 01:46:03 2022

@author: lihongkun
"""

import numpy as np
import itertools
import copy
class Simul_brownian2:
    """ 
    This is the prototype of the simulation code
    It moves the particles with at _velocity, using a vector notation: numpy should be used.
    """
    def __init__(self, n,sample_time, sigma_small,sigma_big,m_h=20):
        np.random.seed(1)
        print("Simul init")
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

        ecart=(np.sqrt(2)*self.sigma_big)/(number+1)
        # for i in range(self.n):
        #     self.position[i+1]=self.position[0,:]-self.sigma_big+np.array([(i%number+1)*ecart,(i//number+1)*ecart])
        self.position[1:,0]=self.position[0,0]-self.sigma_big*np.sqrt(2)/2+(np.arange(self.n)%number+1)*ecart
        self.position[1:,1]=self.position[0,1]-self.sigma_big*np.sqrt(2)/2+(np.arange(self.n)//number+1)*ecart
        self.sigma=np.ones((self.n+1,1))*self.sigma_small
        self.sigma[0]=-self.sigma_big
        self.m=np.ones((self.n+1,1))*self.m_l
        self.m[0]=self.m_h
        self._velocity = np.random.normal(size=self.position.shape)  # random velocities
        self._velocity[0,:]=np.zeros((1,2))
        self._i, self._j = np.triu_indices(self.position.shape[0], k=1)  # all pairs of indices between particles
        self._sample_time=sample_time
        
        

    
    def _wall_time(self):
        velocity=copy.deepcopy(self._velocity[0])
        velocity[np.where(velocity==0)]+=1e-8
        t=np.where(velocity>0,(self.bord_large-self.sigma_big-self.position[0,:])/velocity,\
                   (self.bord_small+self.sigma_big-self.position[0,:])/velocity)
        
        
     
        direction=t.argmin()
        disk=0
        return t.min(),disk,direction
       
    def _pair_time(self):
        rij = self.position[self._i]-self.position[self._j]  # set of all 6 separation vectors
        vij = self._velocity[self._i]-self._velocity[self._j]
        rij1 = rij[self.n:,:]
        vij1 = vij[self.n:,:]
        rij_sq1 = (rij1**2).sum(1)
        vij_sq1 = (vij1**2).sum(1)
        b1=2*(rij1[:,0]*vij1[:,0]+rij1[:,1]*vij1[:,1])
        c1=rij_sq1-((self.sigma[self._i[self.n:],0]+self.sigma[self._j[self.n:],0])**2)    
        t1=np.where((b1**2-4*vij_sq1*c1>0)&(b1<0)&(c1>0),(-b1-np.sqrt(abs(b1**2-4*vij_sq1*c1)))/(2*vij_sq1),2*self._sample_time)
        
        rij2 = rij[:self.n,:]
        vij2 = vij[:self.n,:]
        rij_sq2 = (rij2**2).sum(1)
        vij_sq2 = (vij2**2).sum(1)
        b2=2*(rij2[:,0]*vij2[:,0]+rij2[:,1]*vij2[:,1])
        c2=rij_sq2-((self.sigma[self._i[:self.n],0]+self.sigma[self._j[:self.n],0])**2)    
        t2=np.where((b2**2-4*vij_sq2*c2>0)&(c2<0),(-b2+np.sqrt(abs(b2**2-4*vij_sq2*c2)))/(2*vij_sq2),2*self._sample_time)
        if t1.min()<t2.min():
            pair=t1.argmin()
            t_pair=t1.min()
            i=self._i[self.n:]
            j=self._j[self.n:]
            pair1=i[pair]
            pair2=j[pair]
            
        else:
            pair=t2.argmin()
            t_pair=t2.min()
            i=self._i[:self.n]
            j=self._j[:self.n]
            pair1=i[pair]
            pair2=j[pair]
            
        return t_pair,pair1,pair2
        
    def md_step(self):
        print('Simul::md_step')
        momentum = 0
        time = 0#total time
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
        pressure = momentum/self._sample_time
        return pressure

    def __str__(self):   # this is used to print the position and velocity of the particles
        p = np.array2string(self.position)
        v = np.array2string(self._velocity)
        return 'pos= '+p+'\n'+'vel= '+v+'\n'