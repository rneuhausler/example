import sparpy
import random


def test_exponential_force():
    N = 20
    D = 0.1
    lower_bound = [0, 0]
    upper_bound = [25, 25]
    periodic = [False, False]
    sim_time = 100.0
    number_of_observations = 100
    integrate_time = sim_time / number_of_observations
    dt = 0.01
    epsilon = 10000
    cutoff = 20
    
    lower_grid  = 2.5
    upper_grid  = 22.5
    step_grid  = 5
    grid  = [lower_grid + x*step_grid for x in range(int((upper_grid-lower_grid)/step_grid)+1)]

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
    
    particles = sparpy.Particles2(N)
    
    for p in particles:
        p.position = [random.uniform(lower_bound[0], upper_bound[0]),
                      random.uniform(lower_bound[1], upper_bound[1])]
        p.velocity = [0,0]
        p.species = 0
        p.force = [0,0]


    simulation = sparpy.Simulation2()
    simulation.set_domain(lower_bound, upper_bound, periodic)
    simulation.add_particles(particles, D)
    simulation.add_particles(fixed, 0)
    simulation.add_force(particles, fixed, sparpy.exponential_force2(cutoff, epsilon))

    for i in range(number_of_observations):
        simulation.integrate(integrate_time, dt)

    x_av = 0
    y_av = 0
    for p in particles:
        x_av += p.position[0]
        y_av += p.position[1]
    print x_av/N,y_av/N

    assert len(particles) == N


if __name__ == "__main__":
    test_exponential_force()
