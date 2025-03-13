import math

def compute_happiness(preferences, outcome, num_parties):
    happiness_scores = {}

    for i, voter_pref in enumerate(preferences):
        if voter_pref[0] == outcome:
             happiness_scores[i] = 1
        else: 
            happiness_scores[i] = 0

    return happiness_scores

def compute_sum_happiness(happiness_scores):
    valid_scores = [score for score in happiness_scores.values() if not math.isnan(score)]
    
    if not valid_scores:
        return math.nan
    
    return sum(valid_scores)