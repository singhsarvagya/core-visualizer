from processor_obj_file import Processor
# TODO get this data from the setting 
total_processors = 100
# data_recoder_out_file = "sample_data/data_recorder_out.txt"
# processor_coordinate_file = "settings/processor_coordinate.csv"

# TODO move this function to core visullizer 
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

    for i in range(1, len(lines)):
        data = lines[i].rstrip().split(' ')
        time = data[1]
        Processor.initialize_time_period_list(time)
        Processor.register_processor_data(processor_obj_list, data)

# TODO move this file to figures 
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
