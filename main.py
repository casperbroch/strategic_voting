import numpy as np
from tqdm import tqdm

from tva.btva import BTVA
from tva.happiness import compute_sum_happiness
from tva.generate_situation import generate_preferences
from tva.atva4 import experiments

def main():
    M = 5  # Number of parties
    N = 25  # Number of users
    preferences = generate_preferences(M, N)
    for i, prefs in enumerate(preferences):
        print(f"User {i+1} preference list: {prefs}")

    btva = BTVA(scheme="plurality")
    
    outcome, happiness_scores, risk = btva.analyse(preferences)

    sum_happiness = compute_sum_happiness(happiness_scores)
    
    print(f"Voting Outcome: {outcome}")
    print(f"Happiness Levels per User: {happiness_scores}")
    print(f"Sum of Happiness: {sum_happiness}")
    print(f"Risk: {risk}")

def main_test_ATVA4():
    M = 5  # Number of parties
    N = 25  # Number of users
    scheme = 'plurality'
    strategy = 'compromising_burying'

    for k in tqdm(range(1, N+1)):
        happiness_deltas = []
        risk_deltas = []
        max_user_delta = []
        min_user_delta = []
        for i in tqdm(range(20)):
                voter_deltas, happiness_delta, risk_delta = experiments(M, N, scheme, strategy, k)
                happiness_deltas.append(happiness_delta)
                risk_deltas.append(risk_delta)
                max_user_delta.append(max(voter_deltas))
                min_user_delta.append(min(voter_deltas))
    print("Overall Happiness Deltas: ", np.mean(happiness_deltas))
    print("Overall Risk Deltas: ", np.mean(risk_deltas))
    print("Overall Max User Deltas: ", np.mean(max_user_delta))
    print("Overall Min User Deltas: ", np.mean(min_user_delta))       


if __name__ == "__main__":
    main()