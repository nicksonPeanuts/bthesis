import sys
from xml.dom import ValidationErr

import pygame
import numpy as np
import colorsys

clock = pygame.time.Clock()

rule_number = 82
cell_size = 10
grid_width = 121
generations  = 75
gen_nr = 0
#acolors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

try:
    rule_number = int(input("Enter rule number: "))
    if not 0 <= rule_number <= 255:
        raise ValueError("Rule number must be between 0 and 255")
except ValueError as err:
    print(f"Invalid rule number as {err}")
    exit(1)

pygame.init()
pygame.display.set_caption(f"Wolfram Cellular Automaton - Rule {rule_number}")
screen = pygame.display.set_mode((grid_width * cell_size, generations * cell_size))

generation = np.zeros(grid_width, dtype=int)
generation[grid_width // 2] = 1

def get_color(gen_nr):
    hue = (gen_nr* 0.03) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return int(r*255), int(g*255), int(b*255)

def new_generation(generation, rule_number):
    nextgen = np.zeros_like(generation)
    for i in range(1, len(generation)-1):
        ruleset = (generation[i-1], generation[i], generation[i+1])
        if ruleset == (1,1,1):
            nextgen[i] = rule_number[0]
        elif ruleset == (1,1,0):
            nextgen[i] = rule_number[1]
        elif ruleset == (1,0,1):
            nextgen[i] = rule_number[2]
        elif ruleset == (1,0,0):
            nextgen[i] = rule_number[3]
        elif ruleset == (0,1,1):
            nextgen[i] = rule_number[4]
        elif ruleset == (0,1,0):
            nextgen[i] = rule_number[5]
        elif ruleset == (0,0,1):
            nextgen[i] = rule_number[6]
        elif ruleset == (0,0,0):
            nextgen[i] = rule_number[7]
    return nextgen



def display(gen_nr, generation, cell_size):
    y = 1
    for x, cell in enumerate(generation):
        color = get_color(gen_nr) if cell == 1 else BLACK
        pygame.draw.rect(screen, color, (x*cell_size, gen_nr * cell_size, cell_size, cell_size))
        if cell == 1:
            pygame.display.flip()
            pygame.time.delay(1000 // (1+gen_nr*y))
            pygame.draw.rect(screen, WHITE, (x*cell_size, gen_nr * cell_size, cell_size, cell_size))
            y += 1
        #pygame.display.flip()

def binary_of(number, bits=8):
    binary_string = f"{number:0{bits}b}"
    return [int(bit) for bit in binary_string]


while True:
    display(gen_nr, generation, cell_size)
    gen_nr += 1
    pygame.display.update()
    generation = new_generation(generation, binary_of(rule_number))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

