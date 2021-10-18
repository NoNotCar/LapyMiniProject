import timeit
from matplotlib import pyplot as plt

T = 2.0
n = 45

options = [
    ("normal",{}),
    ("ufuncs", {"fast":True}),
    ("2 rescales",{"rescales":2}),
    ("no jacobian",{"no_jac":True}),
    ("lru cache",{"lru":True})

]

results = []
for name,o in options:
    print(f"Now timing: {name}...")
    results.append(timeit.timeit(f"scratch.optimise_trajectory(n=n,T=T,silent=True,**{str(o)})","import scratch",number=1,globals=globals()))

xs = range(len(options))
plt.bar(xs,results)
plt.xticks(xs,[name for name,_ in options])
plt.ylabel("Time (s)")
plt.xlabel("Optimisation")
plt.title(f"Timings for n={n}")
plt.show()
