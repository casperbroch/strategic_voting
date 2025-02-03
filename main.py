from tva.btva import BTVA

def main():
    preferences = [
        ["B", "B", "C"],
        ["A", "A", "C"],
        ["B", "C", "B"],
        ["C", "A", "B"],
        ["A", "B", "C"]
    ]
    btva = BTVA(scheme="plurality")
    
    outcome = btva.analyse(preferences)
    print(f"Voting Outcome: {outcome}")

if __name__ == "__main__":
    main()