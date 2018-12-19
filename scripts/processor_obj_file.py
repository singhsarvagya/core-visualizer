from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from terminal_gui import TerminalGUI


class Processor:
    '''
        time_period_index_dic:      Is a dictionary of timestamp to index of
                                    data in the processor.data[data_field]
                                    corresponding to this time stamps
        time_period_list:           List if timestamps in accending order
        processor_index_dic:        dictionary of processor name->index
                                    in the porcessor_object_list
        time_index:                 Used to initialize the time_index_list 
        current_time_index:         used to store the current time index 
                                    of the processor 

    '''
    time_period_index_dic = {}
    time_period_list = []
    processor_index_dic = {}
    time_index = 0
    current_time_index = 0
    # patch collection objects for buffer 
    # and stalled states for visualization 
    buffer_num_read_patch_collection = None
    buffer_num_write_patch_collection = None
    stalled_state_patch_collection_1 = None
    stalled_state_patch_collection_2 = None

    def __init__(self, name):
        self.name = name
        self.data = {}
        self.processor_graph_obj = None

    '''
        function intialized the time_period_list
        and time_period_index_dic 
    '''
    @staticmethod
    def initialize_time_period_list(time):
        # also initialize time period list
        if time not in Processor.time_period_index_dic:
            Processor.time_period_list.append(int(time))
            Processor.time_period_index_dic[time] = Processor.time_index
            Processor.time_index += 1
        Processor.time_period_list.sort()

    '''
        function returns the number of processors 
    '''
    @staticmethod
    def get_num_of_processors(): 
        return len(Processor.processor_index_dic.keys())

    '''
        function returns the name of the processor 
        for a given set of coordinate from the 
        coordinate map 
    '''
    @ staticmethod
    def get_processor_name(processor_obj_list, x, y):
        for processor in processor_obj_list:
            proc_x, proc_y = processor.get_processor_graph_obj_coordinates()
            if proc_x == x and proc_y == y: 
                return processor.name
        return None 

    '''
        Function takes in time_stamp and 
        name of the data field as input and
        returns the data value for the given
        input  
    '''
    def access_processor_data(self, time, data_field): 
        if time in Processor.time_period_index_dic:
            time_index = Processor.time_period_index_dic[time]
            return self.data[data_field][time_index]
        else:
            raise Exception("%s data for time %s ps not recorded" % data_field % time)


    '''
        Function initialized the index of the processor 
        corresponding to its name from the first line 
        of data_recorder_out file 
    '''
    @staticmethod
    def initialize_processor_index_dic(data):
        for i in range(2, len(data)):
            Processor.processor_index_dic[data[i]] = i-2

    '''
        function assigns the data in the data stream 
        to its given processor 
    '''
    @staticmethod
    def register_processor_data(processor_object_list, data):
        # get the data field from the data stream 
        data_field = data[0]
        # get the timestamp from the data stream  
        time = data[1]
        # get the time index
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            # initialize the list for the given data field 
            # for the processor if it is not already done
            if data_field not in processor.data:  
                processor.data[data_field] = []
            # add the data to the processor 
            # at the given data_field list and at the given time_index 
            processor.data[data_field].insert(time_index, float(data[i]))

    '''
        function creates a processor graph object for a given 
        processors and maps it to a subplot 
    '''
    def map_processor_graph_object(self, x_coordinate, y_coordinate, ax, processor_object_settings):
        self.processor_graph_obj = ProcessorGraph(x_coordinate,
            y_coordinate,
            self.name,
            processor_object_settings)
        return self.processor_graph_obj.map(ax)

    '''
        function return the timestamp for a given timestamp index 
    '''
    @staticmethod
    def get_time(time_index):
        for element in Processor.time_period_index_dic:
            if Processor.time_period_index_dic[element] == time_index:
                return element
        return None

    '''
        the function return the processor object for 
        a given processor name 
    '''
    @staticmethod
    def get_processor_obj(processor_name, processor_obj_list):
        if processor_name in Processor.processor_index_dic:
            processor_index = Processor.processor_index_dic[processor_name]
            return processor_obj_list[processor_index]
        return None 


    @staticmethod
    def update_processor_map(processor_obj_list, ax, update_tag):
        new_time_state = update_tag
        if new_time_state < 0:
            TerminalGUI.print_func("Processor map already at minimum time period.")
        elif new_time_state >= len(Processor.time_period_index_dic):
            TerminalGUI.print_func("Processor map already at maximum time period")
        else:
            # get time at new_time_state
            time = Processor.get_time(new_time_state)
            # update the current time index
            Processor.current_time_index = new_time_state
            # clean previous patches
            Processor.clean_graph()
            # updating stalled state patched to their respective colors
            stalled_state_patch_list1, stalled_state_patch_list2 = \
                Processor.update_all_stalled_state_patches(processor_obj_list, time)
            Processor.stalled_state_patch_collection_1 = PatchCollection(stalled_state_patch_list1, facecolors='red', edgecolors='red')
            ax.add_collection(Processor.stalled_state_patch_collection_1)
            Processor.stalled_state_patch_collection_2 = PatchCollection(stalled_state_patch_list2, facecolors='green', edgecolors='green')
            ax.add_collection(Processor.stalled_state_patch_collection_2)
            # updating buffer patches
            buffer_num_write_patch_list, buffer_num_read_patch_list = \
                Processor.update_all_buffer_patches(processor_obj_list, time)
            Processor.buffer_num_read_patch_collection = PatchCollection(buffer_num_read_patch_list, facecolors='#0099CC', edgecolors='#0099CC')
            ax.add_collection(Processor.buffer_num_read_patch_collection)
            Processor.buffer_num_write_patch_collection = PatchCollection(buffer_num_write_patch_list, facecolors='#66CCFF', edgecolors='#66CCFF')
            ax.add_collection(Processor.buffer_num_write_patch_collection)
            TerminalGUI.print_func("Processor map changed to "+time+" ps.")

    '''
        Function used to removed the old buffer patch collections 
    '''
    @staticmethod
    def clean_graph():
        if Processor.stalled_state_patch_collection_1:
            Processor.stalled_state_patch_collection_1.remove()
        if Processor.stalled_state_patch_collection_2:
            Processor.stalled_state_patch_collection_2.remove()
        if Processor.buffer_num_read_patch_collection:
            Processor.buffer_num_read_patch_collection.remove()
        if Processor.buffer_num_write_patch_collection:
            Processor.buffer_num_write_patch_collection.remove()


    def get_processor_graph_obj_coordinates(self):
        if self.processor_graph_obj == None:
            return None
        return self.processor_graph_obj.get_coordinates()


    '''
        Function returns the data for a processor state at a given time
        in the dictionary format 
    '''
    def get_data_dictionary(self, time): 
        data_dic = {}
        for key in self.data.keys(): 
            data_dic[key] = self.access_processor_data(time, key)
        return data_dic


    '''
        Function gets the buffer states for the porcessor 
        And updates the patches 
    '''
    def update_buffer_patches(self, time):
        num_write_0 = self.access_processor_data(time, 'input_buffers[0].num_writes')
        num_write_1 = self.access_processor_data(time, 'input_buffers[1].num_writes')
        num_read_0 = self.access_processor_data(time, 'input_buffers[0].num_reads')
        num_read_1 = self.access_processor_data(time, 'input_buffers[1].num_reads')

        # returning the updated patches 
        return self.processor_graph_obj.update_buffer_patches(num_write_0, num_write_1, num_read_0, num_read_1)


    # function returns the stalled state and its patch object for a given processor 
    def update_stalled_state_patches(self, time): 
        stalled_state = self.access_processor_data(time, "stalled")
        stalled_state_patch = self.processor_graph_obj.get_stalled_state_patch()
        return stalled_state_patch, stalled_state


    '''
        Function updates the buffer patches for all the processors 
        for the given time 
    '''
    @staticmethod
    def update_all_buffer_patches(processor_object_list, time):
        list1 = []
        list2 = []

        for processor in processor_object_list:
            # getting the buffer values for the given time 
            # updating the patch object 
            num_write_0_graph_obj, num_write_1_graph_obj, num_read_0_graph_obj, num_read_1_graph_obj \
                = processor.update_buffer_patches(time)
            list1 += [num_write_0_graph_obj, num_write_1_graph_obj]
            list2 += [num_read_0_graph_obj, num_read_1_graph_obj]
        
        return list1, list2


    '''
        Function updates the stalled state patches for all the processors 
        for the given time 
    '''
    @staticmethod
    def update_all_stalled_state_patches(processor_obj_list, time):
        list1 = []
        list2 = []
        for processor in processor_obj_list: 
            stalled_state_patch, stalled_state = processor.update_stalled_state_patches(time)
            if stalled_state == 1:
                list1 += [stalled_state_patch]
            else:
                list2 += [stalled_state_patch]
        return list1, list2


