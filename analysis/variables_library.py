SCORE_RANGES = {
    "phq9": {"min": 0, "max": 27},
    "gad7": {"min": 0, "max": 21},
}


def get_invalid_scores(score_events, questionnaire):
    score_range = SCORE_RANGES[questionnaire]
    return score_events.where(
        (score_events.numeric_value < score_range["min"])
        | (score_events.numeric_value > score_range["max"])
    )
