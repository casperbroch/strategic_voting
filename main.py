from tva.btva import BTVA
from tva.happiness import compute_average_happiness

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
    avg_happiness = compute_average_happiness(happiness_scores)
    
    print(f"Voting Outcome: {outcome}")
    print(f"Happiness Levels per User: {happiness_scores}")
    print(f"Average Happiness: {avg_happiness}")



if __name__ == "__main__":
    main()