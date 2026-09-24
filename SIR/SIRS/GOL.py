import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GOL(object):
    def __init__(self, size, ini):
        """
            Game of life class object

            Attributes:
            size = size (tuple), dimensions of Game of Life.
            initial_state = ini (str), initial state of lattice
        """
        self.size = size
        self.ini = ini
        self.eqm = False
        self.build_lattice()


    def build_lattice(self):
        """
            Creates an ndarray of lattice sites, each site is
            occupied by either an alive or dead cell.
        """
        # Random config.
        if self.ini == "random":
            self.lattice = np.random.choice(a=[0, 1], size=self.size)
        # Oscillator config.
        if self.ini == "oscillator":
            self.lattice = np.zeros(self.size)
            self.lattice[25:28, 25] = self.create_oscillator()
        # Glider config.
        if self.ini == "glider":
            self.lattice = np.zeros(self.size)
            self.lattice[0:3, 0:3] = self.create_glider()
        # Beehive config.
        if self.ini == "beehive":
            self.lattice = np.zeros(self.size)
            self.lattice[25:29, 24:27] = self.create_beehive()
        # Square config.
        if self.ini == "square":
            self.lattice = np.zeros(self.size)
            self.lattice[25:27, 25] = self.create_square()

    def pbc(self, indices):
        """
            Applies periodic boundary conditions (pbc) to a
            2D lattice.
        """
        return(indices[0] % self.size[0], indices[1] % self.size[1])

    def create_glider(self):
        """
            Creates an array in the shape
            of a GOL glider.
        """
        glider = np.zeros((3,3))
        glider[2:] = 1
        glider[1, 2] = 1
        glider[0, 1] = 1
        return glider

    def create_oscillator(self):
        """
            Creates an array in the shape
            of a GOL blinker.
        """
        oscillator = np.ones((1,3))
        return oscillator

    def create_beehive(self):
        """
            Creates an array in the shape
            of a GOL beehive.
        """
        beehive = np.zeros((4,3))
        beehive[0, 1] = 1
        beehive[3, 1] = 1
        beehive[2, 0] = 1
        beehive[1, 0] = 1
        beehive[2, 2] = 1
        beehive[1, 2] = 1
        return beehive

    def create_square(self):
        """
            Creates an array in the shape
            of a GOL square.
        """
        square = np.ones((2, 2))
        return square
    
    def count_nn(self, indices):
        """
            Count the value of 8 nearest neighbours 
            in the Game of Life.
        """
        i, j = indices
        nearest_neighbours = 0

        n_n = self.lattice[(i - 1) % self.size[1], j]
        n_ne = self.lattice[(i - 1) %
                            self.size[1], (j + 1) % self.size[0]]
        n_e = self.lattice[i, (j + 1) % self.size[0]]
        n_se = self.lattice[(i + 1) % self.size[1], (j + 1) % self.size[0]]
        n_s = self.lattice[(i + 1) % self.size[1], j]
        n_sw = self.lattice[(i + 1) % self.size[1], (j - 1) % self.size[0]]
        n_w = self.lattice[i, (j - 1) % self.size[0]]
        n_nw = self.lattice[(i - 1) % self.size[1], (j - 1) % self.size[0]]

        if n_n == 1:
            nearest_neighbours += 1
        if n_ne == 1:
            nearest_neighbours += 1
        if n_e == 1:
            nearest_neighbours += 1
        if n_se == 1:
            nearest_neighbours += 1
        if n_s == 1:
            nearest_neighbours += 1
        if n_sw == 1:
            nearest_neighbours += 1
        if n_w == 1:
            nearest_neighbours += 1
        if n_nw == 1:
            nearest_neighbours += 1
        
        return nearest_neighbours

    def evolve_state(self):
        """
            Parallel updating scheme for the GOL.
        """
        new_state = np.zeros(self.size)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                indices = [i, j]
                if self.lattice[i, j] == 1:
                    if self.count_nn(indices) < 2:
                        new_state[i, j] = 0
                    elif self.count_nn(indices) > 3:
                        new_state[i, j] = 0
                    else:
                        new_state[i, j] = 1

                elif self.lattice[i, j] == 0:
                    if self.count_nn(indices) == 3:
                        new_state[i, j] = 1
                    else:
                        new_state[i, j] = 0

        self.lattice = new_state

    def count_live(self):
        """
            Returns the total number of live cells
            on the lattice.
        """
        return np.sum(self.lattice)

    def check_eqm(self, live_cells):
        """
            Checks if we are in the steady state
            for the GOL.
        """
        if len(live_cells) > 3:
            if live_cells[-1] == live_cells[-2] and live_cells[-2] == live_cells[-3]:
                self.eqm = True

    def boundary_checker(self, x_indices, y_indices):
        """
            Checks if glider position is near the edge
            of the lattice.
        """
        edge_cross_x = False
        edge_cross_y = False
        x_lower = False
        x_upper = False
        y_lower = False
        y_upper = False

        for i in range(x_indices.size):
            if x_indices[i] < 3:
                x_lower = True
            elif x_indices[i] > self.size[0] - 3:
                x_upper = True

        for j in range(y_indices.size):
            if y_indices[j] < 3:
                y_lower = True
            elif y_indices[i] > self.size[1] - 3:
                y_upper = True

        if x_lower and x_upper:
            edge_cross_x = True
        if y_lower and y_upper:
            edge_cross_y = True

        return edge_cross_x, edge_cross_y

    def get_glider_pos(self):
        """
            Returns a tuple of arrays of
            active glider cells.
        """
        x_indices = np.where(self.lattice == 1)[0]
        y_indices = np.where(self.lattice == 1)[1]
        return (x_indices, y_indices)

    def get_com(self, x_indices, y_indices):
        """
            Determines the centre of mass of live cells
            based on a 2D lattice of 1s and 0s.
        """
        com_x = 1 / self.count_live() * np.sum(x_indices)
        com_y = 1 / self.count_live() * np.sum(y_indices)

        return (com_x, com_y)

    def plot_hist(self, data, num_bins):
        """
            Histogram plotter for
            steady state times.
        """
        plt.title("Histogram of GOL EQM Times")
        plt.xlabel("Time (Sweeps)")
        plt.ylabel("Frequency")
        plt.hist(data, num_bins, facecolor='green')
        plt.savefig('gol_eqm_hist.png')
        plt.show()

    def plot_traj(self, x_data, y_data, all):
        """
            Scatter plotter for glider
            trajectory.
        """
        if all == False:
            plt.grid()
            plt.title("GOL Glider trajectory")
            plt.ylabel("x(t)")
            plt.xlabel("Time (Sweeps)")
            p = np.polyfit(x_data[:18], y_data[:18], 1)
            y_fit = np.array(x_data[:18])*p[0] + p[1]
            plt.plot(x_data[:18], y_fit, label ="x(t) = " + str(p[0]) +"t + " + str(p[1]))
            plt.legend(loc = 'upper left')
            plt.scatter(x_data[:18], y_data[:18])
            plt.savefig('single_glider_vel.png')
            plt.show()
            return(p[0])
        else:
            plt.grid()
            plt.title("GOL Glider trajectory")
            plt.ylabel("x(t)")
            plt.xlabel("Time (Sweeps)")
            plt.scatter(x_data, y_data)
            plt.savefig('all_glider_vel.png')
            plt.show()

    def animate(self, *args):
        """
            Creates, saves and returns image of the current state of
            lattice for the FuncAnimation class.
        """
        for i in range(self.it_per_sweep):
            self.evolve_state()
        self.image.set_array(self.lattice)
        return self.image,

    def run_animation(self, sweeps, it_per_sweep):
        """
            Used in partnership with the tester file
            to run the simulation.
        """
        self.it_per_sweep = it_per_sweep
        self.figure = plt.figure()
        self.image = plt.imshow(self.lattice, cmap='jet', animated=True)
        self.animation = animation.FuncAnimation(
            self.figure, self.animate, repeat=False, frames=sweeps, interval=25, blit=True)
        plt.show()
