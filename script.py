import feedparser
import pandas as pd
import os
from datetime import datetime

# Sources for AI Tools (Added User-Agent to avoid blocks)
SOURCES = {
    "Show HN": "https://hnrss.org/showhn",
    "Reddit_SideProject": "https://www.reddit.com/r/SideProject/new/.rss",
    "ProductHunt": "https://www.producthunt.com/feed"
}

def fetch_tools():
    tool_list = []
    # Tell the website we are a browser, not a bot
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    for name, url in SOURCES.items():
        print(f"Scanning {name}...")
        feed = feedparser.parse(url, agent=agent)
        
        for entry in feed.entries:
            title = entry.title.lower()
            if any(k in title for k in ['ai', 'tool', 'bot', 'gpt', 'app']):
                tool_list.append({
                    "tool_name": entry.title,
                    "link": entry.link,
                    "source": name,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })

    new_data = pd.DataFrame(tool_list)

    # Check if file exists to avoid 'File Not Found' errors
    if os.path.exists("output.csv"):
        old_data = pd.read_csv("output.csv")
        final_data = pd.concat([old_data, new_data]).drop_duplicates(subset=['link'])
    else:
        final_data = new_data

    final_data.to_csv("output.csv", index=False)
    print(f"Success! {len(final_data)} tools in database.")

if __name__ == "__main__":
    fetch_tools()
