from matplotlib import pyplot as plt
import numpy as np
import dynamics

STATE_LABELS = ["Linear Displacement", "Angular Displacement","Linear Velocity", "Angular Velocity"]
def rollout(fs,timestep,initial_state=np.zeros(4)):
    states = [initial_state]
    times = [0]
    for f in fs:
        states.append(dynamics.timestep(states[-1],f,timestep))
        times.append(times[-1]+timestep)
    fig, axs = plt.subplots(5, 1, sharex="all")
    fig.set_figheight(12)
    fig.set_figwidth(8)
    for n, ax in enumerate(axs):
        if n < 4:
            ax.plot(times, [s[n] for s in states])
            ax.set_ylabel(STATE_LABELS[n])
        else:
            ax.plot(times[:-1], fs)
            ax.set_ylabel("Applied Force")
        ax.set_xlim(0, times[-1])
    ax.set_xlabel("Time")
    plt.show()