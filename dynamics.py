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

# state vector is x=[q1 q2 q.1 q.2]
def x_dot(s, f):
    aq1 = (l * m2 * np.sin(s[1]) * np.square(s[3]) + f + m2 * g * np.cos(s[1]) * np.sin(s[1])) / (m1 + m2 * (1 - np.square(np.cos(s[1]))))
    aq2 = -(l * m2 * np.cos(s[1]) * np.sin(s[1]) * np.square(s[3]) + f * np.cos(s[1]) + (m1 + m2) * g * np.sin(s[1])) / (l * m1 + l * m2 * (1 - np.square(np.cos(s[1]))))
    return np.array([s[2], s[3], aq1, aq2])

def timestep(s, f, dt):
    return s + x_dot(s, f) * dt

#symbolic equations for pycollo
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

