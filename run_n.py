# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 18:08:39 2022

@author: lihongkun
"""

from simul_n import Simul_n
from animatesimul import AnimateSimul


def main():

    simulation = Simul_n(500,sample_time=0.01, sigma=0.02)  #  sigma particle radius
    print(simulation.__doc__)  # print the documentation from the class

    animate = AnimateSimul(simulation)
    animate.go(nframes=500)
    print(simulation)  #  print last configuration to screen


if __name__ == '__main__':
    main()