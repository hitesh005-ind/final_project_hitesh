
#===============================================================
#  FINALL PROJECT - AIR QUALITY ANALYSIS
#============================================================
 #=============================================================
 # AUTHOR: HITESH CHAUDHARY
 #=============================================================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(folder, "AirQualityUCI.csv")

df = pd.read_csv(
    file_path,
    sep=";",
    encoding="latin1"
)

# Remove completely empty columns
df = df.dropna(axis=1, how="all")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()


for col in df.columns:

    if col not in ["Date", "Time"]:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(",", ".", regex=False)
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")

# Replace invalid sensor value -200 with NaN
for col in df.columns:

    if col not in ["Date", "Time"]:

        df[col] = df[col].replace(-200, np.nan)


df["Date"] = df["Date"].astype(str).str.strip()
df["Time"] = df["Time"].astype(str).str.strip()

# AirQualityUCI has time like 18.00.00
# Convert it to 18:00:00
df["Time"] = df["Time"].str.replace(".", ":", regex=False)

# Create proper DateTime column
df["DateTime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"],
    dayfirst=True,
    errors="coerce"
)

# Sort according to time
df = df.sort_values("DateTime")

# Remove duplicate rows
df = df.drop_duplicates()


print("\n========== DATASET ==========")
print(df.head())

print("\n========== DATA INFORMATION ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


cleaned_file = os.path.join(
    folder,
    "Cleaned_AirQualityUCI.csv"
)

df.to_csv(cleaned_file, index=False)

print("\nCleaned dataset saved successfully!")


sns.set_style("whitegrid")


plt.figure(figsize=(8, 5))

sns.histplot(
    df["CO(GT)"].dropna(),
    bins=30,
    kde=True
)

plt.title("Distribution of CO(GT)")
plt.xlabel("CO(GT)")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

plot_df = df[["DateTime", "CO(GT)"]].copy()

plot_df = plot_df.dropna()

plt.figure(figsize=(12, 6))

plt.plot(
    plot_df["DateTime"],
    plot_df["CO(GT)"]
)

plt.title("CO Concentration Over Time")
plt.xlabel("Date")
plt.ylabel("CO Concentration")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


plot_df = df[["DateTime", "T"]].copy()

plot_df = plot_df.dropna()

plt.figure(figsize=(12, 6))

plt.plot(
    plot_df["DateTime"],
    plot_df["T"]
)

plt.title("Temperature Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


plot_df = df[["DateTime", "RH"]].copy()

plot_df = plot_df.dropna()

plt.figure(figsize=(12, 6))

plt.plot(
    plot_df["DateTime"],
    plot_df["RH"]
)

plt.title("Relative Humidity Over Time")
plt.xlabel("Date")
plt.ylabel("Humidity (%)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


plot_df = df[["T", "CO(GT)"]].copy()

plot_df = plot_df.dropna()

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=plot_df,
    x="T",
    y="CO(GT)"
)

plt.title("Temperature vs CO Concentration")
plt.xlabel("Temperature (°C)")
plt.ylabel("CO Concentration")

plt.tight_layout()
plt.show()


plt.figure(figsize=(8, 6))

sns.boxplot(
    y=df["CO(GT)"].dropna()
)

plt.title("CO Concentration Box Plot")
plt.ylabel("CO Concentration")

plt.tight_layout()
plt.show()


numeric_df = df.select_dtypes(
    include=np.number
)

plt.figure(figsize=(14, 10))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Air Quality Correlation Heatmap")

plt.tight_layout()
plt.show()


print("\n====================================")
print("AIR QUALITY ANALYSIS COMPLETED")
print("====================================")