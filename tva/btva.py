from tva.voting_schemes import plurality_voting
from tva.happiness import compute_happiness
from tva.risk import compute_risk

class BTVA:
    def __init__(self, scheme):
        self.scheme = scheme

    def analyse(self, preferences):
        if self.scheme == "plurality":
            winners = plurality_voting(preferences)
            
            if len(winners) > 1:
                outcome = f"a tie has been detected between: {winners}"
            elif len(winners) == 1:
                outcome = plurality_voting(preferences)[0]
            else:
                outcome = f"no winner found"
        else:
            raise ValueError("Unsupported voting scheme")
        
        happiness_scores = compute_happiness(preferences, winners)
        risk = compute_risk(preferences, winners)

        return outcome, happiness_scores, risk
