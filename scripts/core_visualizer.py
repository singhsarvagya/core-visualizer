from tkinter import *
from tkinter import simpledialog
import argparse
from gui import GUI
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

    def draw(self, processor_obj_list):
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




class CoreVisualizer:

    def __init__(self):
        # initializing a list for processor 
        # objects 
        self.processor_obj_list = []

        # terminal window for GUI
        self.root = Tk()

        self.processor_map = ProcessorMap(self.root)        
        self.processor_graphs = ProcessorGraphs(self.root)
        self.gui = GUI(self.root, self.processor_map, self.processor_graphs, self.processor_obj_list, "fjfe")

    def initialize_processor_obj_list(self):
        rdf.read_data_recoder_out(self.processor_obj_list)

    def draw_processors(self):
        self.processor_map.draw(self.processor_obj_list)

    def pack_gui(self):
        self.gui.pack()

if __name__ == '__main__':
    core_visualizer = CoreVisualizer()
    core_visualizer.initialize_processor_obj_list()
    core_visualizer.pack_gui()
    core_visualizer.draw_processors()
    '''processor_obj_list = []
    rdf.read_data_recoder_out(processor_obj_list)

    # initializing the main frame of the GUI
    root = Tk()
    # This is used to have a matplotlib graph where the data is visualized
    pm = ProcessorMap(root)
    pg = ProcessorGraphs(root)
    gui = GUI(root, pm, pg)
    gui.pack()

    pm.draw()'''
    def on_pick(event):
        patch = event.artist
        if event.mouseevent.inaxes and event.mouseevent.button == 1\
                and not event.mouseevent.dblclick and patch.get_name():
            # pg.update(patch.get_name(), processor_obj_list)
            # graph.fig.canvas.draw()
            pass

    core_visualizer.processor_map.fig.canvas.callbacks.connect('pick_event', on_pick)

    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure you want to exit this application?"):
            core_visualizer.root.destroy()
            sys.exit(0)
    core_visualizer.root.protocol("WM_DELETE_WINDOW", on_closing)

    core_visualizer.root.mainloop()
