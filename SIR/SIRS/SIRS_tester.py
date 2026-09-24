from SIRS import SIRS
import numpy as np

lattice = SIRS(size=(100, 100), ini='random', p1=0.8, p2=0.1, p3=0.01)
lattice.run_animation(sweeps=1000000, it_per_sweep=10000)
