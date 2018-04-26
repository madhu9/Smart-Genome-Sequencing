import os
from data.FastQCManager import FastQC


def get_fastqc_array(dir):
    arr = []
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            arr.append(FastQC(os.path.join(dir, filename)))
    return arr


qc = get_fastqc_array("C:\\Users\\shikd\\Google Drive\\ByteSize\\20170712\\extracted")

for qc in qc:
    print(qc.summary)
