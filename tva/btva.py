from tva.voting_schemes import plurality_voting

class BTVA:
    def __init__(self, scheme):
        self.scheme = scheme

    def analyse(self, preferences):
        if self.scheme == "plurality":
            return plurality_voting(preferences)
        else:
            raise ValueError("Unsupported voting scheme")