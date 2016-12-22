#!/usr/bin/python

from collections import OrderedDict
import matplotlib.pyplot as plt
import sys
import numpy as np


def parse_csv(csv_file):
    """
    Parses csv file with similar format to the one generated by Tracer
    Example:
    time; mean; median; hpd lower 95; hpd upper 95
    """

    csv_data = OrderedDict()

    csv_fh = open(csv_file)

    next(csv_fh)

    for line in csv_fh:

        fields = line.split(",")

        fields = [float(x) for x in fields]

        # Get time as key and median and HPD bounds as value list
        csv_data[float(fields[0])] = fields[2:]

    return csv_data


def skyline_plot(csv_data, output_file):
    """
    Creates a skyline style plot from data on a csv_file. This csv file should
    be compliant with the one generated by Tracer and is parsed by parse_csv
    function.
    """

    fig, ax = plt.subplots()

    #x_data = list(csv_data.keys())
    x_data = np.arange(len(csv_data))

    median_data = [x[0] for x in csv_data.values()]
    lower_hpd = [x[1] for x in csv_data.values()]
    higher_hpd = [x[2] for x in csv_data.values()]

    plt.xticks(x_data, ["%.2E" % x for x in csv_data.keys()], rotation=45,
               ha="right")
    ax.plot(x_data, median_data, "--", color="black")
    #ax.fill_between(x_data, higher_hpd, lower_hpd, facecolor="blue", alpha=0.5)
    ax.plot(x_data, lower_hpd, color="blue")
    ax.plot(x_data, higher_hpd, color="blue")
    ax.fill_between(x_data, higher_hpd, lower_hpd, facecolor="blue", alpha=0.3)

    plt.xlabel("Time")
    plt.ylabel("Ne")

    plt.tight_layout()
    plt.savefig("%s.png" % (output_file))


def main():

    # Get arguments
    args = sys.argv

    csv_file = args[1]
    output_file = args[2]

    csv_data = parse_csv(csv_file)
    skyline_plot(csv_data, output_file)

main()