
from typing import Union, List
import os
import sys

class ProjectRoot:
    # Finds the absolute project root path for Core. Must be called inside the project.

    def __init__(self) -> None:
        self.path = self.find_setup_file('.')

    def find_setup_file(self, f: str) -> List[Union[str, bool]]:
        ''' recursively sniff up the tree until setup.py is found.
            RETURNS: the parent folder for setup.py, or False if this is not a Core package.
        '''
        path = os.path.abspath(os.path.normpath(f))
        if os.path.isfile(os.path.abspath(os.path.normpath(path + os.path.sep + 'setup.py'))):
            return path
        elif path == '/':
            ## the airflow docker container is a special bird where /dags and the project root do not share parent paths
            if os.path.isfile('/usr/src/app/setup.py'):    
                return '/usr/src/app'
            else:
                raise Exception("Unable to determine project root: setup.py not found. Are you in Core?")

        else:
            return self.find_setup_file(os.path.split(os.path.abspath(os.path.normpath(f)))[0])

    def __str__(self)-> List[Union[str, bool]]:
        return self.path

    def get_path(self)-> List[Union[str, bool]]:
        return self.path
