from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image

from EulerSolver import EulerSolver, get_plots_path


class ParametersScreen(GridLayout):
    plot_image: Image
    eulerSolver: EulerSolver

    def __init__(self, **kwargs):
        super(ParametersScreen, self).__init__(**kwargs)
        self.cols = 1

        self.step_label = Label()
        self.message_label = Label(color=[1.0, 0.0, 0.0, 1.0], size_hint_y=0.420)

        equation_input_box = BoxLayout(orientation='horizontal')
        equation_input_box.add_widget(
            Label(text="Enter differential equation y'(x) = "))
        self.derivative = self.create_dark_text_in_field()
        self.derivative.text = "2*y/x"
        equation_input_box.add_widget(self.derivative)
        self.add_widget(equation_input_box)

        solution_input_box = BoxLayout(orientation='horizontal')
        solution_input_box.add_widget(Label(text='Enter solution y(x) ='))
        self.solution = self.create_dark_text_in_field()
        self.solution.text = "x**2"
        solution_input_box.add_widget(self.solution)
        self.add_widget(solution_input_box)

        interval_start_input_box = BoxLayout(orientation='horizontal')
        interval_start_input_box.add_widget(Label(text='Enter the start of the interval: '))
        self.interval_start = self.create_dark_text_in_field()
        self.interval_start.text = "1"
        interval_start_input_box.add_widget(self.interval_start)
        self.add_widget(interval_start_input_box)

        interval_end_input_box = BoxLayout(orientation='horizontal')
        interval_end_input_box.add_widget(Label(text='Enter the end of the interval: '))
        self.interval_end = self.create_dark_text_in_field()
        self.interval_end.text = "2"
        interval_end_input_box.add_widget(self.interval_end)
        self.add_widget(interval_end_input_box)

        step_size_input_box = BoxLayout(orientation='horizontal')
        step_size_input_box.add_widget(Label(text='Initial step size: '))
        self.step_size = self.create_dark_text_in_field()
        self.step_size.text = "0.2"
        step_size_input_box.add_widget(self.step_size)
        self.add_widget(step_size_input_box)

        step_divisor_input_box = BoxLayout(orientation='horizontal')
        step_divisor_input_box.add_widget(Label(text='Every iteration divide step size by: '))
        self.step_divisor = self.create_dark_text_in_field()
        self.step_divisor.text = "3"
        step_divisor_input_box.add_widget(self.step_divisor)
        self.add_widget(step_divisor_input_box)

        self.add_widget(self.message_label)

        self.start_button = Button(text="go!", size_hint_y=0.5)
        self.start_button.bind(on_press=self.start)
        self.add_widget(self.start_button)

    def create_dark_text_in_field(self):
        return TextInput(multiline=False, background_color=[1.0, 1.0, 1.0, 0.3],
                         foreground_color=[1.0, 1.0, 1.0, 1.0])

    def start(self, instance):
        valid, exception = self.validate_input()
        if valid:
            self.show_plot_screen()
        else:
            self.message_label.text = "invalid input: " + str(exception)

    def validate_input(self):
        try:
            float(eval(self.interval_start.text))
            float(eval(self.interval_end.text))
            float(eval(self.step_size.text))
            float(eval(self.step_divisor.text))

            x = float(self.interval_start.text)
            eval(self.solution.text)
            y = float(eval(self.solution.text))
            eval(self.derivative.text)
        except Exception as e:
            print("invalid input", e)
            return False, e
        return True, ""

    def show_plot_screen(self):
        self.clear_widgets()
        self.cols = 1

        solution_function = lambda x: eval(self.solution.text)

        self.eulerSolver = EulerSolver(lambda x, y: eval(self.derivative.text),
                                       solution_function(eval(self.interval_start.text)),
                                       lambda list_x: list(map(solution_function, list_x)),
                                       eval(self.step_size.text))
        self.eulerSolver.explicit_euler_method(eval(self.interval_start.text), eval(self.interval_end.text))

        self.eulerSolver.plot(get_plots_path() + "current_plot.png")
        self.plot_image = Image(source=get_plots_path() + "current_plot.png")
        self.add_widget(self.plot_image)

        self.add_widget(self.get_information_box())

        buttons_box = BoxLayout(orientation="horizontal", size_hint_y=0.15)

        step_button_box = BoxLayout(orientation="horizontal")
        step_button = Button(text="Next iteration! (Divide step by " + self.step_divisor.text + ")")
        step_button.bind(on_press=self.next_step)
        step_button_box.add_widget(step_button)

        filesave_box = BoxLayout(orientation="vertical")
        get_data_to_file_button = Button(text="Get data to a file")
        get_data_to_file_button.bind(on_press=self.save_to_a_file)
        filesave_box.add_widget(get_data_to_file_button)

        filename_box = BoxLayout(orientation="horizontal")
        filename_box.add_widget(Label(text="filename:", size_hint_x=0.2137))
        self.filename_textbox = TextInput(multiline=False)
        self.filename_textbox.text = "EulerMethod"
        filename_box.add_widget(self.filename_textbox)
        filesave_box.add_widget(filename_box)

        buttons_box.add_widget(step_button_box)
        buttons_box.add_widget(filesave_box)

        self.add_widget(buttons_box)

    def save_to_a_file(self, instance):
        print("saving to a file")
        self.eulerSolver.save_state(self.filename_textbox.text + ".csv")

    def get_information_box(self):
        root_box = GridLayout(size_hint_y=0.2)
        root_box.cols = 2

        oed_box = BoxLayout(orientation="horizontal")
        oed_box.add_widget(Label(text="Equation:   " + "y'(x) = " + self.derivative.text))
        root_box.add_widget(oed_box)

        solution_box = BoxLayout(orientation="horizontal")
        solution_box.add_widget(Label(text="Solution:   " + "y(x) = " + self.solution.text))
        root_box.add_widget(solution_box)

        current_step_box = BoxLayout(orientation="horizontal")
        current_step_box.add_widget(Label(text="Current step size: "))
        self.step_label.text = str(self.eulerSolver.h)
        current_step_box.add_widget(self.step_label)
        root_box.add_widget(current_step_box)

        return root_box

    def next_step(self, instance):
        print("in next_step", instance)
        self.eulerSolver.step(eval(self.interval_start.text), eval(self.interval_end.text),
                              eval(self.step_divisor.text))
        self.plot_image.reload()
        self.step_label.text = str(self.eulerSolver.h)

    def get_derivative(self):
        return self.derivative


class MyApp(App):

    def build(self):
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
