from GOL import GOL
import numpy as np
import sys

def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + " <parameters file>")
        quit()
    else:
        infile_parameters = sys.argv[1]

    # Open input file and assinging parameters.
    with open(infile_parameters, "r") as input_file:
        # Read the lines of the input data file
        line = input_file.readline()
        items = line.split(", ")

        simulations = int(items[0])  # No. of simulations.
        ini_cond = str(items[1])     # Initial conditions.
        lattice_size = (int(items[2]), int(items[2]))  # Lattice size.

    game = GOL(size=lattice_size, ini=ini_cond)

    # Simulation for GOL steady state determination.
    if game.ini == 'random':
        eqm_times = []
        # Simulation begins.
        for i in range(simulations):
            print(i)
            live_cells = []
            game = GOL(size=lattice_size, ini=ini_cond)
            # Counter.
            sweeps = 0 
            # Whilst not in EQM.
            while game.eqm == False:
                # Evolve state.
                game.evolve_state()
                # Update sweeps.
                sweeps += 1
                # Count number of live cells in state.
                live_cells.append(game.count_live())
                # Steady state determination.
                game.check_eqm(live_cells)
                # Prevents infinite loop.
                if sweeps == 4000:
                    break
            # Data storing.
            if sweeps == 4000:
                pass
            else:
                # Minus 3 to account for check_eqm.
                eqm_times.append(len(live_cells) - 3)
                print (eqm_times[i])

        # Plotting.
        game.plot_hist(eqm_times, np.arange(0, 3000, 100))

        # Writing to file.
        with open("gol_eqm_hist.dat", "w+") as f:
            f.write("GOL Sweeps to Reach Equilibrium\n")
            for time in eqm_times:
                f.write('%lf\n' % time)

    elif game.ini == 'glider':
        # Initialising data storage.
        x_pos = []
        y_pos = []
        times = []
        plot_all = True
        meas_skips = 10
        # Simulation begins.
        for i in range(simulations):
            for j in range(meas_skips):
                game.evolve_state()
            # Find live cells of glider.
            xs = game.get_glider_pos()[0]
            ys = game.get_glider_pos()[1]
            # Check if at lattice boundary.
            x_checker, y_checker = game.boundary_checker(xs, ys)
            # Store COM pos if not at lattice boundary.
            if x_checker == False and y_checker == False:
                times.append(i)
                x_pos.append(game.get_com(xs, ys)[0] / meas_skips)
                y_pos.append(game.get_com(xs, ys)[1] / meas_skips)

        # Printing glider velocity.
        vel = game.plot_traj(times, x_pos, all=plot_all)
        if plot_all == False:
            print("The velocity of the glider is " + str(vel) + " cells / sweep")
        
        # Writing to a file.
        with open("gol_glider.dat", "w+") as f:
            f.writelines(map("{}, {}, {}\n".format, times, x_pos, y_pos))
        
main()
