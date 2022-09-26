import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import EllipseCollection
from matplotlib.patches import Rectangle
from simul import Simul


class AnimateSimul:
    def __init__(self, simulation):
        print('AnimateSimul')
        self.simulation = simulation
        self.fig, self.ax = plt.subplots(figsize=(5, 5))  # initialise  graphics
        self.circles = EllipseCollection(widths=2*simulation.sigma, heights=2*simulation.sigma, angles=0, units='x',
                                         offsets=simulation.position, transOffset=self.ax.transData)  # circles at pos
        self.ax.add_collection(self.circles)
        rect = Rectangle((0, 0), 1, 1, ec='black', facecolor='none')   #   enclosing box
        self.ax.set_xlim(left=-.1, right=1.1)
        self.ax.set_ylim(bottom=-.1, top=1.1)
        self.ax.add_patch(rect)

    def _anim_step(self, m):  # m is the number of calls that have occurred to this function
        print('anim_step m = ', m)
        self.simulation.md_step()  # perform simulation step
#  calculation a window containing the particles and reset axes
      #  rmin = np.amin(self.simulation.position) - self.simulation.sigma/2. - .1
       # rmax = np.amax(self.simulation.position) + self.simulation.sigma/2. + .1
      #  rmin = min(-.1, rmin)
      #  rmax = max(1.1, rmax)
      #  self.ax.set_xlim(left=rmin, right=rmax)
      #  self.ax.set_ylim(bottom=rmin, top=rmax)
# signal graphics update
        self.circles.set_offsets(self.simulation.position) 

    def go(self, nframes):
        print('go')
        self._ani = animation.FuncAnimation(self.fig, func=self._anim_step, frames=nframes,
                                      repeat=False, interval=20)  # run animation
        plt.show()
