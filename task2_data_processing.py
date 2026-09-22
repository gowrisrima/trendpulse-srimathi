import pandas as pd
import glob
import os

json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in the data folder.")
    exit()

# Select JSON file
input_file = max(json_files, key=os.path.getmtime)

print(f"Reading file: {input_file}")


# Load JSON data into Pandas
df = pd.read_json(input_file)


# Display original number of rows
print(f"Loaded {len(df)} stories from {input_file}")


# Remove duplicate stories 
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")


# Remove rows 
required_columns = ["post_id", "title", "score"]

df = df.dropna(subset=required_columns)
print(f"After removing nulls: {len(df)}")


# Clean title text
df["title"] = df["title"].astype(str).str.strip()


# Clean category text
df["category"] = df["category"].astype(str).str.lower().str.strip()


# Convert score and comments to numbers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
    df["num_comments"],
    errors="coerce"
)


# Remove rows where score/comments could not be converted
df = df.dropna(subset=["score", "num_comments"])


# Convert scores and comments to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# Remove negative comment counts 
df = df[df["num_comments"] >= 0]
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")


# Reset row numbers
df = df.reset_index(drop=True)


# Create output filename 
output_file = "data/trends_clean.csv"


# Save cleaned data
df.to_csv(output_file, index=False)


# Display results
print(f"\nSaved {len(df)} rows to {output_file}")

# Category summary
print("\nStories per category:")
category_order = ["technology", "worldnews", "sports", "science", "entertainment"]
category_counts = df["category"].value_counts().reindex(category_order, fill_value=0)
for category, count in category_counts.items():
    print(f"  {category:<15}{count}")