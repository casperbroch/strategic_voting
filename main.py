from tva.btva import BTVA
from tva.happiness import compute_sum_happiness
from tva.generate_situation import generate_preferences

def main():
    M = 5  # Number of parties
    N = 10  # Number of users
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



if __name__ == "__main__":
    main()