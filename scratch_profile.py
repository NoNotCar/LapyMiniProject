import cProfile
import pstats

T = 2.0
n = 50
rescales = 0

if input("Reprofile solution? ")=="yes":
    import scratch
    print("Profiling scratch solution")
    cProfile.run("scratch.optimise_trajectory(T=T,n=n,rescales=rescales)","stats")
p = pstats.Stats("stats")
p.sort_stats(pstats.SortKey.TIME)
p.print_stats(10)
p.sort_stats(pstats.SortKey.CUMULATIVE)
p.print_stats(30)