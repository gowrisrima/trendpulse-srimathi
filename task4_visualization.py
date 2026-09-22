import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/trends_analysed.csv")

os.makedirs("outputs", exist_ok=True)

def shorten_title(title, max_len=50):
    """Cut long titles down so they don't overflow the chart's y-axis."""
    if len(title) > max_len:
        return title[:max_len - 3] + "..."
    return title


# Bar chart by score

top_stories = df.sort_values("score", ascending=False).head(10)
top_stories = top_stories.iloc[::-1]

short_titles = top_stories["title"].apply(shorten_title)

plt.figure(figsize=(10, 6))

plt.barh(short_titles, top_stories["score"])

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()

plt.savefig("outputs/chart1_top_stories.png")

plt.show()


#Bar chart by category 

category_counts = df["category"].value_counts()

colors = plt.cm.tab10.colors[:len(category_counts)]

plt.figure(figsize=(10, 6))

plt.bar(category_counts.index, category_counts.values, color=colors)

plt.title("Number of Stories by Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/chart2_categories.png")

plt.show()


# Scatter plot

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(10, 6))

plt.scatter(not_popular["score"], not_popular["num_comments"],
            color="gray", label="Not Popular", alpha=0.6)
plt.scatter(popular["score"], popular["num_comments"],
            color="red", label="Popular", alpha=0.6)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")

plt.show()


# one dashboard figure

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# First subplot
axes[0].barh(short_titles, top_stories["score"])
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")

# Second subplot
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_title("Number of Stories by Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=45)

# Third subplot
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                 color="gray", label="Not Popular", alpha=0.6)
axes[2].scatter(popular["score"], popular["num_comments"],
                 color="red", label="Popular", alpha=0.6)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

fig.suptitle("TrendPulse Dashboard")

plt.tight_layout()

plt.savefig("outputs/dashboard.png")

plt.show()


print("All visualizations created successfully.")

print("\nFiles saved:")
print("outputs/chart1_top_stories.png")
print("outputs/chart2_categories.png")
print("outputs/chart3_scatter.png")
print("outputs/dashboard.png")