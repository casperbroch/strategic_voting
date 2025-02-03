def plurality_voting(preferences):
    vote_counts = {}

    for voter_pref in preferences:
        first_choice = voter_pref[0]
        vote_counts[first_choice] = vote_counts.get(first_choice, 0) + 1

    max_votes = max(vote_counts.values(), default=0)

    winners = [candidate for candidate, votes in vote_counts.items() if votes == max_votes]

    return winners