import sparpy
import random


def test_exponential_force():
    N = 100
    D = 0.00001
    lower_bound = [0, 0]
    upper_bound = [1, 1]
    periodic = [True, True]
    sim_time = 10.0
    number_of_observations = 100
    integrate_time = sim_time / number_of_observations
    dt = 0.001
    epsilon = 0.000001
    cutoff = 1.0

    particles = sparpy.Particles2(N)
    fixed = sparpy.Particles2(1)
    fixed[0].position = [0.1,0.1]
    fixed[0].species = 0
    fixed[0].velocity = [0,0]
    for p in particles:
        p.position = [random.uniform(lower_bound[0], upper_bound[0]),
                      random.uniform(lower_bound[1], upper_bound[1])]


    simulation = sparpy.Simulation2()
    simulation.set_domain(lower_bound, upper_bound, periodic)
    simulation.add_particles(particles, D)
    simulation.add_particles(fixed, D/100.0)
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
