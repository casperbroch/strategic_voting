import random
import math

def generate_preferences(M, N):
    parties = {f"P{i+1}": (random.uniform(0, 1), random.uniform(0, 1)) for i in range(M)}
    
    users = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(N)]
    
    preferences = []
    for user in users:
        distances = []
        for party, (px, py) in parties.items():
            distance = math.sqrt((user[0] - px) ** 2 + (user[1] - py) ** 2)
            distances.append((distance, party))
        
        sorted_parties = [party for _, party in sorted(distances)]
        preferences.append(sorted_parties)
    
    return preferences
