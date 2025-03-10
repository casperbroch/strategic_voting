from tva.voting_schemes import *
from tva.happiness import compute_happiness
from tva.risk import compute_risk

class BTVA:
    def __init__(self, scheme):
        self.scheme = scheme

    def analyse(self, preferences):
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
            
        if len(winners) > 1:
            outcome = sorted(winners)[0]
            print(f"a tie has been detected between: {winners}, the winner: {outcome}")
        elif len(winners) == 1:
            outcome = winners[0]
        else:
            outcome = f"no winner found"
        
        happiness_scores = compute_happiness(preferences, winners)
        risk = compute_risk(preferences, winners)


        return outcome, happiness_scores, risk
