import time
import os
import random
import sys
import numpy as np


class GameOfLife:

    """

    CLASSE CHE IMPLEMENTA IL GAME OF LIFE, PER ORA FUNZIONANTE

    TODO: IMPLEMENTARE LA SCELTA DEGLI INTORNI COSI DA POTER FARE I DATASET E TRAINARE LA RETE NEURALE SULLA MOVIOLA

    """

    def __init__(self):
        self.rows = None
        self.cols = None
        self.current_generation = None
        self.next_generation = None

    def clear_console(self):
        """
        Clears the console using a system command based on the user's operating system.
        """

        if sys.platform.startswith('win'):
            os.system("cls")
        elif sys.platform.startswith('linux'):
            os.system("clear")
        elif sys.platform.startswith('darwin'):
            os.system("clear")
        else:
            print("Unable to clear terminal. Your operating system is not supported.\n\r")

    def resize_console(self, rows, cols):
        """
        Re-sizes the console to the size of rows x columns

        :param rows: Int - The number of rows for the console to re-size to
        :param cols: Int - The number of columns for the console to re-size to
        """

        if cols < 32:
            cols = 32

        if sys.platform.startswith('win'):
            command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
            os.system(command)
        elif sys.platform.startswith('linux'):
            command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
            sys.stdout.write(command)
        elif sys.platform.startswith('darwin'):
            command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
            sys.stdout.write(command)
        else:
            print("Unable to resize terminal. Your operating system is not supported.\n\r")

    def create_initial_grid(self, rows, cols):
        """
        Creates a random list of lists that contains 1s and 0s to represent the cells in Conway's Game of Life.

        :param rows: Int - The number of rows that the Game of Life grid will have
        :param cols: Int - The number of columns that the Game of Life grid will have
        :return: Int[][] - A list of lists containing 1s for live cells and 0s for dead cells
        """

        grid = []
        for row in range(rows):
            grid_rows = []
            for col in range(cols):
                # Generate a random number and based on that decide whether to add a live or dead cell to the grid
                # la generazione in questo caso prevede un maggior numero di cellule morte che vive, ci sta per ora
                if random.randint(0, 7) == 0:
                    grid_rows += [1]
                else:
                    grid_rows += [0]
            grid += [grid_rows]
        return grid

    def print_grid(self, rows, cols, grid, generation):
        """
        Prints to console the Game of Life grid

        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
        :param generation: Int - The current generation of the Game of Life grid
        """

        self.clear_console()

        # A single output string is used to help reduce the flickering caused by printing multiple lines
        output_str = ""

        # Compile the output string together and then print it to console
        output_str += "Generation {0} - To exit the program press <Ctrl-C>\n\r".format(generation)
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 0:
                    output_str += ". "
                else:
                    output_str += "@ "
            output_str += "\n\r"
        print(output_str, end=" ")

    def create_next_grid(self, rows, cols, grid, next_grid):
        """
        Analyzes the current generation of the Game of Life grid and determines what cells live and die in the next
        generation of the Game of Life grid.

        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
        :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
        grid
        """

        for row in range(rows):
            for col in range(cols):
                # Get the number of live cells adjacent to the cell at grid[row][col]
                live_neighbors = self.get_live_neighbors(row, col, rows, cols, grid)

                # If the number of surrounding live cells is < 2 or > 3 then we make the cell at grid[row][col] a dead cell
                if live_neighbors < 2 or live_neighbors > 3:
                    next_grid[row][col] = 0
                # If the number of surrounding live cells is 3 and the cell at grid[row][col] was previously dead then make
                # the cell into a live cell
                elif live_neighbors == 3 and grid[row][col] == 0:
                    next_grid[row][col] = 1
                # If the number of surrounding live cells is 3 and the cell at grid[row][col] is alive keep it alive
                else:
                    next_grid[row][col] = grid[row][col]

    def get_live_neighbors(self, row, col, rows, cols, grid):
        """
        Counts the number of live cells surrounding a center cell at grid[row][cell].

        :param row: Int - The row of the center cell
        :param col: Int - The column of the center cell
        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
        :return: Int - The number of live cells surrounding the cell at grid[row][cell]
        """

        life_sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Make sure to count the center cell located at grid[row][col]
                if not (i == 0 and j == 0):
                    # Using the modulo operator (%) the grid wraps around
                    life_sum += grid[((row + i) % rows)][((col + j) % cols)]
        return life_sum

    def grid_changing(self, rows, cols, grid, next_grid):
        """
        Checks to see if the current generation Game of Life grid is the same as the next generation Game of Life grid.

        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
        :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
        grid
        :return: Boolean - Whether the current generation grid is the same as the next generation grid
        """

        for row in range(rows):
            for col in range(cols):
                # If the cell at grid[row][col] is not equal to next_grid[row][col]
                if not grid[row][col] == next_grid[row][col]:
                    return True
        return False

    def get_integer_value(self, prompt, low, high):
        """
        Asks the user for integer input and between given bounds low and high.

        :param prompt: String - The string to prompt the user for input with
        :param low: Int - The low bound that the user must stay within
        :param high: Int - The high bound that the user must stay within
        :return: The valid input value that the user entered
        """

        while True:
            try:
                value = int(input(prompt))
            except ValueError:
                print("Input was not a valid integer value.")
                continue
            if value < low or value > high:
                print("Input was not inside the bounds (value <= {0} or value >= {1}).".format(low, high))
            else:
                break
        return value

    def run_game(self, generations):
        """
        Asks the user for input to setup the Game of Life to run for a given number of generations.

        """

        self.clear_console()

        # Get the number of rows and columns for the Game of Life grid
        self.rows = self.get_integer_value("Enter the number of rows (10-60): ", 10, 60)
        self.clear_console()
        self.cols = self.get_integer_value("Enter the number of cols (10-118): ", 10, 118)

        # Get the number of generations that the Game of Life should run for
        self.resize_console(self.rows, self.cols)

        # Create the initial random Game of Life grids
        self.current_generation = self.create_initial_grid(self.rows, self.cols)
        self.next_generation = self.create_initial_grid(self.rows, self.cols)

        # definiamo un numpy array per questo lavoro
        data = np.zeros((int(generations), self.rows, self.cols), dtype=np.uint8)

        # Run Game of Life sequence
        for gen in range(1, int(generations) + 1):
            if not self.grid_changing(self.rows, self.cols, self.current_generation, self.next_generation):
                break
            self.print_grid(self.rows, self.cols, self.current_generation, gen)

            # salviamo la current generation, la generazione corrente per ottenere poi una cronologia dell'evoluzione ad ogni step
            # DATA MANTAINING
            data[gen - 1] = self.current_generation

            self.create_next_grid(self.rows, self.cols, self.current_generation, self.next_generation)
            time.sleep(1 / 5.0)
            self.current_generation, self.next_generation = self.next_generation, self.current_generation

        self.print_grid(self.rows, self.cols, self.current_generation, gen)

        return input("<Enter> to exit or r to run again: "), data



if __name__ == "__main__":
    game = GameOfLife()

    while True:
        user = input("Insert generations: ")
        check, data = game.run_game(user)
        if check != "r":
            break


