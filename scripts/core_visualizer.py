# tkinter GUI libraries 
from tkinter import *
from tkinter import messagebox

# arg parse library for taking in 
# settings.xml as an argument 
import argparse

# user defined libraries and functions 
from gui import GUI
from figures import ProcessorMap, ProcessorGraphs
import read_data_file as rdf
import matplotlib.pyplot as plt
from processor_obj_file import Processor
from settings import Settings

from terminal_gui import TerminalGUI
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

        # objects to handle processor buffer state 
        # and processor graph visualiztions 
        self.processor_map = ProcessorMap(self.root)        
        self.processor_graphs = ProcessorGraphs(self.root)

        # settings object
        self.settings = Settings(args.settings_file_loc)

        # TODO get title from the setting files 
        self.gui = GUI(self.root,
                        self.processor_map,
                        self.processor_graphs,
                        self.processor_obj_list,
                        self.settings.get_project_title())


    def initialize_processor_obj_list(self):
        rdf.read_data_recoder_out(
            self.processor_obj_list, 
            self.settings.get_data_recorder_out_file_loc())


    def draw_processors(self):
        self.processor_map.draw(self.processor_obj_list,
            self.settings.get_processor_coordinate_file_loc())

    def pack_gui(self):
        self.gui.pack()

if __name__ == '__main__':

    core_visualizer = CoreVisualizer()

    # reading the data recorder out to read the processors data 
    core_visualizer.initialize_processor_obj_list()
    # packing the GUI
    core_visualizer.pack_gui()
    # drawing the figure for the processor objects 
    core_visualizer.draw_processors()

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
