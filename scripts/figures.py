from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PatchCollection
import read_data_file as rdf

PM_FIGURE_ID = 1
SPM_FIGURE_ID = 2

class ProcessorMap:
    def __init__(self, root):

        # initializing the plt plot for processor map 
        self.fig = plt.figure(PM_FIGURE_ID, frameon=False)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.patch.set_visible(False)

        # TODO make this intilization using settings file 
        self.ax.axis([-500, 10500, -500, 10500])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.fig.tight_layout(pad=0.2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.show()

    # TODO remove the rdf dependency 
    def draw(self, processor_obj_list):
        plt.figure(PM_FIGURE_ID)
        patch_list = rdf.plot_processor(processor_obj_list, self.ax)
        p = PatchCollection(patch_list, facecolor='none')
        self.ax.add_collection(p)

    # packing the figure on the root window 
    def pack(self):
        self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)

# TODO reduce this shit using settings.xml 
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