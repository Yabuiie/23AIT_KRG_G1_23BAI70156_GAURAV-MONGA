import pandas as pd
import csv

INPUT_FILE = "data/main.csv"

print("🔄 Loading CSV safely...")

df = pd.read_csv(
    INPUT_FILE,
    engine="python",          # required for malformed CSVs
    sep=",",
    quotechar='"',
    quoting=csv.QUOTE_MINIMAL,
    escapechar="\\",          # handles escaped quotes if present
    on_bad_lines="skip",      # skip only truly broken lines
    dtype=str,                # NO type coercion
    keep_default_na=False     # prevent NaN injection
)

print("✅ CSV loaded")
print("Shape:", df.shape)
print(df.head(3))

# Save EXACT data (no changes)
df.to_parquet("skillweave_clean.parquet", index=False)
df.to_csv("skillweave_clean.csv", index=False)

print("✅ Saved clean CSV + Parquet without modifying content")
