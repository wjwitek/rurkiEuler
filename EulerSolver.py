import numpy as np
import matplotlib.pyplot as plt
import csv


class EulerSolver:
    def __init__(self, ode, initial_condition, exact_solution=None, step_size=0.1):
        self.exact_solution = exact_solution  # lambda
        self.h = step_size
        self.y0 = initial_condition
        self.ode = ode  # solved differential equation, as lambda
        self.y = None
        self.x = None

    def explicit_euler_method(self, a, b):
        # a, b - rage on which equation is solved
        self.x = np.arange(a, b + self.h, self.h)  # Numerical grid
        self.y = np.zeros(len(self.x))
        self.y[0] = self.y0

        for i in range(0, len(self.y) - 1):
            self.y[i + 1] = self.y[i] + self.h * self.ode(self.x[i], self.y[i])

    def plot(self, file_path):
        plt.style.use('seaborn-poster')
        plt.figure(figsize=(12, 8))
        plt.plot(self.y, self.x, 'bo--', label='Przybliżone')
        plt.plot(self.x, -np.exp(-self.x), 'g', label='Dokładne')
        plt.title('Dokładne i przybliżone rozwiązania')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plt.legend(loc='lower right')
        plt.savefig(file_path)
        plt.close()

    def step(self, a, b, file_path):
        self.h /= 10
        self.explicit_euler_method(a, b)
        self.plot(file_path)

    def save_state(self, file_path):
        # open the file in the write mode
        with open(file_path, 'w') as f:
            # create the csv writer
            writer = csv.writer(f, delimiter=" ")

            # add header
            header = ["x", "y"]
            writer.writerow(header)

            # add data
            for i in range(len(self.y)):
                row = [self.x[i], self.y[i]]
                # write a row to the csv file
                writer.writerow(row)
