# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 02:31:45 2022

@author: lihongkun
"""

from brownian2 import Simul_brownian2
from brownian_animatesimul2 import AnimateSimul


def main():

    simulation = Simul_brownian2(n=150,sample_time=0.01, sigma_small=0.01,sigma_big=0.3)  #  sigma particle radius
    print(simulation.__doc__)  # print the documentation from the class

    animate = AnimateSimul(simulation)
    animate.go(nframes=500)
    print(simulation)  #  print last configuration to screen


if __name__ == '__main__':
    main()