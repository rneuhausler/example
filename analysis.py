import sparpy
import random


def test_exponential_force():

    ### Setting up Environment

    lower_bound = [0, 0]
    upper_bound = [25, 25]
    periodic = [True, True]

    sim_time = 10000.0
    number_of_observations = 100
    integrate_time = sim_time / number_of_observations
    dt = 0.01

    grid_dt = 100.0
    grid_updates_per_observation = int(integrate_time / grid_dt)



    ### Initial parameters

    scale_dt = .0001
    density_scale = grid_dt/dt
    a = 0.2 * scale_dt
    d = 0.6 * scale_dt
    gamma = 0.75 * scale_dt
    r = 1.0 * scale_dt
    gp = 0.9 * scale_dt
    gu = 0.1 * scale_dt

    D = 0.001    #Diffusivity

    C = {'cutoff':25, 'Ca':1, 'la':5, 'Cr':0, 'lr':0.1, 'type':0,'percent':20}
    T = {'cutoff':25, 'Ca':0, 'la':0.1, 'Cr':1, 'lr':4, 'type':1, 'percent':40}
    M = {'cutoff':10, 'Ca':1, 'la':5, 'Cr':0, 'lr':0.1, 'type':2, 'percent':40}
    F = {'cutoff':6, 'Ca':0.05, 'la':5, 'Cr':1, 'lr':1, 'type':3, 'count': 50}
    #   lr and la cannot be zero (in the denominator)
    #percent_coral = 60
    #percent_turf = 36
    #percent_macroalgae = 4



    lower_grid  = 2.5
    upper_grid  = 22.5
    step_grid  = 5
    grid  = [lower_grid + x*step_grid for x in range(int((upper_grid-lower_grid)/step_grid)+1)]


    if C['percent'] + T['percent'] + M['percent'] != 100:
        print "percentages do not add up to 100"


    ### Creating the Grid Stochastically

    fixed = sparpy.Particles2(len(grid) ** 2)
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            fixed[count].position = [grid[i],grid[j]]
            fixed[count].velocity = [0,0]
            U = random.uniform(0,100)
            if U <= C['percent']:
                fixed[count].species = 0
            elif U > C['percent'] + T['percent']:
                fixed[count].species = 2
            else:
                fixed[count].species = 1
            count = count+1

    ### Placing the fish stochastically

    particles = sparpy.Particles2(F['count'])
    for p in particles:
        p.position = [random.uniform(lower_bound[0], upper_bound[0]),
                      random.uniform(lower_bound[1], upper_bound[1])]
        p.velocity = [0,0]
        p.species = F['type']
        p.force = [0,0]

    cutoff_exponential = 25
    epsilon = 5

    ### Defining the simulation

    simulation = sparpy.Simulation2()
    simulation.set_domain(lower_bound, upper_bound, periodic)
    simulation.add_particles(particles, D)
    simulation.add_particles(fixed, 0)
    simulation.add_force(particles, fixed, sparpy.morse_force2(C['cutoff'], C['Ca'], C['la'], C['Cr'], C['lr'], C['type']))
    simulation.add_force(particles, fixed, sparpy.morse_force2(T['cutoff'], T['Ca'], T['la'], T['Cr'], T['lr'], T['type']))
    simulation.add_force(particles, fixed, sparpy.morse_force2(M['cutoff'], M['Ca'], M['la'], M['Cr'], M['lr'], M['type']))
    simulation.add_force(particles, particles, sparpy.morse_force2(F['cutoff'], F['Ca'], F['la'], F['Cr'], F['lr'], F['type']))
    simulation.add_action(fixed, particles, sparpy.calculate_density2(2.5,dt/(F['count'] * grid_dt)))
    simulation.add_action(fixed, fixed, sparpy.calculate_density2(step_grid,dt/grid_dt))
    simulation_grid = sparpy.Simulation2()


    ### Running the Simulation

    for i in range(number_of_observations):

        for j in range(grid_updates_per_observation):

            for p in fixed: #fixed is the grid
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
                    if U < (gu + gp * p.density[F['type']]) * grid_dt:
                        p.species = T['type']

    x_av = 0
    y_av = 0
    for p in particles:
        x_av += p.position[0]
        y_av += p.position[1]
    print x_av/F['count'],y_av/F['count']

    assert len(particles) == F['count']


if __name__ == "__main__":
    test_exponential_force()
