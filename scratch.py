import sympy

import dynamics
import numpy as np
import scipy.optimize as optimise
import sympy as sym

def optimise_trajectory(n=20,T=2.0,max_force=20.0,max_disp=2.0,silent=False):
    dt = T/n
    decision_variables = sympy.symbols(" ".join(f"x_{t} theta_{t} v_{t} omega_{t} force_{t}" for t in range(n)))
    decision_array = sympy.Array(decision_variables)
    smxf = np.square(max_force)
    smxd = np.square(max_disp)

    def s(x,t):
        return x[t*5:t*5+4]
    def f(x,t):
        return dynamics.x_dot(s(x,t), x[t * 5 + 4])
    objective = 0.5*(decision_variables[4]**2+decision_variables[-1]**2)+sum(f**2 for f in decision_variables[9:-1:5])
    def colloc_constraint(x,t):
        return 0.5*dt*(f(x,t)+f(x,t+1))-s(x,t+1)+s(x,t)
    def force_constraint(x,t):
        return smxf-np.square(x[t*5+4])
    def final_disp_constraint(x):
        return smxd-np.square(x[-5])
    def final_angle_constraint(x):
        return np.pi-x[-4]
    def final_linvel_constraint(x):
        return x[-3]
    def final_angvel_constraint(x):
        return x[-2]

    jacobian = sym.derive_by_array(objective,decision_array)
    x0 = np.linspace(np.array([0,0,0,0,0]),np.array([max_disp,np.pi,0,0,0]),n)
    x0 = x0.flatten()
    collocs = [{"type":"eq","fun":colloc_constraint,"args":[t]} for t in range(n-1)]
    forces = [{"type":"ineq","fun":force_constraint,"args":[t]} for t in range(n)]
    finals = [
        {"type": "ineq", "fun": final_disp_constraint},
        {"type": "eq", "fun": final_angle_constraint},
        {"type": "eq", "fun": final_linvel_constraint},
        {"type": "eq", "fun": final_angvel_constraint},
        {"type": "eq", "fun": lambda x: x[0:4]}
    ]
    result=optimise.minimize(
        sym.lambdify([decision_variables],objective,"numpy"),
        x0,
        jac=sym.lambdify([decision_variables],jacobian,"numpy"),
        constraints=collocs+forces+finals)
    if not silent:
        print(result)
    return result["x"]
