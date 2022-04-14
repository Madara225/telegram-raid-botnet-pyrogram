import os
import inspect
import importlib.util

class MenuSettings:
	def __init__(self):
		
		self.menu_botnet = []
		for file in os.listdir('functions'):
			if file.endswith(".py"):
				
				name = file[:-3]
				path = 'functions'
				function = importlib.import_module(f'{path}.{name}')
				
				for classname, classobj in inspect.getmembers(function, inspect.isclass):
					all_classes = classobj.__module__
					
					if all_classes[:9] == path and classobj.__doc__ != None:
						if classobj in self.menu_botnet:
							continue
						else:
							self.menu_botnet.append(classobj)

					
