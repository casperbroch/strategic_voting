import math
from tva.voting_schemes import plurality_voting
from itertools import combinations

def compute_risk(preferences, outcome):
        
    if len(outcome) != 1:
        return math.inf
    else:
        outcome = outcome[0]
    
    original_winner = outcome
    num_voters = len(preferences)
    num_parties = len(preferences[0])
    
    for k in range(1, num_voters + 1):
        for voters_to_change in combinations(range(num_voters), k):
            modified_prefs = [list(pref) for pref in preferences]
            
            for voter in voters_to_change:
                modified_prefs[voter] = [c for c in modified_prefs[voter] if c != original_winner]
                if not modified_prefs[voter]:
                    continue
            new_outcome = plurality_voting(modified_prefs)

            if len(new_outcome) != 1:
                continue
            else:
                new_outcome = new_outcome[0]

            if new_outcome != original_winner:
                return k  
    
    return math.inf 