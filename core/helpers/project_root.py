import os
import sys

class ProjectRoot:
    #Finds the absolute project root path for Core. Must be called inside the project.

    def __init__(self):
        self.path = self.find_setup_file('.')

    def find_setup_file(self, f):
        ''' recursively sniff up the tree until setup.py is found.
            RETURNS: the parent folder for setup.py, or False if this is not a Core package.
        '''
        path = os.path.abspath(os.path.normpath(f))
        if os.path.isfile(os.path.abspath(os.path.normpath(path + os.path.sep + 'setup.py'))):
            return path
        elif path == '/':
            return False

        else: 
            return self.find_setup_file(os.path.split(os.path.abspath(os.path.normpath(f)))[0])           

    def __str__(self):
        return self.path

    def get_path(self):
        return self.path
    
