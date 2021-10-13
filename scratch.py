import dynamics
import numpy as np
import scipy.optimize as optimise

def optimise_trajectory(n=20,T=2.0,max_force=20.0,max_disp=2.0,silent=False):
    dt = T/n
    # decision variables x = [s_0[0]...s_0[3],f_0...]
    smxf = np.square(max_force)
    smxd = np.square(max_disp)

    def s(x,t):
        return x[t*5:t*5+4]
    def f(x,t):
        return dynamics.x_dot(s(x,t), x[t * 5 + 4])
    def objective(x):
        return 0.5*(np.square(x[4])+np.square(x[-1]))+sum(np.square(f) for f in x[9:-1:5])
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
    result=optimise.minimize(objective,x0,constraints=collocs+forces+finals)
    if not silent:
        print(result)
    return result["x"]
