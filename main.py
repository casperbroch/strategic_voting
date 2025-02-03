from tva.btva import BTVA

def main():
    preferences = [
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["A", "C", "B"],
        ["C", "A", "B"],
        ["A", "B", "C"]
    ]
    btva = BTVA(scheme="plurality")
    
    outcome = btva.analyse(preferences)
    print(f"Voting Outcome: {outcome}")

if __name__ == "__main__":
    main()