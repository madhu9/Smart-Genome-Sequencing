from data.QCParser import FastQCParser
from data import QCQuantifier as score
import pandas as pd
import os


class FastQC:
    def __init__(self, file_loc):
        if os.path.exists(file_loc):
            self.data = FastQCParser(file_loc)
            self.file = self.data.modules['bs'].loc['Filename'].values[0]
            self.summary = dict()
            self.__quantify()

    def __quantify(self):
        self.summary["pbsq"] = score.pbsq(self.data.modules["pbsq"])['score']
        self.summary["psqs"] = score.psqs(self.data.modules["psqs"])
        self.summary["pbsc"] = score.pbsc(self.data.modules["pbsc"])['avg_error']
        # self.summary["psgc"] = score.psgc(self.data.modules["psgc"]) # TODO: Implement this later
        self.summary["pbnc"] = score.pbnc(self.data.modules["pbnc"])
        self.summary["sld"] = score.sld(self.data.modules["sld"])
        self.summary["ac"] = score.ac(self.data.modules["ac"])


class FastQCPair:
    def __init__(self, forward, reverse):
        self.forward = forward
        self.reverse = reverse
        # TODO: Figure out how these two files relates to each other


class FastQCDataPoint:
    def __init__(self, qc_array):
        self.qc_array = qc_array
        index, summary = self.get_summary_report()
        self.report = pd.DataFrame(summary, index=index)

    def get_summary_report(self):
        index = []
        summary = []
        for qc in self.qc_array:
            summary.append(qc.summary)
            index.append(qc.file)
        return index, summary

    def export_report(self, location):
        self.report.to_csv(location)
