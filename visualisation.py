from matplotlib import pyplot as plt
import numpy as np
import dynamics
import pycollo

STATE_LABELS = ["Linear Displacement", "Angular Displacement","Linear Velocity", "Angular Velocity","Applied Force"]
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

def show_trajectory(x,timestep):
    states = []
    times = []
    for n,_ in enumerate(x[::5]):
        states.append(x[n*5:n*5+5])
        times.append(n*timestep)
    fig, axs = plt.subplots(5, 1, sharex="all")
    fig.set_figheight(12)
    fig.set_figwidth(8)
    for n, ax in enumerate(axs):
        ax.plot(times, [s[n] for s in states])
        ax.set_ylabel(STATE_LABELS[n])
        ax.set_xlim(0, times[-1])
    ax.set_xlabel("Time")
    plt.show()

def compare_solutions(x,timestep,problem):
    states = []
    times = []
    for n, _ in enumerate(x[::5]):
        states.append(x[n * 5:n * 5 + 5])
        times.append(n * timestep)
    time_solution = problem.solution.tau[0] + 1.0
    control_solution = problem.solution.control[0][0]
    fig, axs = plt.subplots(5, 1, sharex="all")
    fig.set_figheight(12)
    fig.set_figwidth(8)
    for n, ax in enumerate(axs):
        ax.plot(times, [s[n] for s in states])
        if n < 4:
            ax.plot(time_solution, problem.solution.state[0][n])
            ax.set_ylabel(STATE_LABELS[n])
        else:
            ax.plot(time_solution, control_solution)
            ax.set_ylabel("Applied Force")
        ax.set_ylabel(STATE_LABELS[n])
        ax.set_xlim(0, times[-1])
    axs[-1].set_xlabel("Time")
    axs[0].legend(["From Scratch", "Pycollo"])
    plt.show()