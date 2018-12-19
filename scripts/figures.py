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

        self.time_min = 0.0
        self.time_max = 0.0

        self.fig.patch.set_visible(False)
        self.fig.tight_layout(pad=0.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.show()

        self.y_max_bound = 2.7
        self.x_max_bound = 2.5

    # gets the min and max time for the graph 
    def set_graph_time_range(self, time_min, time_max): 
        self.time_min = time_min
        self.time_max = time_max


    '''
        Function create the suplots for the processor garphs
    '''
    def create_subplots(self):
        subplot_id = 511
        for i in range(0, len(self.graph_settings)):
            self.subplots.append(self.fig.add_subplot(subplot_id, aspect=0.225))
            subplot_id += 1

    '''
        Function set the subplot labels and axis's 
    '''
    def set_subplots(self, index):
        self.subplots[index].set_xbound(0.0, self.x_max_bound)
        self.subplots[index].set_ybound(-0.1, self.y_max_bound)
        self.subplots[index].set_yticks([])
        self.subplots[index].set_xticks([])
        self.subplots[index].set_xlabel(self.graph_settings[index]["x_label"])
        self.subplots[index].set_ylabel(self.graph_settings[index]["y_label"])

    def pack(self):
        for i in range(0, len(self.graph_settings)): 
            self.set_subplots(i)
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)

    '''
        Function is used to print the processor state
        when the processor graphs are updated
    '''
    def print_processor_state(self, processor): 
        # printing the clicked processor details on the terminal 
        time = Processor.get_time(Processor.current_time_index)
        data = processor.get_data_dictionary(time)
        msg = "Processor State: \n"
        msg += "Name: " + processor.name + "\n"
        msg += "Time: " + time + "\n"
        keys = sorted(list(data.keys()))
        for key in keys: 
            msg += (key + ": " + str(data[key]) + "\n")

        TerminalGUI.print_func(msg)

    '''
        The function is used to refactor the data for the graphs 
        so that it cleanly fits in the subplots 
    '''
    def refactor_graph_data(self, data, time_list, time_cursor): 
        data_new = []
        time_list_new = []
        time_cursor_new = time_cursor
        for i in range(0, len(time_list)): 
            # filtering out the time only between the time range 
            # defined by the user 
            if time_list[i] >=self.time_min and time_list[i] <= self.time_max:
                # reagjusting the time so that the whole graph can fit in the time range  
                time_list_new.append((time_list[i]-self.time_min)*(self.x_max_bound/(self.time_max - self.time_min)))
                data_new.append(data[i])
        # updating the position of the time cursor based on the time range 
        time_cursor_new = (time_cursor - self.time_min)*(self.x_max_bound/(self.time_max - self.time_min))
        
        return data_new, time_list_new, time_cursor_new

    def update(self, proc_name, processor_obj_list):
        if proc_name == None: 
            proc_name = self.current_processor 

        processor_obj = Processor.get_processor_obj(proc_name, processor_obj_list)
        self.current_processor = proc_name
        # getting the cuurent processor map time for time cursor 
        time_cursor = float(Processor.get_time(Processor.current_time_index))

        if processor_obj:
            for i in range(0, len(self.graph_settings)):
                # cleanign the previous graph from the subplot 
                self.subplots[i].clear()
                # scaling the data so that it fits in the plot 
                scale_factor = float(self.graph_settings[i]['scale_factor'])
                data = [data*scale_factor for data in processor_obj.data[self.graph_settings[i]['data_field']]]
                time_list = Processor.time_period_list

                # refactoring the data so that only the data for the selected time range is 
                # displayed 
                data, time_list, time_new = self.refactor_graph_data(data, time_list, time_cursor)

                # ploting the graph 
                self.subplots[i].plot(time_list,
                        data,
                        color="#00adce",
                        linewidth=0.5)
                # plotting the time cursor 
                self.subplots[i].plot((time_new, time_new), (0, 2.70),
                        color="#FF0000",
                        linewidth=0.75)
                # settign the subplots 
                self.set_subplots(i)
            # printing the processor states 
            self.print_processor_state(processor_obj)
            self.canvas.draw()
