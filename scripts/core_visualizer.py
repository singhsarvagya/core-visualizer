from tkinter import *
from tkinter import simpledialog
import argparse
import read_data_file as rdf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PatchCollection
from processor_obj_file import Processor
import subprocess
from tkinter import messagebox, filedialog
import os
import xml.etree.ElementTree as ET
from terminal_gui import TerminalGUI
plt.style.use('bmh')

PM_FIGURE_ID = 1
SPM_FIGURE_ID = 2

parser = argparse.ArgumentParser()
parser.add_argument('settings_file_loc')
args = parser.parse_args()

class ProcessorMap:
    def __init__(self, root):
        self.fig = plt.figure(PM_FIGURE_ID, frameon=False)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.patch.set_visible(False)
        self.ax.axis([-500, 10500, -500, 10500])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.fig.tight_layout(pad=0.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.show()

    def draw(self):
        plt.figure(PM_FIGURE_ID)
        patch_list = rdf.plot_processor(processor_obj_list, self.ax)
        p = PatchCollection(patch_list, facecolor='none')
        self.ax.add_collection(p)

    def pack(self):
        self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)


class ProcessorGraphs:
    def __init__(self, root):
        self.fig = plt.figure(SPM_FIGURE_ID)
        self.sub_plot_activity = self.fig.add_subplot(511, aspect=0.225)
        self.sub_plot_utilization = self.fig.add_subplot(512, aspect=0.225)
        self.sub_plot_stalled_state = self.fig.add_subplot(513, aspect=0.225)
        self.sub_plot_power_mW = self.fig.add_subplot(514, aspect=0.225)
        self.sub_plot_buffer = self.fig.add_subplot(515, aspect=0.225)
        self.fig.patch.set_visible(False)
        self.fig.tight_layout(pad=0.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.show()

    def pack(self):
        self.set_activity_graph()
        self.set_utilization_graph()
        self.set_power_mW_graph()
        self.set_stalled_state_graph()
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)

    def set_activity_graph(self):
        self.sub_plot_activity.set_xbound(-0.1, 2.75)
        self.sub_plot_activity.set_ybound(-0.1, 2.7)
        self.sub_plot_activity.set_yticks([])
        self.sub_plot_activity.set_xticks([])
        self.sub_plot_activity.set_xlabel("Time(ps)")
        self.sub_plot_activity.set_ylabel("Activity")

    def set_utilization_graph(self):
        self.sub_plot_utilization.set_xbound(-0.1, 2.75)
        self.sub_plot_utilization.set_ybound(-0.1, 2.7)
        self.sub_plot_utilization.set_yticks([])
        self.sub_plot_utilization.set_xticks([])
        self.sub_plot_utilization.set_xlabel("Time(ps)")
        self.sub_plot_utilization.set_ylabel("Utilization")

    def set_stalled_state_graph(self):
        self.sub_plot_stalled_state.set_xbound(-0.1, 2.75)
        self.sub_plot_stalled_state.set_ybound(-0.1, 2.7)
        self.sub_plot_stalled_state.set_yticks([])
        self.sub_plot_stalled_state.set_xticks([])
        self.sub_plot_stalled_state.set_xlabel("Time(ps)")
        self.sub_plot_stalled_state.set_ylabel("Stalled State")

    def set_power_mW_graph(self):
        self.sub_plot_power_mW.set_xbound(-0.1, 2.75)
        self.sub_plot_power_mW.set_ybound(-0.1, 2.7)
        self.sub_plot_power_mW.set_yticks([])
        self.sub_plot_power_mW.set_xticks([])
        self.sub_plot_power_mW.set_xlabel("Time(ps)")
        self.sub_plot_power_mW.set_ylabel("Power(mW)")

    def plot_activity_graph(self, processor_obj):
        self.sub_plot_activity.clear()
        activity_factor = 2.5
        activity_list = [data*activity_factor for data in processor_obj.activity]
        self.sub_plot_activity.plot(Processor.time_period_list, activity_list, color='#00adce', linewidth=1)
        self.set_activity_graph()

    def plot_utilization(self, processor_obj):
        self.sub_plot_utilization.clear()
        utilization_factor = 2.5
        utilization_list = [data*utilization_factor for data in processor_obj.utilization]
        self.sub_plot_utilization.plot(Processor.time_period_list, utilization_list, color='#00adce', linewidth=1)
        self.set_utilization_graph()

    def plot_stalled_state(self, processor_obj):
        self.sub_plot_stalled_state.clear()
        stalled_state_factor = 2.5
        stalled_state_list = [data*stalled_state_factor for data in processor_obj.stalled_state]
        self.sub_plot_stalled_state.step(Processor.time_period_list, stalled_state_list, color='#00adce', linewidth=0.8)
        self.set_stalled_state_graph()

    def plot_power_mW(self, processor_obj):
        self.sub_plot_power_mW.clear()
        power_mW_factor = 0.1
        power_mW_list = [data*power_mW_factor for data in processor_obj.power_mW]
        self.sub_plot_power_mW.stackplot(Processor.time_period_list, power_mW_list, color='#00adce')
        self.set_power_mW_graph()

    def update(self, proc_name, processor_obj_list):
        processor_obj = Processor.get_processor_obj(proc_name, processor_obj_list)
        if processor_obj_list:
            self.plot_activity_graph(processor_obj)
            self.plot_utilization(processor_obj)
            self.plot_stalled_state(processor_obj)
            self.plot_power_mW(processor_obj)
            self.canvas.draw()
        else:
            print("Clicked processor object not found")


