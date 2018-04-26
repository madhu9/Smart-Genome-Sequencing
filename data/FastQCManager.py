from data.FastQCParser import FastQCParser
from data import QCQuantifier as score

class FastQC:
    def __init__(self, file_loc):
        self.data = FastQCParser(file_loc)
        self.summary = dict()
        self.__quantify()

    def __quantify(self):
        self.summary["pbsq"] = score.pbsq(self.data.modules["pbsq"])
        self.summary["psqs"] = score.psqs(self.data.modules["psqs"])
        self.summary["pbsc"] = score.pbsc(self.data.modules["pbsc"])
        self.summary["psgc"] = score.psgc(self.data.modules["psgc"])
        self.summary["pbnc"] = score.pbnc(self.data.modules["pbnc"])
        self.summary["sld"] = score.sld(self.data.modules["sld"])
        self.summary["ac"] = score.ac(self.data.modules["ac"])
