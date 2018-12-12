from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PatchCollection
import read_data_file as rdf
from processor_obj_file import Processor


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
    def draw(self, processor_obj_list, processor_coordinate_file_loc):
        plt.figure(PM_FIGURE_ID)
        patch_list = rdf.plot_processor(processor_obj_list,
            processor_coordinate_file_loc, 
            self.ax)
        p = PatchCollection(patch_list, facecolor='none')
        self.ax.add_collection(p)

    # packing the figure on the root window 
    def pack(self):
        self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)


class ProcessorGraphs:
    def __init__(self, root, settings):
        self.fig = plt.figure(SPM_FIGURE_ID)

        # settings the subplots 
        self.graph_settings = settings
        self.subplots = []
        self.set_subplots()

        self.fig.patch.set_visible(False)
        self.fig.tight_layout(pad=0.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.show()

    def set_subplots(self):
        subplot_id = 511
        for i in range(0, len(self.graph_settings)):
            self.subplots.append(self.fig.add_subplot(subplot_id, aspect=0.225))
            subplot_id += 1

    def pack(self):
        for i in range(0, len(self.graph_settings)): 
            self.subplots[i].set_xbound(-0.1, 2.75)
            self.subplots[i].set_ybound(-0.1, 2.7)
            self.subplots[i].set_yticks([])
            self.subplots[i].set_xticks([])
            self.subplots[i].set_xlabel(self.graph_settings[i]["x_label"])
            self.subplots[i].set_ylabel(self.graph_settings[i]["y_label"])
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)

    def update(self, proc_name, processor_obj_list):
        processor_obj = Processor.get_processor_obj(proc_name, processor_obj_list)
        if processor_obj:
            for i in range(0, len(self.graph_settings)):
                self.subplots[i].clear()
                scale_factor = float(self.graph_settings[i]['scale_factor'])
                data = [data*scale_factor for data in processor_obj.data[self.graph_settings[i]['data_field']]]
                self.subplots[i].plot(Processor.time_period_list,
                        data,
                        color="#00adce",
                        linewidth=0.5)
                self.subplots[i].set_xbound(-0.1, 2.75)
                self.subplots[i].set_ybound(-0.1, 2.7)
                self.subplots[i].set_yticks([])
                self.subplots[i].set_xticks([])
                self.subplots[i].set_xlabel(self.graph_settings[i]["x_label"])
                self.subplots[i].set_ylabel(self.graph_settings[i]["y_label"])
                # TODO add a terminal message that prints the current state of the processor 
            self.canvas.draw()
        else:
            # TODO change this to a dialog box or terminal message 
            print("Clicked processor object not found")