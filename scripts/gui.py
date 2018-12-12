from processor_obj_file import Processor
from terminal_gui import TerminalGUI
from tkinter import *
from tkinter import simpledialog
import subprocess
from tkinter import messagebox, filedialog
import os

class GUI:
    def __init__(self,
        root,
        processor_map,
        processor_graphs,
        processor_obj_list, 
        title):

        # initializing the tkinter root window 
        self.root = root

        # intializing the title of the window 
        if title != None and len(title) > 0: 
            self.root.title(title)
        else:
            self.root.title("Core Visualizer")

        # making an object copy of the matplotlib graph object 
        self.processor_map = processor_map
        self.processor_graphs = processor_graphs

        # initializing the other GUI objest 
        self.terminal_gui_obj = TerminalGUI(self.root)
        self.menu_gui = MenuGUI(self.root, processor_map.fig)
        self.toolbar = ToolBar(root, processor_map.ax, processor_map.fig, processor_obj_list)

    # packing all the gui objects 
    def pack(self):
        self.toolbar.pack()
        self.processor_map.pack()
        self.processor_graphs.pack()
        self.terminal_gui_obj.pack()

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
        # don' save the file if the user provides an invalid name 
        if name != '' or name != None:
            self.fig.savefig(name)

    '''
        Function on the main menu. Can be used to open help manual
    '''
    # TODO bug here 
    # in linux
    # works fine in windows 
    def help_func(self):
        subprocess.Popen(["~/core-visualizer/help.txt"], shell=True)

'''
    Class for toolbar GUI
'''
class ToolBar:

    def __init__(self, root, ax, figure, processor_obj_list):
        self.root = root
        self.toolbar = Frame(root)
        self.figure = figure
        self.ax = ax

        # buttons for the next and previous buffer states
        self.next_button = Button(self.toolbar,
                                    text="Next",
                                    command=self.update_next)
        self.prev_button = Button(self.toolbar, 
                                    text="Prev",
                                    command=self.update_prev)
        self.prev_button.pack(side=LEFT, padx=2, pady=2)
        self.next_button.pack(side=LEFT, padx=2, pady=2)

        # button for change step size 
        self.change_step_size_button = Button(self.toolbar,
                                                text="Step Size", 
                                                command=self.change_step_size)
        self.change_step_size_button.pack(side=LEFT, padx=2, pady=2)

        # processor object list 
        self.processor_obj_list = processor_obj_list
        self.step_size = 20

    def pack(self):
        self.toolbar.pack(side=TOP, fill=X)

    '''
        Jumps to next step. Step size can be adjusted
    '''
    def update_next(self):
        Processor.update_processor_map(self.processor_obj_list, self.ax, self.step_size)
        self.figure.canvas.draw()

    '''
        Jumps to previous step. Size of the step can be adjusted
    '''
    def update_prev(self):
        Processor.update_processor_map(self.processor_obj_list, self.ax, -self.step_size)
        self.figure.canvas.draw()

    '''
        Function changes the steps size of the next or prev steps 
    '''
    def change_step_size(self):
        self.step_size = simpledialog.askinteger("Step Size", "Enter Step Size (integer):")
        TerminalGUI.print_func("Step size changed to: "+ str(self.step_size))