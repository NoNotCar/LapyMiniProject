import sympy
import pycollo

import numpy as np
import sympy as sym

#wlog
OVAL_D = 1

m = 1.0
x,y,xv,yv,xf,yf = sympy.symbols("x y xv yv xf yf")
d2 = sym.Piecewise((x**2,OVAL_D>=abs(y)),(x**2+(y-OVAL_D)**2,y>OVAL_D),(x**2+(OVAL_D+y)**2,True))
print(sym.derive_by_array(sym.derive_by_array(d2,[x,y]),[x,y]))
f = sym.lambdify([x,y],d2,"numpy")

# state_variables = [x,y,xv,yv]
# all_variables = [x,y,xv,yv,xf,yf]
# state_equations = {
#     x: xv,
#     y: yv,
#     xv: xf/m,
#     yv: yf/m
# }
# TRACK_INNER = 1.0
# TRACK_OUTER = 2.0
# TRACK_MID = (TRACK_INNER+TRACK_OUTER)*0.5
# T=10.0
# MAX_FORCE = 10.0
# problem = pycollo.OptimalControlProblem("Mass around an oval")
# phase = problem.new_phase("HalfLap",[x,y,xv,yv],[xf,yf])
# phase.state_equations = state_equations
# phase.integrand_functions = [xf**2+yf**2]
# problem.objective_function = phase.integral_variables[0]
# phase.bounds.initial_time = 0.0
# phase.bounds.final_time = T
# phase.bounds.initial_state_constraints = {
#     x: -TRACK_MID,
#     y: 0.0,
#     xv: 0.0,
#     yv: 0.0
# }
# # phase.bounds.state_variables = {
# #     dynamics.x: [-max_disp,max_disp],
# #     dynamics.theta: [-10, 10],
# #     dynamics.v: [-10,10],
# #     dynamics.omega: [-10,10]
# # }
# phase.path_constraints = [d2-TRACK_INNER]
# phase.bounds.final_state_constraints = {
#     x: TRACK_MID,
#     y: 0.0,
#     xv: 0.0,
#     yv: 0.0
# }
# phase.bounds.control_variables = {
#     xf: [-MAX_FORCE,MAX_FORCE],
#     yf: [-MAX_FORCE,MAX_FORCE]
# }
# phase.bounds.integral_variables = [[0, 100]]
# phase.guess.time = [0, T]
# phase.guess.state_variables = [[-TRACK_MID, TRACK_MID], [0, 0], [0, 0], [0, 0]]
# phase.guess.control_variables = [[0, 0],[0, 0]]
# phase.guess.integral_variables = [0]
#
# problem.initialise()
# problem.solve(True)