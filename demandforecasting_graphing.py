from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

class CSVViewerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        self.file_chooser = FileChooserListView()
        self.layout.add_widget(self.file_chooser)

        self.print_button = Button(text='Print CSV', size_hint=(None, None))
        self.print_button.bind(on_press=self.print_csv)
        self.layout.add_widget(self.print_button)

        self.tabs = TabbedPanel(do_default_tab=False, tab_width=200)
        self.layout.add_widget(self.tabs)

        self.column_tab = TabbedPanelItem(text='Select Columns')
        self.column_tab_content = BoxLayout(orientation='vertical', spacing=10)

        self.column_label_1 = Label(text='Enter Column 1 Name:')
        self.column_tab_content.add_widget(self.column_label_1)

        self.column_input_1 = TextInput(hint_text='Column 1', size_hint_y=None, height=40)
        self.column_tab_content.add_widget(self.column_input_1)

        self.column_label_2 = Label(text='Enter Column 2 Name:')
        self.column_tab_content.add_widget(self.column_label_2)

        self.column_input_2 = TextInput(hint_text='Column 2', size_hint_y=None, height=40)
        self.column_tab_content.add_widget(self.column_input_2)

        self.tabs.add_widget(self.column_tab)
        self.column_tab.content = self.column_tab_content

        self.graph_tab = TabbedPanelItem(text='Select Graph Type')
        self.graph_tab_content = BoxLayout(orientation='vertical', spacing=10)

        self.spinner = Spinner(text='Select Plot Type', values=['line', 'bar', 'pie', 'histogram'])
        self.graph_tab_content.add_widget(self.spinner)

        self.tabs.add_widget(self.graph_tab)
        self.graph_tab.content = self.graph_tab_content

        self.display_button = Button(text='Display Graph', size_hint=(None, None))
        self.display_button.bind(on_press=self.display_graph)
        self.layout.add_widget(self.display_button)

        self.csv_label = Label(text='', size_hint=(1, None))
        self.layout.add_widget(self.csv_label)

        return self.layout

    def animate(self, i, plot_type):
        plt.cla()

        plotting_functions = {
            'line': self.plot_line,
            'bar': self.plot_bar,
            'pie': self.plot_pie,
            'histogram': self.plot_histogram
        }

        plotting_functions[plot_type](i)

    def plot_line(self, i):
        plt.plot(self.x_data[:i], self.y_data[:i], marker='o')
        plt.xlabel(self.x_column)
        plt.ylabel(self.y_column)
        plt.title('Animated Line Plot')

    def plot_bar(self, i):
        plt.bar(self.x_data[:i], self.y_data[:i])
        plt.xlabel(self.x_column)
        plt.ylabel(self.y_column)
        plt.title('Animated Bar Plot')

    def plot_pie(self, i):
        plt.pie(self.y_data[:i], labels=self.x_data[:i], autopct='%1.1f%%')
        plt.title('Animated Pie Chart')

    def plot_histogram(self, i):
        plt.hist(self.y_data[:i], bins=20)
        plt.xlabel(self.x_column)
        plt.ylabel('Frequency')
        plt.title('Animated Histogram')

    def display_graph(self, instance):
        filename = self.file_chooser.selection and self.file_chooser.selection[0]
        if filename:
            try:
                data = pd.read_csv(filename)
                self.x_column = self.column_input_1.text
                self.y_column = self.column_input_2.text
                self.x_data = data[self.x_column]
                self.y_data = data[self.y_column]

                plot_type = self.spinner.text
                fig, ax = plt.subplots()
                ani = FuncAnimation(fig, self.animate, fargs=(plot_type,), frames=len(data), interval=1000)

                plt.tight_layout()
                plt.show()
            except Exception as e:
                self.show_error_popup(f"Error: {e}")
        else:
            self.show_error_popup("Please select a CSV file.")

    def print_csv(self, instance):
        filename = self.file_chooser.selection and self.file_chooser.selection[0]
        if filename:
            try:
                data = pd.read_csv(filename)
                self.csv_label.text = str(data)
            except Exception as e:
                self.show_error_popup(f"Error: {e}")
        else:
            self.show_error_popup("Please select a CSV file.")

    def show_error_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    CSVViewerApp().run()