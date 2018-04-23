from data.QCQuantifier import quantify as quantify
from data.FastQCParser import FastQCParser
import pandas as pd

class FastQC:
    def __init__(self, file_loc):
        self.parser = FastQCParser(file_loc)
        self.q_scores = pd.DataFrame()

    def quantify(self):
        self.qc_scores.loc["pbsq"] = quantify.pbsc(self.parser.modules["pbsq"])
        self.qc_scores.loc["psqs"] = quantify.psqs(self.parser.modules["psqs"])
        self.qc_scores.loc["pbsc"] = quantify.pbsc(self.parser.modules["pbsc"])
        self.qc_scores.loc["psgc"] = quantify.psqc(self.parser.modules["psqc"])
        self.qc_scores.loc["pbnc"] = quantify.pbnc(self.parser.modules["pbnc"])
        self.qc_scores.loc["sld"] = quantify.sld(self.parser.modules["sld"])
        self.qc_scores.loc["ac"] = quantify.ac(self.parser.modules["ac"])

    def export_summary(self, extract_location=""):
        """
        Export csv summary of each module and their q_scores
        """
        quantify()
        self.q_scores.to_csv(extract_location)