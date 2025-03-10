import numpy as np

def plurality_voting(preferences):
    vote_counts = {}

    for voter_pref in preferences:
        first_choice = voter_pref[0]
        vote_counts[first_choice] = vote_counts.get(first_choice, 0) + 1

    max_votes = max(vote_counts.values(), default=0)

    winners = [candidate for candidate, votes in vote_counts.items() if votes == max_votes]

    return winners


def convert_to_votingfor2(preferences):
    voting_vectors = np.zeros_like(preferences, dtype=int)

    for (i, preference) in enumerate(preferences):
        voting_vectors[i][int(preference[0][1]) - 1] = 1
        voting_vectors[i][int(preference[1][1]) - 1] = 1
    return voting_vectors

def convert_to_antiplurality(preferences):
    voting_vectors = np.ones_like(preferences, dtype=int)
    for (i, preference) in enumerate(preferences):
        voting_vectors[i][int(preference[-1][1]) - 1] = 0
    return voting_vectors

def convert_to_borda(preferences):
    M = len(preferences[0])
    voting_vectors = np.ones_like(preferences, dtype=int)
    for (i, preference) in enumerate(preferences):
        for (j, candidate) in enumerate(preference):
            voting_vectors[i][int(candidate[1]) - 1] = M - j - 1
            
    return voting_vectors
        
def winners_voting_vectors(voting_vectors):
    total_points = voting_vectors.sum(0)
    winners = [f"P{i+1}" for i in np.where(total_points == max(total_points))[0]]
    return winners
    