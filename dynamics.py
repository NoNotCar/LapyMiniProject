import numpy as np
import sympy as sym

from sympy.utilities.autowrap import ufuncify

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

all_variables = [x,theta,v,omega,force]
state_variables = [x,theta,v,omega]

cart_state_equations = {
    x: v,
    theta: omega,
    v: (l * m2 * sym.sin(theta) * omega**2 + force + m2 * g * sym.cos(theta) * sym.sin(theta)) / (m1 + m2 * (1 - sym.cos(theta)**2)),
    omega: -(l * m2 * sym.cos(theta) * sym.sin(theta) * omega**2 + force * sym.cos(theta) + (m1 + m2) * g * sym.sin(theta)) / (l * m1 + l * m2 * (1 - sym.cos(theta)**2))
}

state_array = sym.Array([cart_state_equations[s] for s in state_variables])

numpied = sym.lambdify(all_variables,state_array,"numpy",cse=True)
ufv = ufuncify(all_variables,cart_state_equations[v])
ufo = ufuncify(all_variables,cart_state_equations[omega])

def fast_x_dot(x,t,v,o,f):
    xd = np.zeros(4)
    xd[0]=v
    xd[1]=o
    xd[2]=ufv(x,t,v,o,f)
    xd[3]=ufo(x,t,v,o,f)
    return xd
def x_dot(s, f):
    return np.array(numpied(*s,f))


def timestep(s, f, dt):
    return s + x_dot(s, f) * dt