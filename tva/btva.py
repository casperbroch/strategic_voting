from tva.voting_schemes import plurality_voting

class BTVA:
    def __init__(self, scheme):
        self.scheme = scheme

    def analyse(self, preferences):
        if self.scheme == "plurality":
            winners = plurality_voting(preferences)
            
            if len(winners) > 1:
                return f"a tie has been detected between: {winners}"
            return plurality_voting(preferences)[0]
        else:
            raise ValueError("Unsupported voting scheme")