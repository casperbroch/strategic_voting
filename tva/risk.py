import math
from tva.voting_schemes import *
from itertools import combinations

def compute_risk(preferences, outcome, scheme='plurality'):
    original_winner = outcome
    num_voters = len(preferences)

    # Prioritize voters who currently rank the winner highest (they are the most impactful)
    voter_priority = sorted(
        range(num_voters), 
        key=lambda v: preferences[v].index(original_winner)
    )
    
    M = len(preferences[0])

    for k in range(1, num_voters + 1):
        print(f"Checking {k}-voter combinations...")

        for voters_to_change in combinations(voter_priority, k):
            backup_prefs = [preferences[v][:] for v in voters_to_change]

            for voter in voters_to_change:
                preferences[voter].remove(original_winner)

            if scheme == 'plurality':
                new_outcome = plurality_voting(preferences)
            elif scheme == 'voting2':
                new_outcome = winners_voting_vectors(convert_to_votingfor2(preferences, M))
            elif scheme == 'antiplurality': 
                new_outcome = winners_voting_vectors(convert_to_antiplurality(preferences, M))
            elif scheme == 'borda':
                new_outcome = winners_voting_vectors(convert_to_borda(preferences, M))
            else:
                raise ValueError("Unsupported voting scheme")
                

            for idx, voter in enumerate(voters_to_change):
                preferences[voter] = backup_prefs[idx]

            if len(new_outcome) != 1:
                continue
            else:
                new_outcome = new_outcome[0]

            if new_outcome != original_winner:
                return k 

    return math.inf 