import numpy as np

from tva.btva import BTVA
from tva.risk import compute_risk
from tva.happiness import compute_happiness, compute_sum_happiness
from tva.voting_schemes import *
from tva.strategies import switch_ranking, bullet_voting_vectors
from tva.generate_situation import generate_preferences

class ATVA4(BTVA):
    def __init__(self, scheme, strategy=None, k=np.inf):
        super().__init__(scheme)
        self.strategy = strategy
        self.k = k

    def apply_strategy(self, old_preferences):
        preferences = old_preferences.copy()
        if self.strategy == "compromising_burying":
            return switch_ranking(preferences, self.k)
        elif self.strategy == "bullet_voting":
            return bullet_voting_vectors(preferences, self.scheme, self.k)
        else:
            return preferences

    def analyse(self, preferences):
        M = len(preferences[0])

        if self.strategy == 'compromising_burying':
            new_preferences, changed_idx = switch_ranking(preferences, self.k)
            if self.scheme == "plurality":
                winners = plurality_voting(new_preferences)
            elif self.scheme == "voting2":
                winners = winners_voting_vectors(convert_to_votingfor2(new_preferences, M))
            elif self.scheme == "antiplurality":
                winners = winners_voting_vectors(convert_to_antiplurality(new_preferences, M))
            elif self.scheme == "borda":
                winners = winners_voting_vectors(convert_to_borda(new_preferences, M))
        
        elif self.strategy == 'bullet_voting':
            voting_vectors, changed_idx = bullet_voting_vectors(preferences, self.scheme, self.k)
            winners = winners_voting_vectors(voting_vectors)
            
        if len(winners) > 1:
            outcome = sorted(winners)[0]

        elif len(winners) == 1:
            outcome = winners[0]
        else:
            outcome = f"no winner found"
        
        happiness_scores = compute_happiness(preferences, outcome)
        risk = compute_risk(preferences, outcome, scheme=self.scheme)


        return (outcome, happiness_scores, risk), changed_idx
            

def experiments(M, N, scheme, strategy, k):
    initial_preferences = generate_preferences(M, N)
    btva = BTVA(scheme=scheme)
    _, initial_happiness_scores, initial_risk = btva.analyse(initial_preferences)
    preferences = initial_preferences.copy()
    atva4 = ATVA4(scheme=scheme, strategy=strategy, k=k)
    (_, happiness_scores, risk), _ = atva4.analyse(preferences)
    
    deltas = [happiness_scores[i] - initial_happiness_scores[i] for i in happiness_scores.keys()]
    return np.array(deltas), sum(deltas), risk - initial_risk