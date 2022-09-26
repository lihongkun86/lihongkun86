from simul import Simul
from animatesimul import AnimateSimul


def main():

    simulation = Simul(sample_time=0.01, sigma=0.15)  #  sigma particle radius
    print(simulation.__doc__)  # print the documentation from the class

    animate = AnimateSimul(simulation)
    animate.go(nframes=100)
    print(simulation)  #  print last configuration to screen


if __name__ == '__main__':
    main()
