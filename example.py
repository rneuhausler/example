import sparpy
import random


def test_exponential_force():
    D = 0.001
    lower_bound = [0, 0]
    upper_bound = [25, 25]
    periodic = [True, True]
    sim_time = 10000
    number_of_observations = 100
    integrate_time = sim_time / number_of_observations
    dt = 0.01
    
    #lr and la cannot be zero (in the denominator)
    C = {'cutoff':25, 'Ca':1, 'la':5, 'Cr':0, 'lr':0.1, 'type':0,'percent':37} 
    M = {'cutoff':25, 'Ca':1, 'la':5, 'Cr':0, 'lr':0.1, 'type':1, 'percent':37}
    T = {'cutoff':10, 'Ca':0, 'la':0.1, 'Cr':1, 'lr':4, 'type':2, 'percent':26}
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

    
    simulation.add_action(fixed, particles, sparpy.calculate_density2(2.5,dt))
    simulation.add_action(fixed, fixed, sparpy.calculate_density2(6,dt))


    
    
    #    simulation.add_force(particles, particles, sparpy.exponential_force2(cutoff, epsilon))


    for i in range(number_of_observations):
        for p in fixed:
            p.density = [0.0,0.0,0.0,0.0]
        simulation.integrate(integrate_time, dt)
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
