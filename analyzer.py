import pandas as pd
import matplotlib.pyplot as plt

# Read in the CSV
df = pd.read_csv("experiment_results.csv")

# HAPPINESS PLOTS 

# 1) Scatter: OutcomeMatchFraction vs. SampleSizeFraction
plt.figure()
plt.plot(df["SampleSizeFraction"], df["OutcomeMatchFraction"])
plt.title("Outcome Match Fraction vs. Sample Size Fraction")
plt.xlabel("Sample Size Fraction")
plt.ylabel("Outcome Match Fraction")
plt.grid(True)
plt.show()

# 2) Bar chart of Strategic Mismatch Fraction by Truncation
grouped_trunc = df.groupby("Truncation")["StrategicMismatchFraction"].mean()
plt.figure()
grouped_trunc.plot(kind="bar")
plt.title("Mean Strategic Mismatch Fraction by Truncation")
plt.xlabel("Truncation")
plt.ylabel("Mean Strategic Mismatch Fraction")
plt.grid(True)
plt.show()

# 3) Histogram of HappinessDifference
plt.figure()
plt.hist(df["HappinessDifference"], bins=10)
plt.title("Histogram of HappinessDifference (Poll - True)")
plt.xlabel("HappinessDifference")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# 4) Line charts of Poll vs. True Happiness for different NoiseRanges
unique_noises = df["NoiseRange"].unique()
for noise in unique_noises:
    subset = df[df["NoiseRange"] == noise].sort_values("SampleSizeFraction")
    plt.figure()
    plt.plot(subset["SampleSizeFraction"], subset["HappinessPollMean"], marker='o', label="Poll Happiness")
    plt.plot(subset["SampleSizeFraction"], subset["HappinessTrueMean"], marker='o', label="True Happiness")
    plt.title(f"Happiness Means vs. Sample Size (Noise={noise})")
    plt.xlabel("Sample Size Fraction")
    plt.ylabel("Mean Happiness")
    plt.legend()
    plt.grid(True)
    plt.show()


# RISK PLOTS
# 1) Histogram of RiskDifference
plt.figure()
plt.hist(df["RiskDifference"], bins=10)
plt.title("Histogram of RiskDifference (Poll - True)")
plt.xlabel("RiskDifference")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# 2) Bar chart of average Poll Risk by Truncation
grouped_risk_trunc = df.groupby("Truncation")["RiskPollMean"].mean()
plt.figure()
grouped_risk_trunc.plot(kind="bar")
plt.title("Mean Poll Risk by Truncation")
plt.xlabel("Truncation")
plt.ylabel("Mean Poll Risk")
plt.grid(True)
plt.show()

# 2) Bar chart of average Poll Happiness by Truncation
grouped_happ_trunc = df.groupby("Truncation")["HappinessPollMean"].mean()
plt.figure()
grouped_happ_trunc.plot(kind="bar")
plt.title("Mean Poll Happiness by Truncation")
plt.xlabel("Truncation")
plt.ylabel("Mean Poll Happiness")
plt.grid(True)
plt.show()

# 3) Scatter: RiskPollMean vs. SampleSizeFraction
plt.figure()
plt.plot(df["SampleSizeFraction"], df["RiskPollMean"])
plt.title("Poll Risk vs. Sample Size Fraction")
plt.xlabel("Sample Size Fraction")
plt.ylabel("Poll Risk")
plt.grid(True)
plt.show()

# 4) Line charts: Poll vs. True Risk for each NoiseRange
for noise in unique_noises:
    subset = df[df["NoiseRange"] == noise].sort_values("SampleSizeFraction")
    plt.figure()
    plt.plot(subset["SampleSizeFraction"], subset["RiskPollMean"], marker='o', label="Poll Risk")
    plt.plot(subset["SampleSizeFraction"], subset["RiskTrueMean"], marker='o', label="True Risk")
    plt.title(f"Risk Means vs. Sample Size (Noise={noise})")
    plt.xlabel("Sample Size Fraction")
    plt.ylabel("Risk")
    plt.legend()
    plt.grid(True)
    plt.show()
