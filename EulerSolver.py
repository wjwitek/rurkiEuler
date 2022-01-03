import numpy as np
import matplotlib.pyplot as plt
import csv
import platform


def get_plots_path():
    if "Windows" in platform.system():
        return "plots\\"
    else:
        return "plots/"


"""
Class performing Euler algorithm and keeping current estimated values.
"""


class EulerSolver:
    def __init__(self, ode, initial_condition, exact_solution=None, step_size=0.1):
        self.exact_solution = exact_solution  # lambda
        self.h = step_size
        self.y0 = initial_condition
        self.ode = ode  # solved differential equation, as lambda
        self.y = []
        self.x = []

    def explicit_euler_method(self, a=0, b=1):
        """
        Calculate y(x) for each x.
        :param a: start of interval (inclusive)
        :param b: end of interval (inclusive)
        """
        # a, b - rage on which equation is solved
        self.x = np.arange(a, b + self.h, self.h)  # Numerical grid
        self.y = np.zeros(len(self.x))
        self.y[0] = self.y0

        for i in range(0, len(self.y) - 1):
            self.y[i + 1] = self.y[i] + self.h * self.ode(self.x[i], self.y[i])

    def plot(self, file_path):
        """
        Plot current x and y, compared to explicit solution.
        :param file_path: where to save plot
        """
        plt.style.use('seaborn-poster')
        plt.figure(figsize=(12, 8))
        plt.plot(self.x, self.y, 'bo--', label='Estimated')
        if self.exact_solution is not None:
            plt.plot(self.x, self.exact_solution(self.x), 'g', label='Exact')
        plt.title('Exact and estimated solutions')
        plt.xlabel('x')
        plt.ylabel('y(x)')
        plt.grid()
        plt.legend(loc='lower right')
        plt.savefig(file_path)
        plt.close()

    def step(self, a=0, b=1, step_divisor = 10):
        """
        Make step smaller, repeat calculating y(x) and redraw plot.
        :param a: start of interval (inclusive)
        :param b: end of interval (inclusive)
        """
        self.h /= step_divisor
        self.explicit_euler_method(a, b)
        self.plot(get_plots_path() + "current_plot.png")

    def save_state(self, file_path):
        """
        Save current x and y(x) to csv file.
        :param file_path: where to save file
        """
        # open the file in the write mode
        with open(file_path, 'w') as f:
            # create the csv writer
            writer = csv.writer(f, delimiter=" ")

            # add header
            header = ["x", "y"]
            if self.exact_solution is not None:
                header.append("y_true")
            writer.writerow(header)

            # add data
            for i in range(len(self.y)):
                row = [round(self.x[i], 2), round(self.y[i], 2)]
                if self.exact_solution is not None:
                    row.append(round(self.exact_solution(self.x)[i], 2))
                # write a row to the csv file
                writer.writerow(row)
