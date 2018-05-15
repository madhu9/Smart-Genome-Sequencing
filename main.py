from data.QCManager import FastQCDataPoint
import system.QCFiles as files


qc_loc = "C:\\Users\\shikd\\Google Drive\\ByteSize\\20170712\\extracted"
qc = files.get_fastqc_array(qc_loc)
qc_list = FastQCDataPoint(qc)

print(qc_list.report)
qc_list.report.to_csv("extracted.csv")
