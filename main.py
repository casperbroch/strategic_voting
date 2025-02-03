from tva.btva import BTVA
from tva.happiness import compute_sum_happiness

def main():
    preferences = [
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "C", "A"],
        ["C", "A", "B"],
        ["A", "B", "C"]
    ]
    btva = BTVA(scheme="plurality")
    
    outcome, happiness_scores = btva.analyse(preferences)
    sum_happiness = compute_sum_happiness(happiness_scores)
    
    print(f"Voting Outcome: {outcome}")
    print(f"Happiness Levels per User: {happiness_scores}")
    print(f"Sum of Happiness: {sum_happiness}")



if __name__ == "__main__":
    main()