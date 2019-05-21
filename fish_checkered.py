import sparpy
import random
import csv
import numpy as np

def test_exponential_force():

    ### Setting up Environment

    lower_bound = [0, 0]
    upper_bound = [25, 25]
    periodic = [True, True]

    sim_time = 10000.0
    number_of_observations = 100
    integrate_time = sim_time / number_of_observations
    dt = 0.01

    #actual_time = 1
    grid_dt = 100.0
    grid_updates_per_observation = int(integrate_time / grid_dt)

    #parameters
    scale_dt = .0001
    density_scale = grid_dt/dt
    a = 0.2 * scale_dt
    d = 0.4 * scale_dt
    gamma = 0.75 * scale_dt
    r = 1.0 * scale_dt
    gp = 0.9 * scale_dt
    gu = 0.1 * scale_dt

    D = 0.001    #Diffusivity

    #lr and la cannot be zero (in the denominator)
    C = {'cutoff':25, 'Ca':1, 'la':5, 'Cr':0, 'lr':0.1, 'type':0,'percent':20}
    T = {'cutoff':25, 'Ca':0, 'la':0.1, 'Cr':1, 'lr':4, 'type':1, 'percent':40}
    M = {'cutoff':10, 'Ca':1, 'la':5, 'Cr':0, 'lr':0.1, 'type':2, 'percent':40}
    F = {'cutoff':6, 'Ca':0.05, 'la':5, 'Cr':1, 'lr':1, 'type':3, 'count': 20}


    #percent_coral = 60
    #percent_turf = 36
    #percent_macroalgae = 4

    lower_grid  = 2.5
    upper_grid  = 22.5
    step_grid  = 5
    grid  = [lower_grid + x*step_grid for x in range(int((upper_grid-lower_grid)/step_grid)+1)]

    if C['percent'] + T['percent'] + M['percent'] != 100:
        print "percentages do not add up to 100"

    fixed = sparpy.Particles2(len(grid) ** 2)
    count = 0
    t = 0

    for i in range(len(grid)):
        for j in range(len(grid)):
            fixed[count].position = [grid[i],grid[j]]
            fixed[count].velocity = [0,0]
            if t == 0:
                fixed[count].species = 0
                t = 1
            elif t == 1:
                fixed[count].species = 1
                t = 2
            else:
                fixed[count].species = 2
                t = 0
            count = count+1
            print("grid point 1 created")

    particles = sparpy.Particles2(F['count'])
    for p in particles:
        p.position = [random.uniform(lower_bound[0], upper_bound[0]),
                      random.uniform(lower_bound[1], upper_bound[1])]
        p.velocity = [0,0]
        p.species = F['type']
        p.force = [0,0]

    cutoff_exponential = 25
    epsilon = 5

    simulation = sparpy.Simulation2()
    simulation.set_domain(lower_bound, upper_bound, periodic)
    simulation.add_particles(particles, D)
    simulation.add_particles(fixed, 0)
    #simulation.add_force(particles, fixed, sparpy.exponential_force2(cutoff_exponential, epsilon))
    simulation.add_force(particles, fixed, sparpy.morse_force2(C['cutoff'], C['Ca'], C['la'], C['Cr'], C['lr'], C['type']))
    simulation.add_force(particles, fixed, sparpy.morse_force2(T['cutoff'], T['Ca'], T['la'], T['Cr'], T['lr'], T['type']))
    simulation.add_force(particles, fixed, sparpy.morse_force2(M['cutoff'], M['Ca'], M['la'], M['Cr'], M['lr'], M['type']))
    simulation.add_force(particles, particles, sparpy.morse_force2(F['cutoff'], F['Ca'], F['la'], F['Cr'], F['lr'], F['type']))


    simulation.add_action(fixed, particles, sparpy.calculate_density2(2.5,dt/(F['count'] * grid_dt)))
    simulation.add_action(fixed, fixed, sparpy.calculate_density2(step_grid,dt/grid_dt))

    simulation_grid = sparpy.Simulation2()

    ### Create Datatable to store each run and each node
    number_of_nodes = len(grid) ** 2
    number_of_recordings = number_of_observations * grid_updates_per_observation
    node_type = np.zeros((number_of_recordings, number_of_nodes))
    node_density = np.zeros((number_of_recordings, number_of_nodes, 4))
    row = 0
    column = 0

    path = 'coral_returned/'

    ### Running the Simulation


    for i in range(number_of_observations):

        for j in range(grid_updates_per_observation):

            for p in fixed:
                p.density = [0.0,0.0,0.0,0.0]
            simulation.integrate(grid_dt, dt)

            for p in fixed:
                U = random.uniform(0,1)

                if p.species == C['type']:
                    if U < d * grid_dt:
                        p.species = T['type']
                    elif U < d * grid_dt + a * p.density[M['type']] * grid_dt:
                        p.species = M['type']

                if p.species == T['type']:
                    if U < gamma * grid_dt * p.density[M['type']] :
                        p.species = M['type']
                    if U < (gamma * grid_dt * p.density[M['type']] +
                            r * grid_dt * p.density[C['type']]):
                        p.species = C['type']

                if p.species == M['type']:
                    if U < ((gu + gp) * p.density[F['type']]) * grid_dt:
                        p.species = T['type']

                ## Store in row for specific column
                node_type[row,column] = p.species
                node_density[row,column,] = p.density
                column = column + 1
            ## update position of row
            column = 0
            row = row + 1

    with open(path + 'type_recording' + str(n) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(node_type)
    csvFile.close()

    with open(path + 'density_recording' + str(n) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(node_density)
    csvFile.close()




        #simulation.update_grid()
          #print particles[0].force
        #simulation.update_grid()
        #print particles[0].force

    x_av = 0
    y_av = 0
    for p in particles:
        x_av += p.position[0]
        y_av += p.position[1]
    print x_av/F['count'],y_av/F['count']

    assert len(particles) == F['count']


if __name__ == "__main__":
    test_exponential_force()


"""

    for i in range(number_of_observations):
        for j in range(grid_updates_per_observation):
            for p in fixed:
                p.density = [0.0,0.0,0.0,0.0]
            simulation.integrate(grid_dt, dt)
            for p in fixed:
                U = random.uniform(0,1)
                if p.species == C['type']:
                    if U < d * grid_dt:
                        p.species = T['type']
                    elif U < d * grid_dt + a * (1 + p.density[M['type']]) * grid_dt:
                        p.species = M['type']
                if p.species == T['type']:
                    if U < gamma * grid_dt * (1 + p.density[M['type']]) :
                        p.species = M['type']
                    if U < (gamma * grid_dt * (1 + p.density[M['type']]) +
                            r * grid_dt * (1 + p.density[C['type']])):
                        p.species = C['type']
                if p.species == M['type']:
                    if U < g * (1 + p.density[T['type']]) * (1 + p.density[F['type']]):
                        p.species = T['type']
"""



"""
    sim_time = 10000
    number_of_observations = 100
    integrate_time = sim_time / number_of_observations
    dt = 0.01
"""





"""

    for i in range(number_of_observations):
        for p in fixed:
            p.density = [0.0,0.0,0.0,0.0]
        simulation.integrate(integrate_time, dt)



    for i in range(number_of_observations):
        for j in range(grid_updates_per_observation):
            for p in fixed:
                p.density = [0.0,0.0,0.0,0.0]
                simulation.integrate(grid_dt, dt)
            for p in fixed:
                if p.density[3] > 0:
                    p.species = C['type']
"""




""" Block grid species assignment




    number_coral = 1
    number_turf = 23
    number_macroalgae = 1


    fixed = sparpy.Particles2(len(grid) ** 2)
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            fixed[count].position = [grid[i],grid[j]]
            fixed[count].velocity = [0,0]
            if count < number_coral:
                fixed[count].species = 0
            elif count < number_coral + number_turf:
                fixed[count].species = 1
            else:
                fixed[count].species = 2
            count = count+1
 """
