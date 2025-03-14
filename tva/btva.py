from tva.voting_schemes import *
from tva.happiness import compute_happiness, compute_sum_happiness
from tva.risk import compute_risk
from itertools import permutations

class BTVA:
    def __init__(self, scheme):
        self.scheme = scheme

    def compute_winner(self, preferences):
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

        return sorted(winners)[0] if len(winners) > 1 else winners[0]

    def apply_strategic_voting(self, preferences, true_preferences):
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

    def _strategic_update(self, profile, true_preferences, voter_index):
        current_outcome = self.compute_winner(profile)
        current_happiness_scores = compute_happiness(true_preferences, current_outcome)
        voter_orig_happiness = current_happiness_scores[voter_index]
        
        best_perm = None
        best_new_happiness = voter_orig_happiness

        print(f"\nEvaluating strategic options for Voter {voter_index+1}:")
        print(f"Current ballot: {profile[voter_index]}")
        print(f"Current outcome: {current_outcome} with happiness {voter_orig_happiness}")
        
        for perm in permutations(profile[voter_index]):
            perm_list = list(perm)
            if perm_list == profile[voter_index]:
                continue 
            
            temp_profile = [list(row) for row in profile]
            temp_profile[voter_index] = perm_list
            outcome_temp = self.compute_winner(temp_profile)
            new_happiness_scores = compute_happiness(true_preferences, outcome_temp)
            new_happiness = new_happiness_scores[voter_index]
            
            if new_happiness > best_new_happiness:
                best_new_happiness = new_happiness
                best_perm = perm_list
        
        if best_perm is not None:
            print(f"Beneficial change found for Voter {voter_index+1}!")
            print(f"New ballot: {best_perm} with happiness {best_new_happiness}")
            return best_perm
        else:
            print(f"No beneficial change for Voter {voter_index+1}. Keeping original ballot.")
            return profile[voter_index]

    def apply_counter_strategic_voting(self, preferences, true_preferences):
        current_matrix = [list(row) for row in preferences]  # deep copy of honest preferences
        total_changes = 0
        num_voters = len(current_matrix)

        print("\nStarting iterative exclusion-inclusion counter strategic voting...\n")
        for i in range(num_voters):
            print(f"\n--- Iteration: Excluding Voter {i+1} ---")
            # Step 1: For every voter except voter i, update their vote strategically.
            for j in range(num_voters):
                if j == i:
                    continue
                new_order = self._strategic_update(current_matrix, true_preferences, j)
                if new_order != current_matrix[j]:
                    print(f"Voter {j+1} updates ballot from {current_matrix[j]} to {new_order}.")
                    current_matrix[j] = new_order

            print("\nMatrix after updating all voters except Voter", i+1)
            for idx, ballot in enumerate(current_matrix):
                print(f"Voter {idx+1}: {ballot}")
            
            # Step 2: Allow the excluded voter i to update his ballot on the updated matrix.
            new_order_excluded = self._strategic_update(current_matrix, true_preferences, i)
            if new_order_excluded != current_matrix[i]:
                print(f"Voter {i+1} (excluded earlier) now updates ballot from {current_matrix[i]} to {new_order_excluded}.")
                current_matrix[i] = new_order_excluded
                total_changes += 1
            else:
                print(f"Voter {i+1} makes no counter update; ballot remains {current_matrix[i]}.")

            current_outcome = self.compute_winner(current_matrix)
            current_total_happiness = compute_sum_happiness(compute_happiness(true_preferences, current_outcome))
            print(f"\nAfter iteration {i+1}:")
            print("Current updated matrix:")
            for idx, ballot in enumerate(current_matrix):
                print(f"  Voter {idx+1}: {ballot}")
            print(f"Current outcome: {current_outcome}")
            print(f"Current total happiness: {current_total_happiness}\n")
        
        return current_matrix, total_changes

    def analyse(self, preferences, counter_voting=True):
        initial_outcome = self.compute_winner(preferences)
        initial_happiness_scores = compute_happiness(preferences, initial_outcome)
        risk = compute_risk(preferences, initial_outcome)

        true_preferences = [list(p) for p in preferences]

        if counter_voting:
            final_matrix, total_changes = self.apply_counter_strategic_voting(preferences, true_preferences)
            return initial_outcome, initial_happiness_scores, risk, final_matrix, total_changes
        else:
            self.apply_strategic_voting(preferences, true_preferences)
            return initial_outcome, initial_happiness_scores, risk
