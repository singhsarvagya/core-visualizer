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