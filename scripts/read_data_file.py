from processor_obj_file import Processor
total_processors = 100
# data_recoder_out_file = "sample_data/data_recorder_out.txt"
# processor_coordinate_file = "settings/processor_coordinate.csv"

def read_data_recoder_out(processor_obj_list,
                          data_recoder_out_file_loc):
    '''
    This function reads data from the data_recoder_out_file and
    initializes the processor objects using that data

    :param processor_obj_list: The dictionary containing processor objects
    :return:
    '''
    lines = tuple(open(data_recoder_out_file_loc, 'r'))

    # initializing the processor objects
    x = lines[0].rstrip().split(' ')
    Processor.initialize_processor_index_dic(x)
    for i in range(2, 2+total_processors):
        processor_obj_list.insert(i-2, Processor(x[i]))

    method = {'utilization': Processor.initialize_utilization,
              'activity': Processor.initialize_activity,
              'stalled': Processor.initialize_stalled_state,
              'power_mW': Processor.initialize_power_mW,
              'input_buffers[0].num_writes': Processor.initialize_input_buffer_0_num_writes,
              'input_buffers[0].num_reads': Processor.initialize_input_buffer_0_num_reads,
              'input_buffers[1].num_writes': Processor.initialize_input_buffer_1_num_writes,
              'input_buffers[1].num_reads': Processor.initialize_input_buffer_1_num_reads}
    for i in range(1, len(lines)):
        data = lines[i].rstrip().split(' ')
        time = data[1]
        Processor.initialize_time_period_index_dic(time)
        method[data[0]](processor_obj_list, data, time)


def plot_processor(processor_obj_list,
                    processor_coordinate_file_loc,
                    ax):
    lines = tuple(open(processor_coordinate_file_loc, 'r'))
    patch_list = []

    # reading processor objects, and x and y coordinates 
    # for the lower left corner of the processor figure 
    for line in lines:
        data = line.rstrip().split(',')
        # initializing the processor object list based on their name  
        processor = processor_obj_list[Processor.processor_index_dic[data[0]]]
        patch_list += processor.map_processor_graph_object(data[2], data[1], ax)

    # returning the list of patches collected for the processor object
    return patch_list