class ProcessorGraph:

    def __init__(self, x_coordinate, y_coordinate, name, processor_object_settings):
        # used to create annotation 
        self.name = name
        self.x_coordinate = int(x_coordinate)+100
        self.y_coordinate = int(y_coordinate)+100
        '''
            patches_list:
                0: buffer num write 0
                1: buffer num read 0
                2: buffer num write 1
                3: buffer num read 1
                4: stalled state
        '''
        self.patches_list = []
        self.processor_label = None

        # settings 
        self.max_buffer_value \
            = float(processor_object_settings['max_buffer_value'])
        self.dimension \
            = float(processor_object_settings['processor_size'])
        self.radius \
            = float(processor_object_settings['stalled_state_radius'])

    # This function create patches and annotations 
    # for the a processor given processor coordinates 
    def map(self, ax):
        # figure for the outter rectangle of the processors 
        # int th processor maps 
        outer_rec = Rectangle(xy=(self.x_coordinate, self.y_coordinate),
            width=self.dimension,
            height=self.dimension,
            picker=True,
            facecolor='none',
            edgecolor='#d3d3d3',
            linewidth=2)
        ax.add_artist(outer_rec)

        self.patches_list += [Rectangle((self.x_coordinate, self.y_coordinate),
                                self.dimension/4, 0),
                              Rectangle((self.x_coordinate+(self.dimension/4),
                                self.y_coordinate),
                                self.dimension/4, 0),
                              Rectangle((self.x_coordinate+(2*self.dimension/4),
                                self.y_coordinate),
                                self.dimension/4, 0),
                              Rectangle((self.x_coordinate+(3*self.dimension/4),
                                self.y_coordinate),
                                self.dimension/4, 0),
                              Circle(xy=(int(self.x_coordinate)+(7*self.dimension/8),
                                int(self.y_coordinate)+(7*self.dimension/8)),
                                radius=self.radius)]

        self.processor_label = plt.annotate(self.name,
                                xy=(self.x_coordinate+self.dimension/2, self.y_coordinate-150),
                                horizontalalignment='center',
                                verticalalignment='center',
                                fontsize='7', weight='bold')
        return self.patches_list

    # function updates the size of the buffer patches on the map 
    # to the given buffer value 
    def update_buffer_patches(self, num_write_0, num_write_1, num_read_0, num_read_1):

        # only useds 80% of the self.dimention to represent buffer 
        # looks pretty 
        self.patches_list[0].set_height(0.8*self.dimension*float(num_write_0)/self.max_buffer_value)
        num_write_0_graph_obj  = self.patches_list[0]

        self.patches_list[2].set_height(0.8*self.dimension*float(num_write_1)/self.max_buffer_value)
        num_write_1_graph_obj = self.patches_list[2]

        self.patches_list[1].set_height(0.8*self.dimension*float(num_read_0)/self.max_buffer_value)
        num_read_0_graph_obj = self.patches_list[1]

        self.patches_list[3].set_height(0.8*self.dimension*float(num_read_1)/self.max_buffer_value)
        num_read_1_graph_obj = self.patches_list[3]

        return [num_write_0_graph_obj, num_write_1_graph_obj, num_read_0_graph_obj, num_read_1_graph_obj] 

    # function returns the stalled state patch 
    def get_stalled_state_patch(self): 
        return self.patches_list[4]

    def get_coordinates(self): 
        return self.x_coordinate, \
            self.y_coordinate