import os.path
import sys
from tkinter import messagebox
import xml.etree.ElementTree as ET


class Settings: 

	def __init__(self, settings_file): 

		# checking if the settings file exist 
		if not os.path.isfile(settings_file):
			messagebox.askokcancel("Error", "Settings file does not exist.") 
			sys.exit(0)

		self.tree = ET.parse(settings_file).getroot() 

	def get_project_title(self):
		# getting the project tile from the settings.xml  
		for atype in self.tree.findall('project_title'):
			return atype.get('value')
		return "Core Visualizer"

	def get_data_recorder_out_file_loc(self): 
		# getting the location of the data_recorder_out_file
		for atype in self.tree.findall('data_recorder_out_file_loc'):
			file_loc = atype.get('value')
			# checking if the data recorder file exists
			if not os.path.isfile(file_loc):
				messagebox.askokcancel("Error", "Data Recorder Out file does not exist.") 
				sys.exit(0)		
			return atype.get('value')

	def get_processor_coordinate_file_loc(self): 
		# getting the location of the processor_coordinate_file_loc
		for atype in self.tree.findall('processor_coordinate_file_loc'):
			file_loc = atype.get('value')
			# checking if the processor coordinate file exists
			if not os.path.isfile(file_loc):
				messagebox.askokcancel("Error", "Processor Coordinate file does not exist.") 
				sys.exit(0)		
			return atype.get('value')

	def get_graph_settings(self):
		# function returns the settings for the 
		# processor graphs 
		graph_settings = []

		# gathering all the graph objects from the xml 
		for graph in self.tree.iter('graph'):
			graph_settings.append( graph.attrib)

		# reordering the graph settings based on their id 
		graph_settings = sorted(graph_settings, key=lambda k: k['id'])
		
		return graph_settings

	def get_processor_object_settings(self): 
		# function to get settings for the processor map
		processor_object_settings = {}
		for field in self.tree.iter('processor_object_settings'):
			processor_object_settings = field.attrib

		return processor_object_settings

	def get_gui_settings(self): 
		# function to get the gui settings from the
		# settings.xml 
		gui_settings = {}
		for field in self.tree.iter('gui_settings'):
			gui_settings = field.attrib

		return gui_settings