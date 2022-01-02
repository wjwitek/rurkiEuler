from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image

from EulerSolver import EulerSolver, get_plots_path

from math import *


class ParametersScreen(GridLayout):
    plot_image: Image
    eulerSolver: EulerSolver

    def __init__(self, **kwargs):
        super(ParametersScreen, self).__init__(**kwargs)
        self.cols = 1

        equation_input_box = BoxLayout(orientation='horizontal')
        equation_input_box.add_widget(Label(text="Enter differential equation y'(x) = "))
        self.derivative = TextInput(multiline=False)
        self.derivative.text = "2*y/x"
        equation_input_box.add_widget(self.derivative)
        self.add_widget(equation_input_box)

        diff_equation_input_box = BoxLayout(orientation='horizontal')
        diff_equation_input_box.add_widget(Label(text="Enter differential equation y'(x) = "))
        self.initial_condition = TextInput(multiline=False)
        self.initial_condition.text = "1"
        diff_equation_input_box.add_widget(self.initial_condition)
        self.add_widget(diff_equation_input_box)

        solution_input_box = BoxLayout(orientation='horizontal')
        solution_input_box.add_widget(Label(text='Enter solution y(x) ='))
        self.solution = TextInput(multiline=False)
        self.solution.text = "x**2"
        solution_input_box.add_widget(self.solution)
        self.add_widget(solution_input_box)

        interval_start_input_box = BoxLayout(orientation='horizontal')
        interval_start_input_box.add_widget(Label(text='Enter the start of the interval: '))
        self.interval_start = TextInput(multiline=False)
        self.interval_start.text = "1"
        interval_start_input_box.add_widget(self.interval_start)
        self.add_widget(interval_start_input_box)

        interval_end_input_box = BoxLayout(orientation='horizontal')
        interval_end_input_box.add_widget(Label(text='Enter the end of the interval: '))
        self.interval_end = TextInput(multiline=False)
        self.interval_end.text = "2"
        interval_end_input_box.add_widget(self.interval_end)
        self.add_widget(interval_end_input_box)

        self.start_button = Button(text="go!", size_hint_y=0.5)
        self.start_button.bind(on_press=self.start)
        self.add_widget(self.start_button)

    def start(self, instance):
        print("yes", instance)
        self.clear_widgets()
        self.cols = 1

        self.eulerSolver = EulerSolver(lambda x, y: eval(self.derivative.text),
                                       int(self.initial_condition.text),
                                       lambda list_x: list(map(lambda x: eval(self.solution.text), list_x)))
        self.eulerSolver.explicit_euler_method(int(self.interval_start.text), int(self.interval_end.text))

        self.eulerSolver.plot(get_plots_path() + "current_plot.png")
        self.plot_image = Image(source=get_plots_path() + "current_plot.png")
        self.add_widget(self.plot_image)

        self.start_button = Button(text="step brother!", size_hint_y=0.1)
        self.start_button.bind(on_press=self.next_step)
        self.add_widget(self.start_button)

    def next_step(self, instance):
        print("in next_step", instance)
        self.eulerSolver.step(int(self.interval_start.text), int(self.interval_end.text))
        self.plot_image.reload()

    def get_derivative(self):
        return self.derivative


class MyApp(App):

    def build(self):
        ParametersScreen()

        return ParametersScreen()


if __name__ == '__main__':
    MyApp().run()

    # derivative = "2*y/x"  # input("Enter differential equation y'(x) = ")
    # initial_condition = 1  # int(input("Enter initial condition y(0) = "))
    # solution = "x**2"  # input("Enter solution y(x) = ")
    # a = 1
    # b = 2
    #
    # eulerSolver = EulerSolver(lambda x, y: eval(derivative), initial_condition,
    #                           lambda list_x: list(map(lambda x: eval(solution), list_x)))
    # eulerSolver.explicit_euler_method(a, b)
    # eulerSolver.plot("testPlot")
    # eulerSolver.step(a, b)
