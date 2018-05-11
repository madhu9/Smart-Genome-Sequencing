import os
from data.QCManager import FastQC
from data.QCManager import  FastQCPair
from data.QCManager import FastQCDataPoint


def get_unique_qc(dir):
    unique_qc = set()
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            formatted_file_name = filename[:-18]
            unique_qc.add(dir + "\\" + formatted_file_name)
    return unique_qc


def get_fastqc_pair_array(dir):
    arr = dict()
    unique_qc = get_unique_qc(dir)
    for qc in unique_qc:
        forward, reverse = get_fastqc_pair(qc)
        arr[qc[qc.rindex('\\')+1:]] = FastQCPair(forward, reverse)
    return arr


def get_qc_pairs_name(unique_qc_name):
    return unique_qc_name + '_R1_001_fastqc.txt', unique_qc_name + '_R2_001_fastqc.txt'


def get_fastqc_pair(unique_qc_name):
    forward, reverse = get_qc_pairs_name(unique_qc_name)
    forward_qc = FastQC(forward) if os.path.exists(forward) else None
    reverse_qc = FastQC(reverse) if os.path.exists(forward) else None
    return forward, reverse


qc = get_fastqc_pair_array("C:\\Users\\shikd\\Google Drive\\ByteSize\\20170712\\extracted")


# qc_list = FastQCDataPoint(qc)
#
# print(qc_list.report)
# qc_list.report.to_csv("extracted.csv")