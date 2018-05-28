from data.QCParser import FastQCParser
from data import QCQuantifier as score
import pandas as pd
import os


class FastQC:
    def __init__(self, file_loc, database):
        """
        Creates a FastQC Object
        :param file_loc: File Location of where the FastQC.txt file is stored
        """
        try:
            self.data = FastQCParser(file_loc)
            self.file = self.data.modules['bs'].loc['Filename'].values[0]
            self.result = self.__get_sequence_result(database)
            self.summary = dict()
            self.__quantify()
        except FileNotFoundError:
            # TODO: Handle case for when file doesn't exists
            print("File doesn't exists")

    def __quantify(self):
        """
        Scores all the modules in the FastQC file
        :return:
        """
        self.summary["pbsq"] = score.pbsq(self.data.modules["pbsq"])['score']
        self.summary["psqs"] = score.psqs(self.data.modules["psqs"])
        self.summary["pbsc"] = score.pbsc(self.data.modules["pbsc"])['avg_error']
        # TODO: Implement PSQC using machine learning
        # self.summary["psgc"] = score.psgc(self.data.modules["psgc"])
        self.summary["pbnc"] = score.pbnc(self.data.modules["pbnc"])
        self.summary["sld"] = score.sld(self.data.modules["sld"])
        self.summary["ac"] = score.ac(self.data.modules["ac"])
        # TODO: Create an index for final outcome of the sequence

    def __get_sequence_result(self, database):
        """
        Given a database of QC results, extract current SQ result
        :param database: Pandas df which must contain WGSID, MISeq, and Date headers
        :return: Result stored in database for current sequence
        """
        filename = self.file[:self.file.index('_')].split('-')
        key_values = {
            'WGSID': filename[0],
            'MISeq': filename[2],
            'Date': filename[3]
        }
        entry = database
        for key, value in key_values.items():
            entry = entry[entry[key] == key_values[key]]
            if len(entry) == 1:
                break
        return entry['LocResult'].values[0], entry['CDCResult'].values[0]


class FastQCPair:
    def __init__(self, forward, reverse):
        """
        Creates a FastQC Pair Object
        :param forward: Forward File
        :param reverse: Reverse File
        """
        self.forward = forward
        self.reverse = reverse
        # TODO: Figure out how these two files relates to each other


class FastQCDataPoint:
    def __init__(self, qc_array):
        """
        Used to store all FastQC files and extract insights
        :param qc_array: List of all FastQC files
        """
        self.qc_array = qc_array
        index, summary = self.__get_summary_report()
        self.report = pd.DataFrame(summary, index=index)

    def __get_summary_report(self):
        """
        Summary of the current data points
        :return: (Tuple) [Array] FileName and [Array] Summary statistics
        """
        index = []
        summary = []
        for qc in self.qc_array:
            summary.append(qc.summary)
            index.append(qc.file)
        return index, summary

    def export_report(self, location):
        """
        Extracts current summary as a csv file
        :param location: Where the csv file will be extracted
        """
        self.report.to_csv(location)
