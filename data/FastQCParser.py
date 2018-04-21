import pandas as pd
from io import StringIO


class FastQCParser:
    def __init__(self, file_loc=""):
        """
        Initialize a FastQCParser
        :param file_loc: location of where the file exists
        """
        self.modules = dict()
        self.file_loc = file_loc
        self.set_location(self.file_loc)

    def set_location(self, file_loc):
        """
        Set the location of where the file exists This will update the module as well
        :param file_loc: string location of the file
        """
        self.file_loc = file_loc
        self.__update_module()

    def __update_module(self):
        self.modules = FastQCParser.__extract_modules(self.file_loc)
        FastQCParser.__str_dict_to_df(self.modules)

    @staticmethod
    def __str_dict_to_df(module):
        for key, val in module.items():
            if val is not "":
                module[key] = pd.read_csv(StringIO(val), sep="\t", index_col=0)

    @staticmethod
    def __extract_modules(file_loc):
        modules = dict()
        section = ""
        with open(file_loc, 'r') as f:
            line = f.readline()
            is_in_section = False
            section = ""
            while line:
                if line[0:2] == ">>":
                    is_in_section = not is_in_section
                    if is_in_section:
                        section = FastQCParser.__extract_name(line)
                        modules[section] = ""
                elif is_in_section:
                    modules[section] += line
                line = f.readline()
        return modules

    @staticmethod
    def __extract_name(line):
        line = line.split(" ")
        name = line[0][2:3]
        for index in range(1, len(line)):
            name += line[index][0]
        return name.upper()
