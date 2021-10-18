import visualisation
import scratch
import collo

T = 2.0
n = 17
rescales = 0

print("Calculating solution from scratch...")
scratch_solution = scratch.optimise_trajectory(T=T,n=n,rescales=rescales,lru=True)
print(len(scratch_solution)//5)
print("Calculating solution using pycollo...")
pycollo_solution = collo.pycollo_optimise(T=T)
visualisation.compare_solutions(scratch_solution, T/(len(scratch_solution)//5), pycollo_solution)