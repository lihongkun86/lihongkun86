# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 17:28:08 2022

@author: lihongkun
"""

import numpy as np


class Simul_n:
    """ 
    This is the prototype of the simulation code
    It moves the particles with at _velocity, using a vector notation: numpy should be used.
    """
    def __init__(self, n,sample_time, sigma):
        np.random.seed(1)
        print("Simul init")
        self.n=n
        self.position = np.zeros((self.n,2))  # starting positions
        self.bord_large=1
        self.bord_small=0
        number=int(np.sqrt(self.n))+1
        ecart=(self.bord_large-self.bord_small)/(number+1)
        for i in range(self.n):
            self.position[i]=np.array([(i//number+1)*ecart,(i%number+1)*ecart])
            
        self._velocity = np.random.normal(size=self.position.shape)  # random velocities
        self._i, self._j = np.triu_indices(self.position.shape[0], k=1)  # all pairs of indices between particles
        self.sigma = sigma  # particle radius
        self._sample_time=sample_time
        self.m=1
        

    # def _wall_time(self,time):
    #     collision_time=[]
    #     par_involve=[]
    #     wall=[]
    #     for i in range(int(time/self._sample_time)):
    #         self.md_step()
    #         posi_index=np.where(np.logical_or(self.position<=self.bord_small+self.sigma,self.position>=self.bord_large-self.sigma))
    #         if np.shape(posi_index[0])[0]!=0:
    #             collision_time.append(i*self._sample_time)
    #             par_involve.append(posi_index[0])
    #             for j in range(np.shape(posi_index[0])[0]):
    #                 condition_x=self.position[posi_index[0][j]][0]<=self.bord_small+self.sigma or self.position[posi_index[0][j]][0]>=self.bord_large-self.sigma
    #                 condition_y=self.position[posi_index[0][j]][1]<=self.bord_small+self.sigma or self.position[posi_index[0][j]][1]>=self.bord_large-self.sigma
    #                 if condition_x==True and condition_y==False:
    #                     wall.append('x')
    #                     self._velocity[posi_index[0][j]][1]=-self._velocity[posi_index[0][j]][1]
    #                 if condition_x==False and condition_y==True:
    #                     wall.append('y')
    #                     self._velocity[posi_index[0][j]][0]=-self._velocity[posi_index[0][j]][0]
    #                 if condition_x==True and condition_y==True:
    #                     wall.append('x and y')
    #                     self._velocity[posi_index[0][j]]=-self._velocity[posi_index[0][j]]
    #     return collision_time,par_involve,wall
    def _wall_time(self):
        t=np.where(self._velocity>0,(self.bord_large-self.sigma-self.position)/self._velocity,\
                   (self.bord_small+self.sigma-self.position)/self._velocity)
        disk,direction=np.unravel_index(t.argmin(),t.shape)
        return t[disk,direction],disk,direction
        # collision_time=np.array([])
        # par_involve=np.array([])
        # wall=np.array([])
        # times=0
        # while times>-1:
        #     wall_running=np.zeros(np.shape(self.position)[0])
        #     collision_timing=np.zeros(np.shape(self.position)[0])
        #     #4 conditions
        #     con_y_large=np.logical_and(self._velocity[:,1]>0,line_y((np.sign(self._velocity[:,0])+1)/2,self._velocity,self.position)>(self.bord_large-self.sigma))
        #     con_y_small=np.logical_and(self._velocity[:,1]<0,line_y((np.sign(self._velocity[:,0])+1)/2,self._velocity,self.position)<(self.bord_small+self.sigma))
        #     con_x_large=np.logical_and(self._velocity[:,0]>0,line_x((np.sign(self._velocity[:,1])+1)/2,self._velocity,self.position)>(self.bord_large-self.sigma))
        #     con_x_small=np.logical_and(self._velocity[:,0]<0,line_x((np.sign(self._velocity[:,1])+1)/2,self._velocity,self.position)<(self.bord_small+self.sigma))
        #     #wall
        #     wall_running[np.where(con_x_large)]=1 #1 for y
        #     wall_running[np.where(con_x_small)]=1
        #     #time
        #     collision_timing[np.where(con_y_large)]=np.abs((self.bord_large-self.sigma-self.position[np.where(con_y_large)][:,1])/self._velocity[np.where(con_y_large)][:,1])
        #     collision_timing[np.where(con_y_small)]=np.abs((self.bord_small+self.sigma-self.position[np.where(con_y_small)][:,1])/self._velocity[np.where(con_y_small)][:,1])
        #     collision_timing[np.where(con_x_large)]=np.abs((self.bord_large-self.sigma-self.position[np.where(con_x_large)][:,0])/self._velocity[np.where(con_x_large)][:,0])
        #     collision_timing[np.where(con_x_small)]=np.abs((self.bord_small+self.sigma-self.position[np.where(con_x_small)][:,0])/self._velocity[np.where(con_x_small)][:,0])
        #     #reset position and velocity
        #     self.position[np.where(con_y_large)][:,0]=line_x(self.bord_large-self.sigma,self._velocity[np.where(con_y_large)],self.position[np.where(con_y_large)])
        #     self.position[np.where(con_y_large)][:,1]=self.bord_large-self.sigma
        #     self.position[np.where(con_y_small)][:,0]=line_x(self.bord_small+self.sigma,self._velocity[np.where(con_y_small)],self.position[np.where(con_y_small)])
        #     self.position[np.where(con_y_small)][:,1]=self.bord_small+self.sigma
        #     self.position[np.where(con_x_large)][:,0]=self.bord_large-self.sigma
        #     self.position[np.where(con_x_large)][:,1]=line_y(self.bord_large-self.sigma,self._velocity[np.where(con_x_large)],self.position[np.where(con_x_large)])
        #     self.position[np.where(con_x_small)][:,0]=self.bord_small+self.sigma
        #     self.position[np.where(con_x_small)][:,1]=line_y(self.bord_small+self.sigma,self._velocity[np.where(con_x_small)],self.position[np.where(con_x_small)])
        #     self._velocity[np.where(con_y_large)][:,1]=-self._velocity[np.where(con_y_large)][:,1]
        #     self._velocity[np.where(con_y_small)][:,1]=-self._velocity[np.where(con_y_small)][:,1]
        #     self._velocity[np.where(con_x_large)][:,0]=-self._velocity[np.where(con_x_large)][:,0]
        #     self._velocity[np.where(con_x_small)][:,0]=-self._velocity[np.where(con_x_small)][:,0]
            
            
            
        #     if times!=0:
        #         collision_timing+=collision_time[-np.shape(self.position)[0]:]
        #     if np.max(collision_timing)> self._sample_time:
        #         break
        #     collision_time=np.hstack((collision_time,collision_timing))
        #     wall=np.hstack((wall,wall_running))
        #     par_involve=np.hstack((par_involve,np.arange(np.shape(self.position)[0])))
        #     times+=1
        # #sort
        # index=np.argsort(collision_time)
        # collision_time=collision_time[index]
        # par_involve=par_involve[index]
        # wall=wall[index]
        # return collision_time,par_involve,wall
    def _pair_time(self):
        rij = self.position[self._i]-self.position[self._j]  # set of all 6 separation vectors
        vij = self._velocity[self._i]-self._velocity[self._j]
        rij_sq = (rij**2).sum(1)
        vij_sq = (vij**2).sum(1)
        b=2*(rij[:,0]*vij[:,0]+rij[:,1]*vij[:,1])
        c=rij_sq-4*(self.sigma**2)    
        t=np.where(np.logical_and(b**2-4*vij_sq*c>0,b<0),(-b-np.sqrt(abs(b**2-4*vij_sq*c)))/(2*vij_sq),2*self._sample_time)
        
        pair=t.argmin()
        t_pair=t.min()

        return t_pair,self._i[pair],self._j[pair]
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
                rij = self.position[pair2]-self.position[pair1]
                rij_sq = np.sum(rij**2)
                rij_unit = rij/np.sqrt(rij_sq)
                v_diff=self._velocity[pair1]-self._velocity[pair2]
                self._velocity[pair1] -= rij_unit*(np.sum(rij_unit*v_diff))
                self._velocity[pair2] += rij_unit*(np.sum(rij_unit*v_diff))
         
        time_to_sample=self._sample_time-time
        self.position += time_to_sample * self._velocity
        pressure = momentum/self._sample_time
        return pressure

    def __str__(self):   # this is used to print the position and velocity of the particles
        p = np.array2string(self.position)
        v = np.array2string(self._velocity)
        return 'pos= '+p+'\n'+'vel= '+v+'\n'