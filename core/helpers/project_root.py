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
            raise Exception("Cant't find setup.py.")

        else:
            return self.find_setup_file(os.path.split(os.path.abspath(os.path.normpath(f)))[0])

    def __str__(self)-> List[Union[str, bool]]:
        return self.path

    def get_path(self)-> List[Union[str, bool]]:
        return self.path
