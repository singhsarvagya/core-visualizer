from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from terminal_gui import TerminalGUI


class Processor:
    time_period_index_dic = {}
    time_period_list = []
    processor_index_dic = {}
    index = 0
    current_time_index = 0
    buffer_num_read_patch_collection = None
    buffer_num_write_patch_collection = None
    stalled_state_patch_collection_1 = None
    stalled_state_patch_collection_2 = None

    def __init__(self, name):
        self.name = name
        self.activity = []
        self.utilization = []
        self.stalled_state = []
        self.power_mW = []
        self.input_buffers_0_num_writes = []
        self.input_buffers_0_num_reads = []
        self.input_buffers_1_num_writes = []
        self.input_buffers_1_num_reads = []
        self.processor_graph_obj = None

    def access_activity(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.activity[index]
        else:
            raise Exception("Activity data for time %s ps not recorded" % time)

    def access_utilization(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.utilization[index]
        else:
            raise Exception("Utilization data for time %s ps not recorded" % time)

    def access_stalled_state(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.stalled_state[index]
        else:
            raise Exception("Stalled state data for time %s ps not recorded" % time)

    def access_power_mW(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.power_mW[index]
        else:
            raise Exception("Power data for time %s ps not recorded" % time)

    def access_input_buffers_0_num_writes(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.input_buffers_0_num_writes[index]
        else:
            raise Exception("Input buffer 0 num write data for time %s ps not recorded" % time)

    def access_input_buffers_0_num_reads(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.input_buffers_0_num_reads[index]
        else:
            raise Exception("Input buffer 0 num read d for time %s ps not recorded" % time)

    def access_input_buffers_1_num_writes(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.input_buffers_1_num_writes[index]
        else:
            raise Exception("Input buffer 1 num write data for time %s ps not recorded" % time)

    def access_input_buffers_1_num_reads(self, time):
        if time in Processor.time_period_index_dic:
            index = Processor.time_period_index_dic[time]
            return self.input_buffers_1_num_reads[index]
        else:
            raise Exception("Input buffer 1 num read data for time %s ps not recorded" % time)

    @staticmethod
    def initialize_time_period_index_dic(time):
        # also initialize time period list
        if time not in Processor.time_period_index_dic:
            Processor.time_period_list.append(int(time)/10000000)
            Processor.time_period_index_dic[time] = Processor.index
            Processor.index += 1
        Processor.time_period_list.sort()

    @staticmethod
    def initialize_processor_index_dic(data):
        for i in range(2, len(data)):
            Processor.processor_index_dic[data[i]] = i-2

    @staticmethod
    def initialize_activity(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.activity.insert(time_index, float(data[i]))

    @staticmethod
    def initialize_utilization(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.utilization.insert(time_index, float(data[i]))

    @staticmethod
    def initialize_stalled_state(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.stalled_state.insert(time_index, int(data[i]))

    @staticmethod
    def initialize_power_mW(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.power_mW.insert(time_index, float(data[i]))

    @staticmethod
    def initialize_input_buffer_0_num_writes(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.input_buffers_0_num_writes.insert(time_index, int(data[i]))

    @staticmethod
    def initialize_input_buffer_0_num_reads(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.input_buffers_0_num_reads.insert(time_index, int(data[i]))

    @staticmethod
    def initialize_input_buffer_1_num_writes(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.input_buffers_1_num_writes.insert(time_index, int(data[i]))

    @staticmethod
    def initialize_input_buffer_1_num_reads(processor_object_list, data, time):
        time_index = Processor.time_period_index_dic[time]
        for i in range(2, len(data)):
            processor = processor_object_list[i-2]
            processor.input_buffers_1_num_reads.insert(time_index, int(data[i]))

    def map_processor_graph_object(self, x_coordinate, y_coordinate, ax):
        self.processor_graph_obj = ProcessorGraph(x_coordinate, y_coordinate, self.name)
        return self.processor_graph_obj.map(ax)

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

    @staticmethod
    def get_time(time_state):
        for element in Processor.time_period_index_dic:
            if Processor.time_period_index_dic[element] == time_state:
                return element
        return None

    @staticmethod
    def get_processor_obj(processor_name, processor_obj_list):
        processor_index = Processor.processor_index_dic[processor_name]
        return processor_obj_list[processor_index]


class ProcessorGraph:
    max_buffer_value = 14500.0

    def __init__(self, x_coordinate, y_coordinate, name):
        self.name = name
        self.x_coordinate = int(x_coordinate)
        self.y_coordinate = int(y_coordinate)
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
        outer_rec = Rectangle(xy=(self.x_coordinate + 100, self.y_coordinate + 100), width=800,
                              height=800,  picker=True, facecolor='none',
                              edgecolor='#d3d3d3', linewidth=2)
        ax.add_artist(outer_rec)
        self.patches_list += [Rectangle((self.x_coordinate+100, self.y_coordinate+100), 200, 0),
                              Rectangle((self.x_coordinate+300, self.y_coordinate+100), 200, 0),
                              Rectangle((self.x_coordinate+500, self.y_coordinate+100), 200, 0),
                              Rectangle((self.x_coordinate+700, self.y_coordinate+100), 200, 0),
                              Circle(xy=(int(self.x_coordinate)+800, int(self.y_coordinate)+800), radius=75)]

        self.processor_label = plt.annotate(self.name,
                                            xy=(self.x_coordinate+500, self.y_coordinate-25),
                                            horizontalalignment='center', verticalalignment='center',
                                            fontsize='7', weight='bold')
        return self.patches_list

    @staticmethod
    def update_stalled_state_patches(processor_obj_list, time):
        list1 = []
        list2 = []
        for processor in processor_obj_list:
            stalled_state_patch = processor.processor_graph_obj.patches_list[4]
            time_index = Processor.time_period_index_dic[time]
            if processor.stalled_state[time_index] == 1:
                list1 += [stalled_state_patch]
            else:
                list2 += [stalled_state_patch]
        return list1, list2

    @staticmethod
    def update_buffer_patches(processor_object_list, time):
        list1 = []
        list2 = []
        for processor in processor_object_list:

            num_write_0 = processor.access_input_buffers_0_num_writes(time)
            processor.processor_graph_obj.patches_list[0].set_height(float(num_write_0)*700/ProcessorGraph.max_buffer_value)
            num_write_0_graph_obj  = processor.processor_graph_obj.patches_list[0]

            num_write_1 = processor.access_input_buffers_1_num_writes(time)
            processor.processor_graph_obj.patches_list[2].set_height(float(num_write_1)*700/ProcessorGraph.max_buffer_value)
            num_write_1_graph_obj = processor.processor_graph_obj.patches_list[2]

            list1 += [num_write_0_graph_obj, num_write_1_graph_obj]

            num_read_0 = processor.access_input_buffers_0_num_reads(time)
            processor.processor_graph_obj.patches_list[1].set_height(float(num_read_0)*700/ProcessorGraph.max_buffer_value)
            num_read_0_graph_obj = processor.processor_graph_obj.patches_list[1]

            num_read_1 = processor.access_input_buffers_1_num_reads(time)
            processor.processor_graph_obj.patches_list[3].set_height(float(num_read_1)*700/ProcessorGraph.max_buffer_value)
            num_read_1_graph_obj = processor.processor_graph_obj.patches_list[3]

            list2 += [num_read_0_graph_obj, num_read_1_graph_obj]
        return list1, list2

    @staticmethod
    def clean_patches(processor_obj_list):
        list = []
        for processor in processor_obj_list:
            graph_obj = processor.processor_graph_obj
            list += graph_obj.patches_list
        return list
