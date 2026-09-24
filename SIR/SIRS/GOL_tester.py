from GOL import GOL
import numpy as np

lattice = GOL(size=(50, 50), ini='random')
lattice.run_animation(sweeps=1000000, it_per_sweep=1)
