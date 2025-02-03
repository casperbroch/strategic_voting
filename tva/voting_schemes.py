def plurality_voting(preferences):
    vote_counts = {}
    
    for voter_pref in preferences:
        first_choice = voter_pref[0]
        vote_counts[first_choice] = vote_counts.get(first_choice, 0) + 1
    
    winner = sorted(vote_counts.items(), key=lambda x: (-x[1], x[0]))[0][0]
    return winner
