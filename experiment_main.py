import random
import copy
from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import math

# -----------------------------
# Experiment 1: Varying Number of Voters (M) with fixed N
# -----------------------------
def strategic_vote_for_voter(profile, true_preferences, voter_index):
    current_outcome = voting_scheme(profile)
    current_happiness_scores = compute_happiness(true_preferences, current_outcome)
    voter_orig_happiness = current_happiness_scores[voter_index]

    best_perm = None
    best_new_happiness = voter_orig_happiness

    for perm in permutations(profile[voter_index]):
        perm_list = list(perm)
        if perm_list == profile[voter_index]:
            continue  # Skip the honest ordering

        temp_profile = copy.deepcopy(profile)
        temp_profile[voter_index] = perm_list
        outcome_temp = voting_scheme(temp_profile)
        new_happiness_scores = compute_happiness(true_preferences, outcome_temp)
        new_happiness = new_happiness_scores[voter_index]

        if new_happiness > best_new_happiness:
            best_new_happiness = new_happiness
            best_perm = perm_list

        return profile[voter_index]
    
def voting_scheme(preferences):
    vote_count = {}
    for pref in preferences:
        top = pref[0]
        vote_count[top] = vote_count.get(top, 0) + 1
    max_votes = max(vote_count.values())
    winners = [cand for cand, count in vote_count.items() if count == max_votes]
    winners.sort()
    return winners[0]

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


def iterative_counter_exclusion(honest_preferences, true_preferences):
    current_matrix = copy.deepcopy(honest_preferences)
    M = len(current_matrix)
    total_changes = 0

    for i in range(M):
        for j in range(M):
            if j == i:
                continue
            new_order = strategic_vote_for_voter(current_matrix, true_preferences, j)
            if new_order != current_matrix[j]:
                print(f"Voter {j} updates ballot from {current_matrix[j]} to {new_order}.")
                current_matrix[j] = new_order


        # Step 2: Allow the excluded voter i to update his ballot on the updated matrix.
        new_order_excluded = strategic_vote_for_voter(current_matrix, true_preferences, i)
        if new_order_excluded != current_matrix[i]:
            current_matrix[i] = new_order_excluded
            total_changes += 1


        current_outcome = voting_scheme(current_matrix)
        current_total_happiness = compute_sum_happiness(compute_happiness(true_preferences, current_outcome))

    return current_matrix, total_changes

def experiment_iterative_vary_voters(voter_list, fixed_N, trials=10, seed=None):
    if seed is not None:
        random.seed(seed)

    abs_updates = []
    frac_updates = []

    for M in voter_list:
        total_updates = 0
        for _ in tqdm(range(trials), desc=f"Varying voters: M={M}", leave=False):
            candidates = [chr(ord('A') + i) for i in range(fixed_N)]
            honest_preferences = []
            for _ in range(M):
                ballot = candidates[:]
                random.shuffle(ballot)
                honest_preferences.append(ballot)
            true_preferences = copy.deepcopy(honest_preferences)

            _, updates = iterative_counter_exclusion(honest_preferences, true_preferences)
            total_updates += updates
        avg_updates = total_updates / trials
        abs_updates.append(avg_updates)
        frac_updates.append(avg_updates / M)

    return abs_updates, frac_updates

# -----------------------------
# Experiment 2: Varying Number of Candidates (N) with fixed M
# -----------------------------

def experiment_iterative_vary_candidates(candidate_list, fixed_M, trials=8, seed=None):
    if seed is not None:
        random.seed(seed)

    abs_updates = []
    frac_updates = []

    for N in candidate_list:
        total_updates = 0
        for _ in tqdm(range(trials), desc=f"Varying candidates: N={N}", leave=False):
            candidates = [chr(ord('A') + i) for i in range(N)]
            honest_preferences = []
            for _ in range(fixed_M):
                ballot = candidates[:]
                random.shuffle(ballot)
                honest_preferences.append(ballot)
            true_preferences = copy.deepcopy(honest_preferences)

            _, updates = iterative_counter_exclusion(honest_preferences, true_preferences)
            total_updates += updates
        avg_updates = total_updates / trials
        abs_updates.append(avg_updates)
        frac_updates.append(avg_updates / fixed_M)

    return abs_updates, frac_updates

# -----------------------------
# Main: Run Experiments and Plot
# -----------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Experiment 1: Varying number of voters, fixed N = 3
    voter_list = [5, 10, 20, 30, 40]
    fixed_N_exp1 = 3
    trials_exp1 = 10
    abs_updates_voters, frac_updates_voters = experiment_iterative_vary_voters(voter_list, fixed_N_exp1, trials=trials_exp1, seed=42)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].plot(voter_list, abs_updates_voters, marker='o', color='b')
    axs[0].set_xlabel("Number of Voters (M)")
    axs[0].set_ylabel("Avg # of Updates (Absolute)")
    axs[0].set_title("Experiment 1: Absolute Updates vs. Voters")
    axs[0].grid(True)

    axs[1].plot(voter_list, frac_updates_voters, marker='o', color='g')
    axs[1].set_xlabel("Number of Voters (M)")
    axs[1].set_ylabel("Avg Fraction of Voters Updating")
    axs[1].set_title("Experiment 1: Fraction Updates vs. Voters")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

    # Experiment 2: Varying number of candidates, fixed M = 10
    candidate_list = [3, 4, 5, 6, 7]
    fixed_M_exp2 = 10
    trials_exp2 = 8
    abs_updates_candidates, frac_updates_candidates = experiment_iterative_vary_candidates(candidate_list, fixed_M_exp2, trials=trials_exp2, seed=42)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].plot(candidate_list, abs_updates_candidates, marker='o', color='b')
    axs[0].set_xlabel("Number of Candidates (N)")
    axs[0].set_ylabel("Avg # of Updates (Absolute)")
    axs[0].set_title("Experiment 2: Absolute Updates vs. Candidates")
    axs[0].grid(True)

    axs[1].plot(candidate_list, frac_updates_candidates, marker='o', color='g')
    axs[1].set_xlabel("Number of Candidates (N)")
    axs[1].set_ylabel("Avg Fraction of Voters Updating")
    axs[1].set_title("Experiment 2: Fraction Updates vs. Candidates")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()