import timeit
import scratch
import collo
import visualisation

T = 2.0
n = 13
rescales = 2

print("Timing solution from scratch...")
print(timeit.timeit("scratch.optimise_trajectory(T=2.0,n=13,rescales=2,silent=True)","import scratch", number=1))
print("Sanity checking - recalculating solution")
scratch_solution = scratch.optimise_trajectory(T=T,n=n,rescales=rescales,silent=True)
print("Calculating solution using pycollo...")
pycollo_solution = collo.pycollo_optimise(T=T,silent=True)
visualisation.compare_solutions(scratch_solution, T/(len(scratch_solution)//5), pycollo_solution)
