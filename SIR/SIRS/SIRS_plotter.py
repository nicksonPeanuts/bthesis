from SIRS import SIRS
import numpy as np
import sys
import matplotlib.pyplot as plt
import math

def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + " <parameters file>")
        quit()
    else:
        infile_parameters = sys.argv[1]

    # Open input file and assinging parameters.
    with open(infile_parameters, "r") as input_file:
        # Read the lines of the input data file.
        line = input_file.readline()
        items = line.split(", ")
        # Lattice size.
        lattice_size = (int(items[0]), int(items[0]))
        desired_plot = str(items[1]) # Desired plot.
        ini_cond = str(items[2])     # Initial conditions.
        p2 = float(items[3])         # P(I --> R).
        p_step = float(items[4])     # Probability steps.
        eqm_sweeps = int(items[5])   # Equilibrium sweeps.
        sweeps = int(items[6])       # No. of sweeps.

    # Heatmap plot.
    if desired_plot == 'heatmap':
        # Initialising probability domains.
        p1s = np.arange(0.0, 1.0 + p_step, p_step)
        #print(p1s.size)
        p3s = np.arange(0.0, 1.0 + p_step, p_step)
        # Initialising phase matrix.
        phase_matrix = np.zeros((p1s.size, p3s.size))
        var_matrix = np.zeros((p1s.size, p3s.size))

        # Simulation begins.
        for p1 in p1s:
            print(p1)
            # Data storage.
            psi_per_p1 = []
            var_data = []
            for p3 in p3s:
                simulation = SIRS(size=lattice_size,
                                    ini=ini_cond, p1=p1, p2=p2, p3=p3)
                psi_per_p3 = []
                # Sweep over lattice.
                for sweep in range(sweeps):
                    for j in range(simulation.size[0]*simulation.size[1]):
                        simulation.update_SIRS()
                    # Get data.
                    if sweep >= eqm_sweeps and simulation.get_infected() != 0:
                        psi_per_p3.append(simulation.get_infected())
                    # Stop when absorbing state reached.
                    elif sweep >= eqm_sweeps:
                        break
                # Data collection.
                if len(psi_per_p3) != 0:
                    psi_per_p1.append(simulation.get_avg_obs(
                        psi_per_p3) / (simulation.size[0]*simulation.size[1]))
                    var_data.append(simulation.get_infected_var(
                        psi_per_p3) / (simulation.size[0]*simulation.size[1]))
                else:
                    psi_per_p1.append(0.0)
                    var_data.append(0.0)

            # Update matrix columns.
            phase_matrix[:, int(p1*(p1s.size-1))] = psi_per_p1
            var_matrix[:, int(p1*(p1s.size-1))] = var_data

        # Plotting.
        simulation.plot_phase_diagram(phase_matrix, p_step)
        simulation.plot_variance_contour(var_matrix, p_step)

        # Writing to file.
        np.savetxt("phase_data.dat", phase_matrix, fmt='%1.5f', delimiter=' ', 
                    newline = '\n# p1 = [0.0, 0.025, ..., 1.0]' + ' p3 = [0.0, 0.025, ..., 1.0]\n',
                    header = 'Phase Diagram Raw Data'
                    )
        np.savetxt("var_data.dat", var_matrix, fmt='%1.5f', delimiter=' ',
                    newline = '\n# p1 = [0.0, 0.025, ..., 1.0]' + ' p3 = [0.0, 0.025, ..., 1.0\n',
                    header = 'Phase Diagram Variance Raw Data'
                    )

    # Variance cut plot.
    elif desired_plot == 'variance_plot':
        # Initialising probability domains.
        p1s = np.arange(0.2, 0.51, 0.01)
        p3 = 0.5
        # Data storage.
        var_array = np.zeros(p1s.size)
        error_array = np.zeros(p1s.size)
        # Simulation begins.
        for i in range(p1s.size):
            print(p1s[i])
            # Data storage.
            psis = []
            # New simulation.
            simulation = SIRS(size=lattice_size,
                              ini=ini_cond, p1=p1s[i], p2=p2, p3=p3)
            # Sweeping.
            for sweep in range(10000):
                for j in range(simulation.size[0]*simulation.size[1]):
                        simulation.update_SIRS()
                if sweep >= eqm_sweeps:
                        psis.append(simulation.get_infected())
            # Update arrays.
            var_array[i] = simulation.get_infected_var(psis) / \
                (simulation.size[0] * simulation.size[1])
            error_array[i] = simulation.bootstrap(psis, 100)

        # Plotting.
        simulation.plot_figure(p1s, var_array, error_array)

        # Writing to a file.
        with open("var_cut.dat", "w+") as f:
            f.writelines(map("{}, {}, {}\n".format, p1s, var_array, error_array))
            
    # Immunity plot.
    elif desired_plot == 'immunity':
        # Initialising probabilities.
        p1 = 0.5
        p3 = 0.5
        # Initialising x domain.
        im_fracs = np.arange(0.0, 0.525, 0.025)
        # Data storage.
        overall_psis = []
        im_errors = []
        # Looping to generate errorbars.
        for k in range(5):
            print(k)
            # Data storage.
            psi_per_k = []
            # New simulation.
            for frac in im_fracs:
                psi_per_frac = []
                simulation = SIRS(size=lattice_size,
                                  ini=ini_cond, p1=p1, p2=p2, p3=p3)
                # Creating immune sites.
                for i in range(int(simulation.size[0]*simulation.size[1]*frac)):
                    indices = (np.random.randint(0, simulation.size[0]),
                               np.random.randint(0, simulation.size[1]))
                    simulation.lattice[indices] = 2
                # Sweeping.
                for sweep in range(sweeps * 10):
                    for j in range(simulation.size[0]*simulation.size[1]):
                            simulation.update_SIRS()
                    if sweep >= eqm_sweeps:
                            # Storing infected sites per frac.
                            psi_per_frac.append(simulation.get_infected() / (simulation.size[0] * simulation.size[1]))
                # Storing averages.            
                psi_per_k.append(simulation.get_avg_obs(psi_per_frac))
            # Storing data from each simulation.
            overall_psis.append(psi_per_k)
        # Computing errors.
        for vals in np.array(overall_psis).T:
            im_errors.append(np.std(vals)/math.sqrt(len(vals)))
        # Generating y_data.
        infected_fracs = np.mean(overall_psis, axis = 0)

        # Plotting.
        plt.title('Infected Sites vs. Immune Fraction')
        plt.xlabel('Immune Fraction')
        plt.ylabel('Infected Fraction')
        plt.errorbar(im_fracs, infected_fracs, yerr = im_errors)
        plt.savefig("immunity_plot.png")
        plt.show()

        # Writing to file.
        with open("immunity.dat", "w+") as f:
            f.writelines(map("{}, {}, {}\n".format, im_fracs, infected_fracs, im_errors))

    elif desired_plot == "sir_curve":
        # we are in a SIRS model, p3 must be 0 
        p1 = 0.35
        p2 = 0.1
        p3 = 0

        # start the simulation with this
        simulation = SIRS(size=(50,50), ini = "sir", p1 = p1, p2 = p2, p3 = p3)

        S_hist = []
        I_hist = []
        R_hist = []

        # let's start the simulation, the algorithms must work this way
        for i in range(100):
            # updating the simulation CA
            for _ in range(simulation.size[0] * simulation.size[1]):
                simulation.update_SIRS()

            S = np.count_nonzero(simulation.lattice == -1)
            I = np.count_nonzero(simulation.lattice == 0)
            R = np.count_nonzero(simulation.lattice == 1)

            S_hist.append(S)
            I_hist.append(I)
            R_hist.append(R)

        t = np.arange(len(S_hist))
        plt.plot(t, np.array(S_hist), label='S(t)')
        plt.plot(t, np.array(I_hist), label='I(t)')
        plt.plot(t, np.array(R_hist), label='R(t)')
        plt.legend()
        plt.xlabel('sweep')
        plt.ylabel('people')
        plt.title('SIR lattice dynamics')
        plt.savefig('sir_curves.png')
        plt.show()



# avvia la simulazione
main()
