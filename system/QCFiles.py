import os
from data.QCManager import FastQC
from data.QCManager import FastQCDataPoint


def get_fastqc_array(dir):
    arr = []
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            arr.append(FastQC(os.path.join(dir, filename)))
    return arr


qc = get_fastqc_array("C:\\Users\\shikd\\Google Drive\\ByteSize\\20170712\\extracted")

qc_list = FastQCDataPoint(qc)

print(qc_list.report)
qc_list.report.to_csv("extracted.csv")
