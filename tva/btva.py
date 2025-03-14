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
        For each voter (one at a time), try all alternative orderings (except the current one)
        and select the ordering that maximizes his personal happiness.
        This is the original (non-counter) version.
        """
        for i in range(len(preferences)):
            print(f"\nEvaluating strategic options for Voter {i+1}:")
            current_outcome = self.compute_winner(preferences)
            current_happiness_scores = compute_happiness(true_preferences, current_outcome)
            current_total_happiness = compute_sum_happiness(current_happiness_scores)
            voter_orig_happiness = current_happiness_scores[i]

            best_perm = None
            best_new_happiness = voter_orig_happiness
            best_new_total = current_total_happiness
            best_outcome = current_outcome

            for perm in permutations(preferences[i]):
                if list(perm) == preferences[i]:
                    continue  # skip current ordering

                mod_preferences = preferences.copy()  # shallow copy; row i will be replaced
                mod_preferences[i] = list(perm)

                outcome = self.compute_winner(mod_preferences)
                new_happiness_scores = compute_happiness(true_preferences, outcome)
                new_total = compute_sum_happiness(new_happiness_scores)

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

    def apply_counter_strategic_voting(self, preferences, true_preferences):
        """
        Implements counter voting:
         - For each voter (as the excluded one), first update all other voters strategically,
           leaving the excluded voter’s vote unchanged.
         - Then, allow the excluded voter to try all alternative orderings on the updated profile.
         
        The method prints detailed output and returns a dictionary mapping each excluded voter
        index to the final profile, outcome, happiness scores, and total happiness.
        """
        num_voters = len(preferences)
        counter_results = {}
        for excluded in range(num_voters):
            print("\n" + "="*60)
            print(f"--- Experiment: Excluding Voter {excluded+1} Initially ---")
            # Create a fresh copy (deep copy of rows) of the honest preferences.
            mod_preferences = [list(row) for row in preferences]
            # For all voters except the excluded one, update their votes strategically.
            for voter in range(num_voters):
                if voter == excluded:
                    continue
                current_outcome = self.compute_winner(mod_preferences)
                current_happiness_scores = compute_happiness(true_preferences, current_outcome)
                current_total_happiness = compute_sum_happiness(current_happiness_scores)
                voter_orig_happiness = current_happiness_scores[voter]

                best_perm = None
                best_new_happiness = voter_orig_happiness
                best_new_total = current_total_happiness
                best_outcome = current_outcome

                for perm in permutations(mod_preferences[voter]):
                    if list(perm) == mod_preferences[voter]:
                        continue
                    trial_preferences = mod_preferences.copy()
                    trial_preferences[voter] = list(perm)
                    outcome = self.compute_winner(trial_preferences)
                    new_happiness_scores = compute_happiness(true_preferences, outcome)
                    new_total = compute_sum_happiness(new_happiness_scores)
                    if new_happiness_scores[voter] > best_new_happiness:
                        best_new_happiness = new_happiness_scores[voter]
                        best_perm = list(perm)
                        best_new_total = new_total
                        best_outcome = outcome

                if best_perm is not None:
                    mod_preferences[voter] = best_perm
                    print(f"\nVoter {voter+1}:")
                    print("Strategic vote (ordering):", best_perm)
                    print("New outcome:", best_outcome)
                    print("New happiness score:", best_new_happiness)
                    print("Original happiness score:", voter_orig_happiness)
                    print("Original TOTAL happiness score:", current_total_happiness)
                    print("New TOTAL happiness score:", best_new_total)
                else:
                    print(f"\nVoter {voter+1}: No beneficial strategic vote found. Keeping original vote.")

            # Now apply strategic voting for the excluded voter on the updated matrix.
            print(f"\nNow applying strategic voting for the excluded Voter {excluded+1} on the new matrix:")
            current_outcome = self.compute_winner(mod_preferences)
            current_happiness_scores = compute_happiness(true_preferences, current_outcome)
            current_total_happiness = compute_sum_happiness(current_happiness_scores)
            voter_orig_happiness = current_happiness_scores[excluded]

            best_perm = None
            best_new_happiness = voter_orig_happiness
            best_new_total = current_total_happiness
            best_outcome = current_outcome

            for perm in permutations(mod_preferences[excluded]):
                if list(perm) == mod_preferences[excluded]:
                    continue
                trial_preferences = mod_preferences.copy()
                trial_preferences[excluded] = list(perm)
                outcome = self.compute_winner(trial_preferences)
                new_happiness_scores = compute_happiness(true_preferences, outcome)
                new_total = compute_sum_happiness(new_happiness_scores)
                if new_happiness_scores[excluded] > best_new_happiness:
                    best_new_happiness = new_happiness_scores[excluded]
                    best_perm = list(perm)
                    best_new_total = new_total
                    best_outcome = outcome

            if best_perm is not None:
                mod_preferences[excluded] = best_perm
                print(f"\nVoter {excluded+1} strategic vote (ordering):", best_perm)
                print("New outcome:", best_outcome)
                print("New happiness score:", best_new_happiness)
                print("Original happiness score:", voter_orig_happiness)
                print("Original TOTAL happiness score:", current_total_happiness)
                print("New TOTAL happiness score:", best_new_total)
            else:
                print(f"\nVoter {excluded+1}: No beneficial strategic vote found. Keeping original vote.")

            # Final outcome after both rounds of strategic voting:
            final_outcome = self.compute_winner(mod_preferences)
            final_happiness_scores = compute_happiness(true_preferences, final_outcome)
            final_total_happiness = compute_sum_happiness(final_happiness_scores)
            print("\nFinal Matrix after applying strategic voting for all voters (including excluded Voter {0}):".format(excluded+1))
            for i, pref in enumerate(mod_preferences):
                print(f"Voter {i+1}: {pref}")
            print("\nFinal Outcome:", final_outcome)
            print("Final Happiness Scores (using true preferences):", final_happiness_scores)
            print("Final Total Happiness:", final_total_happiness)

            counter_results[excluded] = {
                "matrix": mod_preferences,
                "outcome": final_outcome,
                "happiness_scores": final_happiness_scores,
                "total_happiness": final_total_happiness
            }
        return counter_results

    def analyse(self, preferences, counter_voting=True):
        """
        Analyzes the voting situation.
         - First, computes the initial outcome, happiness scores, and risk.
         - Then, stores the true (honest) preferences.
         - Finally, applies either the regular strategic voting or counter strategic voting,
           based on the counter_voting flag.
           
        Returns a tuple containing the initial outcome, initial happiness scores, risk,
        and (if counter_voting is True) the counter voting results.
        """
        initial_outcome = self.compute_winner(preferences)
        initial_happiness_scores = compute_happiness(preferences, initial_outcome)
        risk = compute_risk(preferences, initial_outcome)

        # Store a copy of the honest preferences.
        true_preferences = [list(p) for p in preferences]

        if counter_voting:
            counter_results = self.apply_counter_strategic_voting(preferences, true_preferences)
            return initial_outcome, initial_happiness_scores, risk, counter_results
        else:
            self.apply_strategic_voting(preferences, true_preferences)
            return initial_outcome, initial_happiness_scores, risk
