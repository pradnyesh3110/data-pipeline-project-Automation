import feedparser
import pandas as pd

# Example RSS feed (you can change later)
url = "https://news.google.com/rss"

feed = feedparser.parse(url)

data = []

for entry in feed.entries:
    data.append({
        "title": entry.title,
        "link": entry.link,
        "published": entry.published
    })

df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)

print("CSV file created successfully")
