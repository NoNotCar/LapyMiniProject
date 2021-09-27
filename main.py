import visualisation
import scratch
import collo

T = 2.0
n = 50
dt = T/n

print("Calculating solution from scratch...")
scratch_solution = scratch.optimise_trajectory(T=T,n=n)
print("Calculating solution using pycollo...")
pycollo_solution = collo.pycollo_optimise(T=T)
visualisation.compare_solutions(scratch_solution, dt, pycollo_solution)