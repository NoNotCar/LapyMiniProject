import pycollo
import dynamics
import sympy as sym
import numpy as np

def pycollo_optimise(T=2.0,max_force=20.0,max_disp=2.0):
    problem = pycollo.OptimalControlProblem("CartPole swing-up")
    phase = problem.new_phase("SwingUp",[dynamics.x,dynamics.theta,dynamics.v,dynamics.omega],dynamics.force)
    phase.state_equations = dynamics.cart_state_equations
    phase.integrand_functions = [dynamics.force**2]
    problem.objective_function = phase.integral_variables[0]
    phase.bounds.initial_time = 0.0
    phase.bounds.final_time = T
    phase.bounds.initial_state_constraints = {
        dynamics.x: 0.0,
        dynamics.theta: 0.0,
        dynamics.v: 0.0,
        dynamics.omega: 0.0
    }
    phase.bounds.state_variables = {
        dynamics.x: [-max_disp,max_disp],
        dynamics.theta: [-10, 10],
        dynamics.v: [-10,10],
        dynamics.omega: [-10,10]
    }
    phase.bounds.final_state_constraints = {
        dynamics.x: [-max_disp, max_disp],
        dynamics.theta: sym.pi,
        dynamics.v: 0.0,
        dynamics.omega: 0.0
    }
    phase.bounds.control_variables = {
        dynamics.force: [-max_force,max_force]
    }
    phase.guess.time = [0, T]
    phase.guess.state_variables = [[0, max_disp/2], [0, np.pi], [0, 0], [0, 0]]
    phase.guess.control_variables = [[0, 0]]
    phase.guess.integral_variables = [0]

    problem.initialise()
    problem.solve(True)
    return problem


