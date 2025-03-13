import itertools
import csv
from tqdm import tqdm

from tva.btva import BTVA
from tva.happiness import compute_sum_happiness
from tva.generate_situation import generate_preferences, simulate_poll

def run_experiment():
    M = 5  # Number of parties
    N = 50  # Number of voters
    preferences = generate_preferences(M, N)

    #sample_sizes = [0.2, 0.4, 0.6, 0.8, 1.0]
    sample_sizes = [0.5]

    # noise_ranges = [
    #     [0.0, 0.0],
    # ]
    noise_ranges = [
        [0.0, 0.1],
        [0.0, 0.2],
        [0.0, 0.3],
        [0.0, 0.4],
        [0.0, 0.5]
    ]
    truncation_ranges = [3,4,5]

    n_repeats = 100  # repeat each combo to average out randomness

    results = []

    combos = list(itertools.product(sample_sizes, noise_ranges, truncation_ranges))

    for (sample, noise, trunc) in tqdm(combos, desc="Experiment Progress"):
        sample_size = int(N * sample)

        sum_outcome_match = 0
        sum_strat_mismatch = 0
        sum_hap_poll = 0.0
        sum_hap_true = 0.0

        sum_risk_poll = 0.0
        sum_risk_true = 0.0

        for _ in range(n_repeats):
            # Simulate a poll with some truncation and noise
            polled_prefs = simulate_poll(preferences, sample_size, trunc, noise)

            # Analyze polled preferences
            btva = BTVA(scheme="plurality")
            outcome_poll, happiness_poll, risk_poll = btva.analyse(polled_prefs, M)
            outcome_true, happiness_true, risk_true = btva.analyse(preferences, M)

            avg_happiness_poll = compute_sum_happiness(happiness_poll) / sample_size
            avg_happiness_true = compute_sum_happiness(happiness_true) / N

            outcome_match = 1 if outcome_poll == outcome_true else 0
            strategy_mismatch = 1 if risk_poll != risk_true else 0

            sum_outcome_match += outcome_match
            sum_strat_mismatch += strategy_mismatch
            sum_hap_poll += avg_happiness_poll
            sum_hap_true += avg_happiness_true

            sum_risk_poll += risk_poll
            sum_risk_true += risk_true

        # Compute averages over the n_repeats
        avg_outcome_match = sum_outcome_match / n_repeats
        avg_strat_mismatch = sum_strat_mismatch / n_repeats
        avg_hap_poll = sum_hap_poll / n_repeats
        avg_hap_true = sum_hap_true / n_repeats

        # NEW: Averages for poll-based and true-based risk
        avg_risk_poll = sum_risk_poll / n_repeats
        avg_risk_true = sum_risk_true / n_repeats

        # Differences
        happiness_diff = avg_hap_poll - avg_hap_true
        risk_diff = avg_risk_poll - avg_risk_true 

        results.append({
            "SampleSizeFraction": sample,
            "NoiseRange": str(noise),
            "Truncation": trunc,
            "OutcomeMatchFraction": avg_outcome_match,
            "StrategicMismatchFraction": avg_strat_mismatch,
            "HappinessPollMean": avg_hap_poll,
            "HappinessTrueMean": avg_hap_true,
            "HappinessDifference": happiness_diff,
            "RiskPollMean": avg_risk_poll,
            "RiskTrueMean": avg_risk_true,
            "RiskDifference": risk_diff
        })

    # Write aggregated results to CSV
    with open("experiment_results.csv", "w", newline="") as f:
        fieldnames = [
            "SampleSizeFraction",
            "NoiseRange",
            "Truncation",
            "OutcomeMatchFraction",
            "StrategicMismatchFraction",
            "HappinessPollMean",
            "HappinessTrueMean",
            "HappinessDifference",
            "RiskPollMean",
            "RiskTrueMean",
            "RiskDifference"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    run_experiment()
