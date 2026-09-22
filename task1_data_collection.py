import requests
import time
import json
import os
from datetime import datetime

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
BEST_STORIES_URL = "https://hacker-news.firebaseio.com/v0/beststories.json"
NEW_STORIES_URL = "https://hacker-news.firebaseio.com/v0/newstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}

TARGET_TOTAL = 125

category_keywords = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


def find_category(title):
    """Find the first category whose keyword appears in the title."""

    title_lower = title.lower()

    for category, keywords in category_keywords.items():

        for keyword in keywords:

            if keyword.lower() in title_lower:
                return category

    return None


# fetch stories

try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    top_story_ids = response.json()[:500]

    print(f"Found {len(top_story_ids)} top story IDs.")

except requests.RequestException as error:

    print("Failed to fetch top story IDs:", error)
    exit()


all_stories = []
fetched_ids = set()


def fetch_story(story_id):
    """Fetch one HackerNews story safely."""

    if story_id in fetched_ids:
        return None

    fetched_ids.add(story_id)

    try:

        response = requests.get(
            ITEM_URL.format(story_id),
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        story = response.json()

        if not story or story.get("type") != "story":
            return None

        if not story.get("title"):
            return None

        return story

    except requests.RequestException as error:

        print(f"\nFailed to fetch story {story_id}: {error}")
        return None


print("\nFetching first 500 story details...")

for index, story_id in enumerate(top_story_ids, start=1):

    story = fetch_story(story_id)

    if story:
        all_stories.append(story)

    print(f"Fetched {index}/{len(top_story_ids)}", end="\r")


print(
    f"\nSuccessfully fetched {len(all_stories)} "
    f"stories from the first 500 IDs."
)


# Categorize the fetched stories

stories = []

category_count = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}


def add_matching_story(story):
    """Add a story if its category still has space."""

    title = story.get("title", "")
    category = find_category(title)

    if category is None:
        return False

    if category_count[category] >= 25:
        return False

    story_data = {
        "post_id": story.get("id"),
        "title": title,
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", "unknown"),
        "collected_at": datetime.now().isoformat()
    }

    stories.append(story_data)
    category_count[category] += 1

    return True


for story in all_stories:

    if len(stories) >= TARGET_TOTAL:
        break

    add_matching_story(story)


print("\nMatching stories from first 500 IDs:")

for category, count in category_count.items():
    print(f"{category}: {count}")

print(f"Total matching stories: {len(stories)}")


if len(stories) < TARGET_TOTAL:

    print(
        f"\nOnly {len(stories)} stories found so far (target {TARGET_TOTAL})."
    )

    print(
        "Fetching additional HackerNews best stories..."
    )

    try:

        response = requests.get(
            BEST_STORIES_URL,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        best_story_ids = response.json()

    except requests.RequestException as error:

        print("Failed to fetch best story IDs:", error)
        best_story_ids = []


    for story_id in best_story_ids:

        if len(stories) >= TARGET_TOTAL:
            break

        story = fetch_story(story_id)

        if story:

            add_matching_story(story)

if len(stories) < 100:

    print(
        f"\nStill only {len(stories)} stories after best stories."
    )

    print(
        "Fetching additional HackerNews new stories..."
    )

    try:

        response = requests.get(
            NEW_STORIES_URL,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        new_story_ids = response.json()

    except requests.RequestException as error:

        print("Failed to fetch new story IDs:", error)
        new_story_ids = []

    for story_id in new_story_ids:

        if len(stories) >= TARGET_TOTAL:
            break

        story = fetch_story(story_id)

        if story:

            add_matching_story(story)


# Wait 2 seconds between category 
print("\nProcessing categories...")

for category in category_keywords:

    print(
        f"Processed {category}: "
        f"{category_count[category]} stories"
    )

    if category != "entertainment":
        time.sleep(2)


# Create data folder

os.makedirs("data", exist_ok=True)


# Save JSON

today = datetime.now().strftime("%Y%m%d")

filename = f"data/trends_{today}.json"


with open(filename, "w", encoding="utf-8") as file:

    json.dump(
        stories,
        file,
        indent=4,
        ensure_ascii=False
    )


# Final output

print("\n----------------------------------------")

print(f"Collected {len(stories)} stories.")

print(f"Saved to {filename}")

print("----------------------------------------")

print("\nStories collected by category:")

for category, count in category_count.items():

    print(f"{category}: {count}")