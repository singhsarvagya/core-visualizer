from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from terminal_gui import TerminalGUI


class Processor:
    '''
        time_period_index_dic:      Is a dictionary of timestamp to index of
                                    data in the processor.data[data_field]
                                    corresponding to this time stamps
        time_period_list:           List if timestamps in accending order in secs
        processor_index_dic: 

    '''
    time_period_index_dic = {}
    time_period_list = []
    processor_index_dic = {}
    time_index = 0
    current_time_index = 0
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
            # convert the time to sec 
            # assumes time in pico second 
            Processor.time_period_list.append(int(time)/10000000)
            Processor.time_period_index_dic[time] = Processor.time_index
            Processor.time_index += 1
        Processor.time_period_list.sort()


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
    def map_processor_graph_object(self, x_coordinate, y_coordinate, ax):
        self.processor_graph_obj = ProcessorGraph(x_coordinate, y_coordinate, self.name)
        return self.processor_graph_obj.map(ax)

    '''
        function return the timestamp for a given timestamp index 
    '''
    @staticmethod
    def get_time(time_state):
        for element in Processor.time_period_index_dic:
            if Processor.time_period_index_dic[element] == time_state:
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
        new_time_state = Processor.current_time_index + update_tag
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
                ProcessorGraph.update_stalled_state_patches(processor_obj_list, time)
            Processor.stalled_state_patch_collection_1 = PatchCollection(stalled_state_patch_list1, facecolors='red', edgecolors='red')
            ax.add_collection(Processor.stalled_state_patch_collection_1)
            Processor.stalled_state_patch_collection_2 = PatchCollection(stalled_state_patch_list2, facecolors='green', edgecolors='green')
            ax.add_collection(Processor.stalled_state_patch_collection_2)
            # updating buffer patches
            buffer_num_write_patch_list, buffer_num_read_patch_list = \
                ProcessorGraph.update_buffer_patches(processor_obj_list, time)
            Processor.buffer_num_read_patch_collection = PatchCollection(buffer_num_read_patch_list, facecolors='#0099CC', edgecolors='#0099CC')
            ax.add_collection(Processor.buffer_num_read_patch_collection)
            Processor.buffer_num_write_patch_collection = PatchCollection(buffer_num_write_patch_list, facecolors='#66CCFF', edgecolors='#66CCFF')
            ax.add_collection(Processor.buffer_num_write_patch_collection)
            TerminalGUI.print_func("Processor map changed to "+time+" ps.")

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
            return -1 
        return self.processor_graph_obj.x_coordinate, \
            self.processor_graph_obj.y_coordinate

# TODO define global constants for graph object
# dimensions 
class ProcessorGraph:
    max_buffer_value = 14500.0

    def __init__(self, x_coordinate, y_coordinate, name):
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

    def map(self, ax):
        # TODO make the dimensions here independent 
        # in all rectangle and circle
        outer_rec = Rectangle(xy=(self.x_coordinate, self.y_coordinate), width=800,
                              height=800,  picker=True, facecolor='none',
                              edgecolor='#d3d3d3', linewidth=2)
        ax.add_artist(outer_rec)
        self.patches_list += [Rectangle((self.x_coordinate, self.y_coordinate), 200, 0),
                              Rectangle((self.x_coordinate+200, self.y_coordinate), 200, 0),
                              Rectangle((self.x_coordinate+400, self.y_coordinate), 200, 0),
                              Rectangle((self.x_coordinate+600, self.y_coordinate), 200, 0),
                              Circle(xy=(int(self.x_coordinate)+700, int(self.y_coordinate)+700), radius=75)]

        self.processor_label = plt.annotate(self.name,
                                            xy=(self.x_coordinate+400, self.y_coordinate-125),
                                            horizontalalignment='center', verticalalignment='center',
                                            fontsize='7', weight='bold')
        return self.patches_list

    @staticmethod
    def update_stalled_state_patches(processor_obj_list, time):
        list1 = []
        list2 = []
        for processor in processor_obj_list:
            stalled_state_patch = processor.processor_graph_obj.patches_list[4]
            # time_index = Processor.time_period_index_dic[time]
            if processor.access_processor_data(time, "stalled") == 1:
                list1 += [stalled_state_patch]
            else:
                list2 += [stalled_state_patch]
        return list1, list2

    @staticmethod
    def update_buffer_patches(processor_object_list, time):
        list1 = []
        list2 = []

        # TODO remove 700 here 
        for processor in processor_object_list:

            num_write_0 = processor.access_processor_data(time, 'input_buffers[0].num_writes')
            processor.processor_graph_obj.patches_list[0].set_height(float(num_write_0)*700/ProcessorGraph.max_buffer_value)
            num_write_0_graph_obj  = processor.processor_graph_obj.patches_list[0]

            num_write_1 = processor.access_processor_data(time, 'input_buffers[1].num_writes')
            processor.processor_graph_obj.patches_list[2].set_height(float(num_write_1)*700/ProcessorGraph.max_buffer_value)
            num_write_1_graph_obj = processor.processor_graph_obj.patches_list[2]

            list1 += [num_write_0_graph_obj, num_write_1_graph_obj]

            num_read_0 = processor.access_processor_data(time, 'input_buffers[0].num_reads')
            processor.processor_graph_obj.patches_list[1].set_height(float(num_read_0)*700/ProcessorGraph.max_buffer_value)
            num_read_0_graph_obj = processor.processor_graph_obj.patches_list[1]

            num_read_1 = processor.access_processor_data(time, 'input_buffers[1].num_reads')
            processor.processor_graph_obj.patches_list[3].set_height(float(num_read_1)*700/ProcessorGraph.max_buffer_value)
            num_read_1_graph_obj = processor.processor_graph_obj.patches_list[3]

            list2 += [num_read_0_graph_obj, num_read_1_graph_obj]
        return list1, list2
