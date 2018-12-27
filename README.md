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

## Processor Graphs 

## Toolbar

* Prev 
* Next 
* Step Size 
* Time Range 

## Setting.xml 

### Project Title 

You can change the process title as per your need in the settings.xml. This will be reflected in the GUI. 

### data_recorder_out_file_loc

Here you need to define the location of the data recorder out file that contains information about the input and output buffers of a core as well as Activity, Utilization, Stalled State and Power.  

### processor_coordinate_file_loc

Here you need to define the location of the user generated file that contains the information about the position of every individual processor on the processor map. It contains the coordinate of the lower left corner on the each processor to be specific. You can look at the sample processor coordinate file in the settings folder. 

### graph_settings
### processor_obj_setting 
### gui_settings 

You can use the GUI settings to define the initial time steps size for the application.

## Contributor 
* Sarvagya Singh (sarvagya.vatsal@gmail.com)