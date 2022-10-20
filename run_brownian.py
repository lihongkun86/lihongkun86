# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:49:05 2022

@author: lihongkun
"""

from brownian import Simul_brownian
from brownian_animatesimul import AnimateSimul


def main():
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    simulation = Simul_brownian(n=100,sample_time=0.01, sigma_small=0.02,sigma_big=0.1)  #  sigma particle radius
    print(simulation.__doc__)  # print the documentation from the class

    animate = AnimateSimul(simulation)
    animate.go(nframes=500)
    print(simulation)  #  print last configuration to screen


if __name__ == '__main__':
    main()