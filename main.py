import visualisation
import scratch

T = 2.0
n = 40
dt = T/n

visualisation.show_trajectory(scratch.optimise_trajectory(T=T,n=n),dt)