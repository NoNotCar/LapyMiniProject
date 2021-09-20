import numpy as np

# constants

# cart mass
m1 = 1

# pole mass
m2 = 1

# pole length
l = 1

# gravity
g = 9.81

# state vector is x=[q1 q2 q.1 q.2]
def x_dot(x, f):
    aq1 = (l*m2*np.sin(x[1])*np.square(x[3])+f+m2*g*np.cos(x[1])*np.sin(x[0]))/(m1+m2*(1-np.cos(np.square(x[1]))))
    aq2 = -(l*m2+np.cos(x[1])*np.sin(x[1])*np.square(x[3])+f*np.cos(x[1])+(m1+m2)*g*np.sin(x[1]))/(l*m1+l*m2*(1-np.cos(np.square(x[1]))))
    return np.array([x[2],x[3],aq1,aq2])

def timestep(x,f,dt):
    return x+x_dot(x,f)*dt