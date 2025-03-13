import math
from tva.voting_schemes import plurality_voting
from itertools import combinations

def compute_risk(preferences, outcome):
    original_winner = outcome
    num_voters = len(preferences)

    # Prioritize voters who currently rank the winner highest (they are the most impactful)
    voter_priority = sorted(
        range(num_voters),
        key=lambda v: preferences[v].index(original_winner) if original_winner in preferences[v] else math.inf
    )

    MAX_RISK_THRESHOLD = int(0.1 * num_voters)  # Max 10% of voters considered for change

    for k in range(1, min(MAX_RISK_THRESHOLD, num_voters) + 1):
            #print(f"Checking {k}-voter combinations...")

        for voters_to_change in combinations(voter_priority, k):
            backup_prefs = [preferences[v][:] for v in voters_to_change]

            # Remove the original winner from preferences safely
            for voter in voters_to_change:
                if original_winner in preferences[voter]:  # Check before removing
                    preferences[voter].remove(original_winner)

            # Ensure no empty lists are passed to plurality_voting
            filtered_prefs = [v for v in preferences if v]

            if not filtered_prefs:  # If all lists are empty, skip
                continue

            new_outcome = plurality_voting(filtered_prefs)

            # Restore preferences to original state
            for idx, voter in enumerate(voters_to_change):
                preferences[voter] = backup_prefs[idx]

            # Handle cases where no clear winner is found
            if len(new_outcome) != 1:
                continue
            else:
                new_outcome = new_outcome[0]

            # If changing these k voters changes the winner, return k as risk measure
            if new_outcome != original_winner:
                return k

    return MAX_RISK_THRESHOLD # If no change in outcome is found, risk is infinite
