import pandas as pd
import numpy as np


# Load CSV file
input_file = "data/trends_clean.csv"

df = pd.read_csv(input_file)


print("========== TRENDPULSE ANALYSIS ==========\n")

print(f"Loaded data: {df.shape}")

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

overall_avg_score = df["score"].mean()
overall_avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {overall_avg_score:,.0f}")
print(f"Average comments: {overall_avg_comments:,.0f}")


# category

category_counts = df["category"].value_counts()

print("\n========== STORIES BY CATEGORY ==========")
print(category_counts)

top_category = category_counts.idxmax()
top_category_count = category_counts.max()
print(f"\nMost stories in: {top_category} ({top_category_count} stories)")


# Average of score

average_scores = df.groupby("category")["score"].mean()

print("\n========== AVERAGE SCORE BY CATEGORY ==========")
print(average_scores.round(2))


# Average of comments

average_comments = df.groupby("category")["num_comments"].mean()

print("\n========== AVERAGE COMMENTS BY CATEGORY ==========")
print(average_comments.round(2))


# Highest scoring 

highest_score_index = df["score"].idxmax()

highest_score_story = df.loc[highest_score_index]

print("\n========== HIGHEST SCORING STORY ==========")

print("Title:", highest_score_story["title"])
print("Category:", highest_score_story["category"])
print("Score:", highest_score_story["score"])


#  Most commented story

most_commented_index = df["num_comments"].idxmax()

most_commented_story = df.loc[most_commented_index]

print("\n========== MOST COMMENTED STORY ==========")

print("Title:", most_commented_story["title"])
print("Category:", most_commented_story["category"])
print("Comments:", most_commented_story["num_comments"])

print(
    f'\nMost commented story: "{most_commented_story["title"]}"'
    f'  — {most_commented_story["num_comments"]:,} comments'
)


# NumPy calculations

scores = df["score"].to_numpy()

print("\n========== NUMPY SCORE ANALYSIS ==========")

print("Mean score:", np.mean(scores))
print("Median score:", np.median(scores))
print("Maximum score:", np.max(scores))
print("Minimum score:", np.min(scores))
print("Standard deviation:", np.std(scores))

# New columns
df["engagement"] = df["num_comments"] / (df["score"] + 1)

df["is_popular"] = df["score"] > overall_avg_score

print("\n========== NEW COLUMNS ==========")
print(df[["title", "score", "engagement", "is_popular"]].head())


# Category with highest average score

top_average_category = average_scores.idxmax()

print("\nCategory with highest average score:")
print(top_average_category)


#Category with highest average comments

top_comment_category = average_comments.idxmax()

print("\nCategory with highest average comments:")
print(top_comment_category)


# Save the dataframe

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")


analysis_results = pd.DataFrame({
    "category": average_scores.index,
    "story_count": category_counts.reindex(
        average_scores.index
    ).values,
    "average_score": average_scores.values,
    "average_comments": average_comments.reindex(
        average_scores.index
    ).values
})

analysis_results.to_csv(
    "data/category_analysis.csv",
    index=False
)

print("Category summary also saved to data/category_analysis.csv")