class GUI:
    def __init__(self, root, processor_map, processor_graphs):
        self.root = root
        self.root.title("Core Visualizer")
        self.processor_map = processor_map
        self.processor_graphs = processor_graphs
        self.terminal_gui_obj = TerminalGUI(self.root)
        self.menu_gui = MenuGUI(self.root, processor_map.fig)
        self.toolbar = ToolBar(root, processor_map.ax, processor_map.fig)

    def pack(self):
        self.toolbar.pack()
        self.processor_map.pack()
        self.processor_graphs.pack()
        # self.terminal_gui_obj.pack()


'''
    Main menu function
'''
class MenuGUI:

    def __init__(self, root, fig):

        # creating a menu bar at the top of the GUI
        self.root = root
        self.fig = fig
        self.menu = Menu(root)
        self.root.config(menu=self.menu)

        # creating file tab in menu with Start, Save Figure and Exit in a drop down menu
        self.subMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Save Figure", command=self.save_fig)
        self.subMenu.add_separator()
        self.subMenu.add_command(label="Exit", command=self.exit_func)

        self.settingsMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Settings", menu=self.settingsMenu)
        self.settingsMenu.add_command(label="Change Step Size", command=ToolBar.change_step_size)

        # creating help menu; If you chose help, it will open a help file stored where the project is stored
        self.helpMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="Help", command=self.help_func)

    '''
        Function used to quit the function
    '''
    def exit_func(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to exit this application?"):
            self.root.destroy()
            sys.exit(0)

    ''' Executed when File->Save Figure is chosen. Asks the user for file name and location and save the current
        graph on the screen at given location with the given filename. The file produced is of .png format'''
    def save_fig(self):
        name = filedialog.asksaveasfilename(defaultextension=".png", initialdir=os.path.expanduser('~'))

        if name != '' or name != None:
            self.fig.savefig(name)

    '''
        Function on the main menu. Can be used to open help manual
    '''
    def help_func(self):
        subprocess.Popen(["user_guide.txt"], shell=True)

'''
    Class for toolbar GUI
'''
class ToolBar:
    step_size = 20
    ax = None

    def __init__(self, root, ax, figure):
        self.root = root
        self.toolbar = Frame(root)
        self.figure = figure
        ToolBar.ax = ax
        self.next_button = Button(self.toolbar, text="Next", command=self.update_next)
        self.prev_button = Button(self.toolbar, text="Prev", command=self.update_prev)
        self.prev_button.pack(side=LEFT, padx=2, pady=2)
        self.next_button.pack(side=LEFT, padx=2, pady=2)

    def pack(self):
        self.toolbar.pack(side=TOP, fill=X)

    '''
        Jumps to next step. Step size can be adjusted
    '''
    def update_next(self):
        Processor.update_processor_map(processor_obj_list, ToolBar.ax, ToolBar.step_size)
        self.figure.canvas.draw()

    '''
        Jumps to previous step. Size of the step can be adjusted
    '''
    def update_prev(self):
        Processor.update_processor_map(processor_obj_list, ToolBar.ax, -ToolBar.step_size)
        self.figure.canvas.draw()

    @staticmethod
    def change_step_size():
        ToolBar.step_size = simpledialog.askinteger("Step Size", "Enter Step Size (integer):")
        TerminalGUI.print_func("Step size changed to: "+ str(ToolBar.step_size))

if __name__ == '__main__':
    processor_obj_list = []
    rdf.read_data_recoder_out(processor_obj_list)

    # initializing the main frame of the GUI
    root = Tk()
    # This is used to have a matplotlib graph where the data is visualized
    pm = ProcessorMap(root)
    pg = ProcessorGraphs(root)
    gui = GUI(root, pm, pg)
    gui.pack()

    pm.draw()
    def on_pick(event):
        patch = event.artist
        if event.mouseevent.inaxes and event.mouseevent.button == 1\
                and not event.mouseevent.dblclick and patch.get_name():
            pg.update(patch.get_name(), processor_obj_list)
            #graph.fig.canvas.draw()

    pm.fig.canvas.callbacks.connect('pick_event', on_pick)

    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure you want to exit this application?"):
            root.destroy()
            sys.exit(0)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
