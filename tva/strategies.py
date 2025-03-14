import numpy as np
from tva.voting_schemes import *

def switch_ranking(preferences, k=np.inf):
    # compromising + burying
    k = min(k, len(preferences))
    preferences_to_change = np.random.choice(range(len(preferences)), size=k, replace=False)
    for i in preferences_to_change:
        if len(preferences[i]) > 1:
            idx1, idx2 = np.random.randint(len(preferences[i]), size=2) # in case of same values nothing changes
            preferences[i][idx1], preferences[i][idx2] = preferences[i][idx2], preferences[i][idx1]  
    print('Compromising/burying')
    for i, prefs in enumerate(preferences):
        print(f"User {i+1} new preference list: {prefs}")
    return preferences, preferences_to_change

def bullet_voting_vectors(preferences, scheme, k=np.inf):
    M = len(preferences[0])
    k = min(k, len(preferences))
    preferences_to_change = np.random.choice(range(len(preferences)), size=k, replace=False)
    if scheme == "voting2":
        vectors = convert_to_votingfor2(preferences, M)
        for i in preferences_to_change:
            idx = np.random.choice(np.where(vectors[i] == 1)[0])
            vectors[i][idx] = 0
    elif scheme == "antiplurality":
        vectors = convert_to_antiplurality(preferences, M)
        vectors_plurality = convert_to_plurality(preferences, M)
        for i in preferences_to_change: 
            vectors[i] = vectors_plurality[i]
            
    elif scheme == "borda":
        vectors = convert_to_borda(preferences, M)
        for i in preferences_to_change:
            new_vector = np.zeros(M)
            new_vector[vectors[i].argmax()] = M - 1
            vectors[i] = new_vector
    else:
        raise ValueError("Unsupported voting scheme")
            
    return vectors, preferences_to_change