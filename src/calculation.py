
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
    performances = get_performance(overall_performances, steps)
    labels = ["Min RTT", "Avg RTT", "Max RTT", "Std RTT"]
    colors = ["green", "yellow", "red", "blue"]
    ax = plt.subplots(2, 2)[1]
    index = 0
    for i in range(0, 2):
        for j in range(0,2):
            ax[i, j].set_xlabel("L (bits)")
            ax[i, j].set_ylabel(labels[index] + "(ms)")
            ax[i, j].plot(x, performances[index], 'o', color=colors[index])
            index += 1
    plt.show()


# get a coeff
def coeff_a(steps, overall_performances):
    min_rtt = get_performance(overall_performances, steps)[0]
    min_s = [x/1000 for x in min_rtt] # convert from ms to s
    fit_s = np.polyfit(steps, min_s, 1)
    return fit_s


# calculate S and S_b
def calculate_throughput(steps, overall_performances, n_links):
    a = coeff_a(steps, overall_performances)
    s = float(n_links) / a[0]
    s_b = 2 / a[0]
    return s, s_b, a[1]