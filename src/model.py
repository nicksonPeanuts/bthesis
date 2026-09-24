
import numpy as np
from cellular_automata.cellular_automata import CellularAutomata as ca

"""

The main idea is to take a cellular automata

and obtain from it the frames of the evolutions

"""


model = ca(width=50,height=50, input_array='', generations=100, save_image=True,save_movie=False,
                  save_data=True, filename='testautomata')

model.game_of_life()

