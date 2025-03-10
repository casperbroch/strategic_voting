import random
import math

def generate_preferences(M, N):
    parties = {f"P{i+1}": (random.uniform(0, 1), random.uniform(0, 1)) for i in range(M)}

    voters = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(N)]

    preferences = []
    for user_coord in voters:
        distances = []
        for party_label, (px, py) in parties.items():
            distance = math.sqrt((user_coord[0] - px)**2 + (user_coord[1] - py)**2)
            distances.append((distance, party_label))

        ranked_parties = [party_label for (dist, party_label) in sorted(distances)]
        preferences.append(ranked_parties)

    return preferences


import random

def simulate_poll(preferences, sample_size):
    """
    1) Randomly select 'sample_size' voters from the full 'preferences'.
    2) For each selected voter, randomly decide how many top preferences we actually
       see from them (1 to 3).
    3) Assign the voter a noise probability in [0.0, 0.5].
    4) With probability = that noise probability, perform one adjacent swap among 
       their truncated preferences (if there's more than 1).
    5) Return the polled preference lists, each truncated to the known size.
    """
    N = len(preferences)
    if N == 0:
        return []

    M = len(preferences[0])

    sampled_indices = random.sample(range(N), min(sample_size, N))
    polled_preferences = []

    for idx in sampled_indices:
        voter_pref = preferences[idx][:]

        # STEP A: Decide how many top preferences we observe (1 to 3, or up to M if M < 3)
        top_k = random.randint(1, min(M, 3))
        truncated_pref = voter_pref[:top_k]

        # Assign a random noise probability to THIS voter
        voter_noise_prob = random.uniform(0.0, 0.5)

        #With probability voter_noise_prob, swap one adjacent pair
        if random.random() < voter_noise_prob and len(truncated_pref) > 1:
            i = random.randint(0, len(truncated_pref) - 2)
            truncated_pref[i], truncated_pref[i+1] = truncated_pref[i+1], truncated_pref[i]

        polled_preferences.append(truncated_pref)

    return polled_preferences
