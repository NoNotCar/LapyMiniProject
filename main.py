import visualisation
import scratch
import collo

T = 2.0
n = 13
rescales = 2

print("Calculating solution from scratch...")
scratch_solution = scratch.optimise_trajectory(T=T,n=n,rescales=rescales)
print(len(scratch_solution)//5)
print("Calculating solution using pycollo...")
pycollo_solution = collo.pycollo_optimise(T=T)
visualisation.compare_solutions(scratch_solution, T/(len(scratch_solution)//5), pycollo_solution)