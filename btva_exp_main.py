import random
import copy
from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def voting_scheme(preferences):
    vote_count = {}
    for pref in preferences:
        top = pref[0]
        vote_count[top] = vote_count.get(top, 0) + 1
    max_votes = max(vote_count.values())
    winners = [cand for cand, count in vote_count.items() if count == max_votes]
    winners.sort()
    return winners[0]

def compute_happiness(true_preferences, outcome):
    happiness_scores = []
    for pref in true_preferences:
        if outcome in pref:
            rank = pref.index(outcome)
            happiness = len(pref) - rank
        else:
            happiness = 0
        happiness_scores.append(happiness)
    return happiness_scores

def apply_strategic_voting(preferences, true_preferences):
    new_preferences = copy.deepcopy(preferences)
    num_voters = len(new_preferences)
    
    current_outcome = voting_scheme(new_preferences)
    current_happiness = compute_happiness(true_preferences, current_outcome)
    
    changes = 0
    for v in range(num_voters):
        original_ranking = new_preferences[v]
        original_happiness = current_happiness[v]
        
        best_perm = None
        best_gain = 0
        
        for perm in permutations(original_ranking):
            perm_list = list(perm)
            if perm_list == original_ranking:
                continue
            
            trial_prefs = copy.deepcopy(new_preferences)
            trial_prefs[v] = perm_list
            
            outcome = voting_scheme(trial_prefs)
            new_happiness = compute_happiness(true_preferences, outcome)
            
            gain = new_happiness[v] - original_happiness
            if gain > best_gain:
                best_gain = gain
                best_perm = perm_list
        
        if best_perm is not None:
            new_preferences[v] = best_perm
            changes += 1
            current_outcome = voting_scheme(new_preferences)
            current_happiness = compute_happiness(true_preferences, current_outcome)
    
    return new_preferences, changes

def experiment_vary_voters(voter_list, fixed_N, trials=5, seed=None):
    if seed is not None:
        random.seed(seed)
    
    abs_changes = []
    frac_changes = []
    
    for M in voter_list:
        scenario_changes = []
        for _ in tqdm(range(trials), desc=f"Varying voters: M={M}", leave=False):
            candidates = [chr(ord('A') + i) for i in range(fixed_N)]
            preferences = []
            for __ in range(M):
                c = candidates[:]
                random.shuffle(c)
                preferences.append(c)
            
            true_prefs = copy.deepcopy(preferences)
            _, changes = apply_strategic_voting(preferences, true_prefs)
            scenario_changes.append(changes)
        
        avg_abs = np.mean(scenario_changes)
        abs_changes.append(avg_abs)
        frac_changes.append(avg_abs / M)
    
    return abs_changes, frac_changes

def experiment_vary_candidates(candidate_list, fixed_M, trials=5, seed=None):
    if seed is not None:
        random.seed(seed)
    
    abs_changes = []
    frac_changes = []
    
    for N in candidate_list:
        scenario_changes = []
        for _ in tqdm(range(trials), desc=f"Varying candidates: N={N}", leave=False):
            candidates = [chr(ord('A') + i) for i in range(N)]
            preferences = []
            for __ in range(fixed_M):
                c = candidates[:]
                random.shuffle(c)
                preferences.append(c)
            
            true_prefs = copy.deepcopy(preferences)
            _, changes = apply_strategic_voting(preferences, true_prefs)
            scenario_changes.append(changes)
        
        avg_abs = np.mean(scenario_changes)
        abs_changes.append(avg_abs)
        frac_changes.append(avg_abs / fixed_M)
    
    return abs_changes, frac_changes

if __name__ == "__main__":
    voter_list = [5, 10, 20, 30, 40] 
    fixed_N_for_expA = 3             
    trials_for_expA = 10              
    
    # Run Experiment A
    print("Running Experiment A (Vary M, fixed N=3)...")
    abs_changes_A, frac_changes_A = experiment_vary_voters(
        voter_list, 
        fixed_N_for_expA, 
        trials=trials_for_expA,
        seed=42
    )
    
    import matplotlib.pyplot as plt
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].plot(voter_list, abs_changes_A, marker='o', color='b')
    axs[0].set_xlabel("Number of Voters (M)")
    axs[0].set_ylabel("Avg # of Strategic Changes (Absolute)")
    axs[0].set_title("Experiment A: Absolute Changes vs. M")
    axs[0].grid(True)
    
    axs[1].plot(voter_list, frac_changes_A, marker='o', color='g')
    axs[1].set_xlabel("Number of Voters (M)")
    axs[1].set_ylabel("Avg Fraction of Voters Changing")
    axs[1].set_title("Experiment A: Fraction of Changes vs. M")
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()
    

    candidate_list = [3, 4, 5, 6, 7] 
    fixed_M_for_expB = 10       
    trials_for_expB = 8         
    
    # Run Experiment B
    print("\nRunning Experiment B (Vary N, fixed M=10)...")
    abs_changes_B, frac_changes_B = experiment_vary_candidates(
        candidate_list,
        fixed_M_for_expB,
        trials=trials_for_expB,
        seed=42
    )
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].plot(candidate_list, abs_changes_B, marker='o', color='b')
    axs[0].set_xlabel("Number of Candidates (N)")
    axs[0].set_ylabel("Avg # of Strategic Changes (Absolute)")
    axs[0].set_title("Experiment B: Absolute Changes vs. N")
    axs[0].grid(True)
    
    axs[1].plot(candidate_list, frac_changes_B, marker='o', color='g')
    axs[1].set_xlabel("Number of Candidates (N)")
    axs[1].set_ylabel("Avg Fraction of Voters Changing")
    axs[1].set_title("Experiment B: Fraction of Changes vs. N")
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()