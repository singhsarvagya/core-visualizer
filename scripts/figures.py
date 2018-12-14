from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PatchCollection
from processor_obj_file import Processor
from terminal_gui import TerminalGUI

PM_FIGURE_ID = 1
SPM_FIGURE_ID = 2

# TODO update the subplot to a marker when user timesteps into it 

class ProcessorMap:
    def __init__(self, root):

        # initializing the plt plot for processor map 
        self.fig = plt.figure(PM_FIGURE_ID, frameon=False)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.patch.set_visible(False)

        self.ax.axis([-500, 10500, -500, 10500])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.fig.tight_layout(pad=0.2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.show()

    # TODO remove the rdf dependency 
    def draw(self, processor_obj_list, processor_coordinate_file_loc):
        plt.figure(PM_FIGURE_ID)

        lines = tuple(open(processor_coordinate_file_loc, 'r'))
        patch_list = []

        # reading processor objects, and x and y coordinates 
        # for the lower left corner of the processor figure 
        for line in lines:
            data = line.rstrip().split(',')
            # initializing the processor object list based on their name  
            processor = processor_obj_list[Processor.processor_index_dic[data[0]]]
            patch_list += processor.map_processor_graph_object(data[2],
                data[1],
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
        self.create_subplots()

        self.current_processor = None 

        self.fig.patch.set_visible(False)
        self.fig.tight_layout(pad=0.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.show()

    def create_subplots(self):
        subplot_id = 511
        for i in range(0, len(self.graph_settings)):
            self.subplots.append(self.fig.add_subplot(subplot_id, aspect=0.225))
            subplot_id += 1

    def set_subplots(self, index):
        self.subplots[index].set_xbound(-0.1, 2.75)
        self.subplots[index].set_ybound(-0.1, 2.7)
        self.subplots[index].set_yticks([])
        self.subplots[index].set_xticks([])
        self.subplots[index].set_xlabel(self.graph_settings[index]["x_label"])
        self.subplots[index].set_ylabel(self.graph_settings[index]["y_label"])

    def pack(self):
        for i in range(0, len(self.graph_settings)): 
            self.set_subplots(i)
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)

    def update(self, proc_name, processor_obj_list):
        processor_obj = Processor.get_processor_obj(proc_name, processor_obj_list)
        self.current_processor = proc_name
        if processor_obj:
            for i in range(0, len(self.graph_settings)):
                self.subplots[i].clear()
                scale_factor = float(self.graph_settings[i]['scale_factor'])
                data = [data*scale_factor for data in processor_obj.data[self.graph_settings[i]['data_field']]]
                self.subplots[i].plot(Processor.time_period_list,
                        data,
                        color="#00adce",
                        linewidth=0.5)
                self.set_subplots(i)
                # TODO add a terminal message that prints the current state of the processor 
            self.canvas.draw()
        else:
            # TODO change this to a dialog box or terminal message 
            messagebox.askokcancel("Error", "Clicked processor object not found.") 
