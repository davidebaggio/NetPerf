
import numpy as np
import matplotlib.pyplot as plt

# get performance


def get_performance(overall_performances, steps):
    min_rtt = []
    avg_rtt = []
    max_rtt = []
    stdev_rtt = []
    
    for i in range(len(steps)):
        min_rtt.append(overall_performances[i][0])
        avg_rtt.append(overall_performances[i][1])
        max_rtt.append(overall_performances[i][2])
        stdev_rtt.append(overall_performances[i][3])
    
    return min_rtt, avg_rtt, max_rtt, stdev_rtt

# plot the 4 graphs in one window


def plot_all(steps, overall_performances):
    x = steps
    y1, y2, y3, y4 = get_performance(overall_performances, steps)
    fig, ax = plt.subplots()
    ax.set_xlabel("L (bits)")
    ax.set_ylabel("RTT (ms)")
    ax.plot(x, y1, 'o', label="Min RTT")
    ax.plot(x, y2, 'o', label="Avg RTT")
    ax.plot(x, y3, 'o', label="Max RTT")
    ax.plot(x, y4, 'o', label="Std RTT")
    ax.legend()
    plt.show()

# get a coeff


def coeff_a(steps, overall_performances):
    min_rtt = get_performance(overall_performances, steps)[0]
    fit = np.polynomial.polynomial.polyfit(steps, min_rtt, 1)
    return float(fit[1])

# calculate S and S_b


def calculate_throughput(steps, overall_performances, n_links):
    a = coeff_a(steps, overall_performances)
    s = float(n_links) / a
    s_b = 2 / a
    return s, s_b