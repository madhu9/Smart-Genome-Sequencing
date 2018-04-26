def pbsq(data, min_q_score = 30, col_index="Lower Quartile"):
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
        score += __score_pbsq(current_data, prev_data)
        print(score)
    return score


def __score_pbsq(current_data, prev_data):
    return 1 / abs((current_data - prev_data) / 2 + 1)


def psqs(data, majoritiy_score):
    """
    Score Per Sequence Quality Score
    :param data: Pandas DataFrame of PSQS
    :param majoritiy_score: What should majority of the scores be
    :return: Score received by PSQS
    """
    # Majority of reads should have q score above 30
    # We can calculate percent area above 30 vs total area
    # Get the cutoff by statistical analysis of all data and determine optimal percent cutoff value
    return None


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
    return None


def sld(data, percent_same_length):
    """
    Score SLD
    :param data: Pandas Dataframe of SLD
    :param percent_same_length: What percentage of length distribution should be the same length
    :return: Score
    """
    # Most point should be the same length
    # Can be parsed from fastq file
    return None


def ac(data):
    """
    Check Adapter Content
    :param data: AC Pandas DataFrame
    :return: 0 or 1 weather if fails or passes
    """
    # Pass if everything is 0
    # Fail if Exponential Line
    return None
