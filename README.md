# Core Visualizer
This application is used for visualizing the runtime data from the Kilocore processor to analyze the application algorithm structure. It visualized the input and output buffers of a core as well as Activity, Utilization, Stalled State and Power which gives the user essential information about the runtime efficiency on the Kilocore processor.

## Environment 

Ubuntu 16.04 

## Installing dependencies 

Just go to your project folder in the terminal and run the install-deps.sh like following. You might need to enter your password to run the sudo commands. 

`./install-deps.sh`

The script might not have execute permissions. For that run the command below and rerun the install-deps scripts: 

`chmod 700 install-deps.sh`

## Running the project 

You can run the project by using the run.sh script as follows: 

`./run.sh`

The script might not have execute permissions. For that run the command below and rerun the run scripts: 

`chmod 700 run.sh`

## Processor Map

The processor map is used to visualize the buffer and stalled state of the graph. The user can use prev and next buttons to jump to the next time and the processor map will be updated accordingly. 

## Processor Graphs 

The processor graphs are used to visualize Activity, Utilization, Stalled State and Power of individual processor. The user can simply click on a processor on the processor map and the processor garphs will be updated accordingly. The red marker on the processor graphs indicates the current timestep of the processor map. The user can adjust the time range to look at the specific portion of the processor graphs. 

## Toolbar

* Prev: The user can jump to the previous time step using this button 
* Next: The user can jump to the next time step using this button 
* Step Size: The user can change the timestep jump size using this button. Hence, the user can control size of time steps when they use prev or next buttons.
* Time Range: Here the user can define the time range for the graphs so that the user can look at the specific portions of the graphs in more detail. 

## Setting.xml 

### project_title

You can change the process title as per your need in the settings.xml. This will be reflected on the GUI. 

### data_recorder_out_file_loc

Here you need to define the location of the data recorder out file that contains information about the input and output buffers of a core as well as Activity, Utilization, Stalled State and Power.  

### processor_coordinate_file_loc

Here you need to define the location of the user generated file that contains the information about the position of every individual processor on the processor map. It contains the coordinate of the lower left corner on the each processor to be specific. You can look at the sample processor coordinate file in the settings folder. 

### graph_settings

* number of graphs: The user need to define the number of the graph that they require 
* id: The user need to assign a unique integar ID to each graph 
* x_label: The user need to define the x label for the graph 
* y_label: The user need to define the y label for the graph 
* data field: The user need to define the data field so the application can access appropriate data from teh data recorder out file to create graphs 
* scale factor: The user need to manually define the scale factor for each graph so that it perfectly fits in the figure. Scale factor can defined as a value which when multiple to the maximum value in the dataset that need to be graphs, the result is no greater than 2.5. 

### processor_obj_setting 

* max_buffer_size: The user must provide the max buffer value among all the processors for visualization purposes. 
* processor_size: The user can customized the size of the processors in the processor map using this field.
* stalled_state_radius: The user can customize the size of the circle that repsents the stalled state of processors on processor map using this field. 

### gui_settings 

You can use the GUI settings to define the initial time steps size for the application.

## Contributor 
* Sarvagya Singh (sarvagya.vatsal@gmail.com, sarsing@ucdavis.edu)