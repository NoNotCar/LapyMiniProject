import numpy as np
import sympy as sym

# constants

# cart mass
m1 = 1.0

# pole mass
m2 = 0.3

# pole length
l = 0.5

# gravity
g = 9.81



#symbolic equations
#using x=q1 theta=q2 v=q.1 omega=q.2

x = sym.Symbol("x")
theta = sym.Symbol("theta")
v = sym.Symbol("v")
omega = sym.Symbol("omega")
force = sym.Symbol("force")

cart_state_equations = {
    x: v,
    theta: omega,
    v: (l * m2 * sym.sin(theta) * omega**2 + force + m2 * g * sym.cos(theta) * sym.sin(theta)) / (m1 + m2 * (1 - sym.cos(theta)**2)),
    omega: -(l * m2 * sym.cos(theta) * sym.sin(theta) * omega**2 + force * sym.cos(theta) + (m1 + m2) * g * sym.sin(theta)) / (l * m1 + l * m2 * (1 - sym.cos(theta)**2))
}

all_variables = [x,theta,v,omega,force]
state_variables = [x,theta,v,omega]

numpied = [sym.lambdify(all_variables,cart_state_equations[s],"numpy") for s in state_variables]

def x_dot(s, f):
    return np.array([numpied[i](*s,f) for i,_ in enumerate(s)])

def timestep(s, f, dt):
    return s + x_dot(s, f) * dt