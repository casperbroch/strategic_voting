import math

def compute_happiness(preferences, outcome):
    happiness_scores = {}

    for i, voter_pref in enumerate(preferences):
        rank = voter_pref.index(outcome)
        happiness_scores[i] = len(voter_pref) - rank
    
    return happiness_scores

def compute_sum_happiness(happiness_scores):
    valid_scores = [score for score in happiness_scores.values() if not math.isnan(score)]
    
    if not valid_scores:
        return math.nan
    
    return sum(valid_scores)