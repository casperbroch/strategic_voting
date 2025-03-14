from tva.voting_schemes import *
from tva.happiness import compute_happiness, compute_sum_happiness
from tva.risk import compute_risk
from itertools import permutations

class BTVA:
    def __init__(self, scheme):
        self.scheme = scheme

    def compute_winner(self, preferences):
        """Computes the winner based on the selected voting scheme."""
        if self.scheme == "plurality":
            winners = plurality_voting(preferences)
        elif self.scheme == "voting2":
            winners = winners_voting_vectors(convert_to_votingfor2(preferences))
        elif self.scheme == "antiplurality":
            winners = winners_voting_vectors(convert_to_antiplurality(preferences))
        elif self.scheme == "borda":
            winners = winners_voting_vectors(convert_to_borda(preferences))
        else:
            raise ValueError("Unsupported voting scheme")

        # Resolve ties by lexicographic order
        return sorted(winners)[0] if len(winners) > 1 else winners[0]

    def apply_strategic_voting(self, preferences, true_preferences):
        """
        For each voter (one at a time), try all possible alternative orderings (except the current one)
        and select the ordering that maximizes his personal happiness.
        """
        for i in range(len(preferences)):
            print(f"\nEvaluating strategic options for Voter {i+1}:")

            # Compute current outcome based on the selected voting scheme
            current_outcome = self.compute_winner(preferences)

            # Compute happiness using true preferences
            current_happiness_scores = compute_happiness(true_preferences, current_outcome)
            current_total_happiness = compute_sum_happiness(current_happiness_scores)
            voter_orig_happiness = current_happiness_scores[i]

            best_perm = None
            best_new_happiness = voter_orig_happiness
            best_new_total = current_total_happiness
            best_outcome = current_outcome

            # Evaluate all alternative orderings for voter i
            for perm in permutations(preferences[i]):
                if list(perm) == preferences[i]:
                    continue  # Skip if same as current vote

                # Create modified profile with voter i using the new ordering
                mod_preferences = preferences.copy()
                mod_preferences[i] = list(perm)

                # Compute new outcome using the same voting scheme
                outcome = self.compute_winner(mod_preferences)
                new_happiness_scores = compute_happiness(true_preferences, outcome)
                new_total = compute_sum_happiness(new_happiness_scores)

                # Check if this ordering increases the voter's happiness
                if new_happiness_scores[i] > best_new_happiness:
                    best_new_happiness = new_happiness_scores[i]
                    best_perm = list(perm)
                    best_new_total = new_total
                    best_outcome = outcome

            if best_perm is not None:
                preferences[i] = best_perm
                print("Strategic vote (ordering):", best_perm)
                print("New outcome:", best_outcome)
                print("New happiness score:", best_new_happiness)
                print("Original happiness score:", voter_orig_happiness)
                print("Original TOTAL happiness score:", current_total_happiness)
                print("New TOTAL happiness score:", best_new_total)
            else:
                print("No beneficial strategic vote found. Keeping original vote.")

    def analyse(self, preferences):
        outcome = self.compute_winner(preferences)
        happiness_scores = compute_happiness(preferences, outcome)
        risk = compute_risk(preferences, outcome)

        # Store original preferences before applying strategic voting
        true_preferences = [list(p) for p in preferences]

        self.apply_strategic_voting(preferences, true_preferences)

        return outcome, happiness_scores, risk
