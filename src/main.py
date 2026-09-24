#!/usr/bin/env python3

import os
import random
import sys
import numpy as np
from gameoflife import GameOfLife


#
#       
#   TODO: condizioni iniziali ( come le setto per far variare gli esperimenti? )
#         capire come rendere modello stocastico o deterministico
#         capire come gestire la questione degli intorni, -> MOORE/VON NEUMANN
#       


# Start the Game of Life
run = "r"
num_generations = 0

# dataset per la nostra bella rete neurale
dataset = None

# Instanziamo la classe GameOfLife
cellular_automata = GagithumeOfLife()

# RUN EXPERIMENT
while run == "r":
    gens = cellular_automata.get_integer_value("Enter the number of generations: ", 1, 5000)

    # TENIAMO TRACCIA DEL NUMERO DI GENERAZIONI
    num_generations = gens
    out, dataset = cellular_automata.run_game(gens)
    run = out


# funzione di print dei dati, la moviola
def showdata(data, gens):
    for i in range(gens):
        print(data[i])
        os.system("cls")


# ABBIAMO UNA SPECIE DI MOVIOLA! bene questo per il game of life
if dataset is not None:
    showdata(dataset, num_generations)
