from scipy import optimize as optimise

import dynamics
import numpy as np
import sympy as sym
from itertools import count
from functools import lru_cache


def s(x, t):
    return x[t * 5:t * 5 + 4]

def sf(x,t):
    return x[t*5:t*5+5]

def f(x,t):
    return dynamics.x_dot(s(x, t), x[t * 5 + 4])

def lruf(x,t):
    return _lruf(*sf(x,t))
@lru_cache
def _lruf(x,theta,v,omega,f):
    return dynamics.fast_x_dot(x,theta,v,omega,f)

def ff(x, t):
    return dynamics.fast_x_dot(*sf(x, t))

def rescale(x):
    return np.array([0.5*(sf(x,t//2)+sf(x,t//2+1)) if t%2 else sf(x,t//2) for t in range(len(x)//5*2-1)])

def optimise_trajectory(n=20,T=2.0,max_force=20.0,max_disp=2.0,silent=False,rescales=0,guess=None,**kwargs):
    if guess is not None:
        n=len(guess)
    elif rescales:
        for i in count():
            final = i
            for _ in range(rescales):
                final*=2
                final-=1
            if final>=n:
                if not silent:
                    print(f"starting with {i} points")
                n=i
                break
    dt = T/n
    decision_variables = sym.symbols(" ".join(f"x_{t} theta_{t} v_{t} omega_{t} force_{t}" for t in range(n)))
    decision_array = sym.Array(decision_variables)
    smxf = np.square(max_force)
    smxd = np.square(max_disp)
    cf = ff if kwargs.get("fast") else lruf if kwargs.get("lru") else f

    objective = 0.5*(decision_variables[4]**2+decision_variables[-1]**2)+sum(force**2 for force in decision_variables[9:-1:5])
    def colloc_constraint(x,t):
        return 0.5*dt*(cf(x,t)+cf(x,t+1))-s(x,t+1)+s(x,t)
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

    if kwargs.get("no_jac"):
        jacobian = None
    else:
        jacobian = sym.lambdify([decision_variables],sym.derive_by_array(objective,decision_array),"numpy")
    x0 = guess if guess is not None else np.linspace(np.array([0,0,0,0,0]),np.array([max_disp,np.pi,0,0,0]),n)
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
        jac=jacobian,
        constraints=collocs+forces+finals)
    if not silent:
        print(result)
    if rescales>0:
        return optimise_trajectory(T=T,max_force=max_force,max_disp=max_disp,silent=silent,rescales=rescales-1,guess=rescale(result["x"]))
    return result["x"]
