import os
EMAIL_USER = os.getenv("Pradnyeshrisbud1@gmail.com")
EMAIL_PASS = os.getenv("aqbr yjpk zkby efzv")
EMAIL_TO = os.getenv("Pradnyeshrisbud1@gmail.com")
import feedparser
import pandas as pd
import os
from datetime import datetime

# 1. ONLY use sources that are for "Products" and "Tools"
SOURCES = {
    "Show HN": "https://hnrss.org/showhn",
    "Reddit_SideProject": "https://www.reddit.com/r/SideProject/new/.rss",
    "ProductHunt": "https://www.producthunt.com/feed"
}

def fetch_tools():
    tool_list = []
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    # 2. Strict Keywords: Must mention these
    ALLOW_KEYWORDS = ['ai', 'tool', 'bot', 'gpt', 'app', 'saas', 'automation', 'built', 'github']
    
    # 3. Reject Keywords: Block these news topics
    REJECT_KEYWORDS = ['crisis', 'trump', 'nasa', 'war', 'killed', 'arrested', 'hospital', 'sport', 'ncaa']

    for name, url in SOURCES.items():
        print(f"Scanning {name}...")
        feed = feedparser.parse(url, agent=agent)
        
        for entry in feed.entries:
            title = entry.title.lower()
            
            # LOGIC: Must have an ALLOW word AND NO REJECT words
            if any(k in title for k in ALLOW_KEYWORDS):
                if not any(rk in title for rk in REJECT_KEYWORDS):
                    tool_list.append({
                        "tool_name": entry.title,
                        "link": entry.link,
                        "source": name,
                        "date_found": datetime.now().strftime("%Y-%m-%d")
                    })

    new_data = pd.DataFrame(tool_list)

    # 4. Clean and Save (Resetting the columns to be simple)
    if not new_data.empty:
        if os.path.exists("output.csv"):
            try:
                old_data = pd.read_csv("output.csv")
                # Ensure we only keep the columns we want
                combined = pd.concat([old_data, new_data], ignore_index=True)
                final_data = combined[['tool_name', 'link', 'source', 'date_found']].drop_duplicates(subset=['link'])
            except:
                final_data = new_data
        else:
            final_data = new_data
            
        final_data.to_csv("output.csv", index=False)
        print(f"Done! Found {len(new_data)} new tools.")
    else:
        print("No new tools found matching your filters.")

if __name__ == "__main__":
    fetch_tools()
