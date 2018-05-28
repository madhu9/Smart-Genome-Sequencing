import os
from data.QCManager import FastQC
from data.QCManager import FastQCPair


def get_fastqc_pair_dict(dir):
    """
    Get matching forward and reverse filename location
    :param dir: Location of all QC files
    :return: (dict)Dictionary of each unique sequence filename and their (FastQCPair)paired file
    """
    qc_pair = dict()
    unique_qc = __get_unique_qc(dir)
    for qc in unique_qc:
        forward, reverse = __get_fastqc_pair(qc)
        qc_pair[qc[qc.rindex('\\') + 1:]] = FastQCPair(forward, reverse)
    return qc_pair


def get_fastqc_array(dir):
    """
    Returns an array of QC files given it's directory
    :param dir: Location of all QC files
    :return: (Array) QC Files
    """
    qc_array = []
    unique_qc = __get_unique_qc(dir)
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            file_loc = os.path.join(dir, filename)
            qc_array.append(FastQC(file_loc))
    return qc_array


def __get_unique_qc(dir):
    """
    Given a directory, returns all the unique qc files (excluding the forward and the reverse prefix)
    :param dir: Location of the directory
    :return: (Set)All unique QC file location
    """
    unique_qc = set()
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            formatted_file_name = filename[:-18]
            unique_qc.add(dir + "\\" + formatted_file_name)
    return unique_qc


def __get_qc_pairs_name(unique_qc_name):
    """
    Given an unique qc file, returns the forward and reverse filename
    :param unique_qc_name: unique filename
    :return: Tuple of (String)forward and (String)reverse file name
    """
    return unique_qc_name + '_R1_001_fastqc.txt', unique_qc_name + '_R2_001_fastqc.txt'


def __get_fastqc_pair(unique_qc_name):
    """
    Given an unique fastqc name, returns it's forward and reverse FastQC
    :param unique_qc_name: Unique qc name
    :return: (tuple)(FastQC)Forward, (FastQC)Reverse. Value of None indicates Path doesn't exists
    """
    forward, reverse = __get_qc_pairs_name(unique_qc_name)
    forward_qc = FastQC(forward) if os.path.exists(forward) else None
    reverse_qc = FastQC(reverse) if os.path.exists(forward) else None
    return forward_qc, reverse_qc


def extract_results(file_loc):
    return None


class ReportDatabase:
    def __init__(self, file_loc):
        self.file_loc = file_loc

    @staticmethod
    def __create_entry_id(entry):
        """
        Given a database entry with WGSID, MiSeq and Date, extract the filename prefix for entry
        :return:
        """
        try:
            file = entry['WGSID'] + '-NYC-' + entry['MISeq'] + '-' + ReportDatabase.__get_reformatted_date(entry['Date'])
        except AttributeError:
            print("Missing Data")
        return file

    @staticmethod
    def __get_reformatted_date(date):
        date = date.split('/')
        if date[0] == 1:
            date[0] = '0' + date[0]
        return date[2] + date[0] + date[1]
