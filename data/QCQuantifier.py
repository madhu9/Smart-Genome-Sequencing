def pbsq(data, min_q_score=30, col_index="Lower Quartile"):
    """
    Score Per Base Sequence Quality from a Pandas Dataframe
    :param data: Pandas Dataframe containing PBSQ data
    :param min_q_score: Minimum Q score cut-off
    :return: Score of the PBSQ module
    """
    # Look at the very last possible where lower quartile is above 30
    # if at least half way, plus some positive offset, module passes
    # Scoring System:
    # each base above 30, receives 1 / (abs(slope) + 1)
    base_above_q30 = 0
    score = 0
    for index in range(1, len(data)):
        current_row = data.iloc[index]
        prev_row = data.iloc[index - 1]
        current_data = current_row[[col_index]]
        current_data = current_data.values[0]
        if current_data < min_q_score:
            return score
        prev_data = prev_row.loc[[col_index]]
        prev_data = prev_data.values[0]
        score += __score_pbsq_slope(current_data, prev_data)
    return score


def __score_pbsq_slope(current_data, prev_data):
    return 1 / abs((current_data - prev_data) / 2 + 1)


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
    return data[min_required_score:].sum() / data[:]['Count'].sum() * 100


def pbsc(data):
    """
    Score Per Base Sequence Content
    :param data: Pandas Dataframe
    :return: Score received by this module
    """
    # T and A should be very close
    # C and G should be very close
    # T + A + C + G should be close to 100
    return None


def psgc(data):
    """
    Per Sequence GC content
    :param data: PSGC Pandas DataFrame
    :return: Score of SPGC
    """
    # use machine learning
    return None


def pbnc(data):
    """
    Score Per Base N Content
    :param data: Pandas Dataframe of PBNC
    :return: PBNC Score
    """
    # Area should be as close to 0 as possible
    # Closer to the front and back, higher the score
    # Spikes in the middle has lower score
    center_data_percentage = 70
    center_data_range = (int((100 - 70) / 2), len(data) - int((100 - 70) / 2))

    # ranges in beginning, middle and end range
    # TODO: figure out how to calculate __pbnc_score_ends and __pbnc_score_middle
    return __pbnc_score_ends(data[0:center_data_range[0]]) + \
           __pbnc_score_middle(data[center_data_percentage[0]:center_data_range[1]]) + \
           __pbnc_score_ends(data[center_data_range[1]:])


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
    :param percent_same_length: What percentage of length distribution should be the same length
    :return: Score (Mode Length, Percentage of data of this length)
    """
    # Most point should be the same length
    # Can be parsed from fastqc file
    mode = data['Count'].max()
    total = data['Count'].sum()
    return mode, mode/total*100


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
