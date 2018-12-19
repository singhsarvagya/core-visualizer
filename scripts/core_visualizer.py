# tkinter GUI libraries
# add verticle marker to the graphs 
from tkinter import *
from tkinter import messagebox

# arg parse library for taking in 
# settings.xml as an argument 
import argparse
import os

# user defined libraries and functions 
from gui import GUI
from figures import ProcessorMap, ProcessorGraphs
from processor_obj_file import Processor
from settings import Settings
from terminal_gui import TerminalGUI

import matplotlib.pyplot as plt
plt.style.use('bmh')

parser = argparse.ArgumentParser()
parser.add_argument('settings_file_loc')
args = parser.parse_args()


class CoreVisualizer:

    def __init__(self):
        # initializing a list for processor 
        # objects 
        self.processor_obj_list = []

        # terminal window for GUI
        self.root = Tk()
        # settings object
        self.settings = Settings(args.settings_file_loc)

        # objects to handle processor buffer state 
        # and processor graph visualiztions 
        self.processor_map = ProcessorMap(self.root)        
        self.processor_graphs = ProcessorGraphs(self.root,
                                                self.settings.get_graph_settings())

        self.gui = GUI(self.root,
                        self.processor_map,
                        self.processor_graphs,
                        self.processor_obj_list,
                        self.settings.get_project_title(), 
                        self.settings.get_gui_settings())

    '''
        Function reads the data recorder out file 
        and initialized the processor object list 
    '''
    def initialize_processor_obj_list(self):
        lines = tuple(open(self.settings.get_data_recorder_out_file_loc(), 'r'))

        # initializing the processor objects
        x = lines[0].rstrip().split(' ')
        
        # intialized the dictionary from 
        # processor name to processor index 
        Processor.initialize_processor_index_dic(x)
        
        # intialize all the processor objects 
        for i in range(2, 2+Processor.get_num_of_processors()):
            self.processor_obj_list.insert(i-2, Processor(x[i]))

        # reading the data from the file and
        # adding the data to each processor object 
        for i in range(1, len(lines)):
            data = lines[i].rstrip().split(' ')
            Processor.initialize_time_period_list(data[1])
            Processor.register_processor_data(self.processor_obj_list, data)


    '''
        Function used to set the initial range of time
        for the processor graphs 
    '''
    def setup_graph_time_range(self): 
        self.processor_graphs.set_graph_time_range(
            min(Processor.time_period_list), max(Processor.time_period_list))

    '''
        Function return the name of the processor 
        for the given set of x, y coordinates from the processor 
        map 
    '''
    def get_processor_name(self, x, y): 
        return Processor.get_processor_name(self.processor_obj_list, x, y)

    '''
        Function updates the processor graph 
        when user clicks on a certain processor 
    '''
    def update_graphs(self, x, y):
        processor_name = self.get_processor_name(x, y)
        self.processor_graphs.update(processor_name,
            self.processor_obj_list)

    '''
        Function draws the initial processor maps 
    '''
    def draw_processors(self):
        self.processor_map.draw(self.processor_obj_list,
            self.settings.get_processor_coordinate_file_loc(),
            self.settings.get_processor_object_settings())
        
    '''
        Function packs the GUI 
    '''
    def pack_gui(self):
        self.gui.pack()

if __name__ == '__main__':

    core_visualizer = CoreVisualizer()

    # reading the data recorder out to read the processors data 
    core_visualizer.initialize_processor_obj_list()
    # setting processor graph range 
    core_visualizer.setup_graph_time_range()
    # packing the GUI
    core_visualizer.pack_gui()
    # drawing the figure for the processor objects 
    core_visualizer.draw_processors()

    def on_pick(event):
        patch = event.artist
        if event.mouseevent.inaxes and event.mouseevent.button == 1\
                and not event.mouseevent.dblclick:
            core_visualizer.update_graphs(patch.xy[0], patch.xy[1])

    core_visualizer.processor_map.fig.canvas.callbacks.connect('pick_event', on_pick)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to exit the application?"):
            core_visualizer.root.destroy()
        sys.exit(0)
    core_visualizer.root.protocol("WM_DELETE_WINDOW", on_closing)

    core_visualizer.root.mainloop()
