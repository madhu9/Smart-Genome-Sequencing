import numpy as np


def pbsq(data, min_q_score=30, col_index="Lower Quartile"):
    """
    Score Per Base Sequence Quality from a Pandas Dataframe
    :param data: Pandas Dataframe containing PBSQ data
    :param min_q_score: Minimum Q score cut-off
    :return: A dictionary of (above-min) and (score)
    """
    # Look at the very last possible where lower quartile is above 30
    # if at least half way, plus some positive offset, module passes
    # Scoring System:
    # each base above 30, receives 1 / (abs(slope) + 1)
    base_above_min = 0
    score = 0
    for index in range(1, len(data)):
        current_row = data.iloc[index]
        prev_row = data.iloc[index - 1]
        current_data = current_row[[col_index]]
        current_data = current_data.values[0]
        if current_data < min_q_score:
            return {"percent-above-min": base_above_min/len(data)*100,
                    "score": score}
        prev_data = prev_row.loc[[col_index]]
        prev_data = prev_data.values[0]
        score += __score_pbsq_slope(current_data, prev_data)
        base_above_min += 1
    return {"percent-above-min": base_above_min/len(data)*100,
            "score": score}


def __score_pbsq_slope(current_data, prev_data):
    return 1 / (abs((current_data - prev_data)) / 2 + 1)


def psqs(data, min_required_score=30):
    """
    Percent of Scores Per Sequence Quality above min score
    :param data: Pandas DataFrame of PSQS
    :param min_required_score: What should majority of the scores be
    :return: percentage over majority_score
    """
    # Majority of reads should have q score above 30
    # We can calculate percent area above 30 vs total area
    # Get the cutoff by statistical analysis of all data and determine optimal percent cutoff value
    sum = data[min_required_score:].sum().values[0]
    return sum / data[:]['Count'].sum() * 100


def pbsc(data):
    """
    Score Per Base Sequence Content
    :param data: Pandas Dataframe
    :return: Score received by this module
    """
    # T and A should be very close
    ta_percent_error = []
    cg_percent_error = []
    for index, row in data.iterrows():
        expected_val = (row['T'] + row['A'])/2
        ta_percent_error.append(__get_percent_error(row['T'], expected_val))
        # C and G should be very close
        expected_val = (row['C'] + row['G'])/2
        cg_percent_error.append(__get_percent_error(row['C'], expected_val))
    ta_percent_error = np.array(ta_percent_error)
    cg_percent_error = np.array(cg_percent_error)
    ta_mean_error = ta_percent_error.mean()
    cg_mean_error = cg_percent_error.mean()
    return {"ta_error": ta_percent_error,
            "ta_mean_error": ta_percent_error,
            "cg_error": cg_percent_error,
            "cg_mean_error": cg_mean_error,
            "avg_error": (ta_mean_error + cg_mean_error)/2}


def __get_percent_error(calc_val, expected_val):
    return abs((expected_val - calc_val)/expected_val*100)


def psgc(data):
    """
    Per Sequence GC content
    :param data: PSGC Pandas DataFrame
    :return: Score of PSGC
    """
    # TODO: use machine learning
    return 0


def pbnc(data):
    """
    Score Per Base N Content
    :param data: Pandas Dataframe of PBNC
    :return: PBNC Score
    """
    score = 0
    # Area should be as close to 0 as possible
    # Closer to the front and back, higher the score
    # Spikes in the middle has lower score
    # TODO: Use different calculation for different part of the graph
    # center_data_percentage = 70
    # c_range_start = int((100 - center_data_percentage) / 2)
    # c_range_end = len(data) - int((100 - center_data_percentage) / 2)
    # Ranges in beginning, middle and end range
    # score = __pbnc_score_ends(data[0:c_range_start]) + \
    #        __pbnc_score_middle(data[c_range_start:c_range_end]) + \
    #        __pbnc_score_ends(data[c_range_end:])
    for index in range(len(data)):
        # TODO: Check through all data and make sure it's below 0
        if data.iloc[index].values[0] > 0:
            score += 1
    return score


def __pbnc_score_ends(data_series):
    # TODO: how the beginning and the end should be scored
    return 0


def __pbnc_score_middle(data_series):
    # TODO:  how the middle of the series should be scored
    return 0


def sld(data):
    """
    Score SLD
    :param data: Pandas Dataframe of SLD
    :return: Percentage of data of this length
    """
    # Most point should be the same length
    # Can be parsed from fastqc file
    mode = data['Count'].max()
    total = data['Count'].sum()
    # TODO: Return which length it is as well as the percent distribution
    return mode/total*100


def ac(data):
    """
    Check Adapter Content
    :param data: AC Pandas DataFrame
    :return: 0 or 1 weather if fails or passes
    """
    for column in data.columns:
        if data[column].max() > 1:
            return 0
    return 1
