import timeit
import scratch
import collo
import visualisation

T = 2.0
n = 50
dt = T / n

print("Timing solution from scratch...")
print(timeit.timeit("scratch.optimise_trajectory(T=2.0,n=50,silent=True)","import scratch", number=1))
print("Sanity checking - recalculating solution")
scratch_solution = scratch.optimise_trajectory(T=T,n=n,silent=True)
print("Calculating solution using pycollo...")
pycollo_solution = collo.pycollo_optimise(T=T,silent=True)
visualisation.compare_solutions(scratch_solution, dt, pycollo_solution)
