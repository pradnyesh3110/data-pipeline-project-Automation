import feedparser
import pandas as pd
from datetime import datetime

# Tool-focused sources
FEEDS = {
    "ProductHunt": "https://www.producthunt.com/feed",
    "ShowHN_AI": "https://hnrss.org/showhn",
    "MarkTechTools": "https://www.marktechpost.com/category/ai-tools/feed/"
}

# Keywords to ensure we get 'Tools' and not just articles
TOOL_KEYWORDS = ['ai', 'tool', 'platform', 'app', 'bot', 'gpt', 'llm', 'api', 'extension', 'agent']

def fetch_ai_tools():
    all_tools = []
    
    for name, url in FEEDS.items():
        print(f"Checking {name}...")
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            content = (entry.title + " " + entry.get("summary", "")).lower()
            
            # Check if it mentions AI keywords
            if any(word in content for word in TOOL_KEYWORDS):
                all_tools.append({
                    "tool_name": entry.title,
                    "link": entry.link,
                    "source": name,
                    "date_added": datetime.now().strftime("%Y-%m-%d"),
                    "summary": entry.get("summary", "No description provided.")[:200] + "..."
                })
    
    # Process and deduplicate
    new_df = pd.DataFrame(all_tools)
    
    try:
        # Keep a running list of everything we find
        existing_df = pd.read_csv("output.csv")
        final_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['link'], keep='first')
    except Exception:
        final_df = new_df

    final_df.to_csv("output.csv", index=False)
    print(f"Done! Saved {len(final_df)} unique tools to output.csv")

if __name__ == "__main__":
    fetch_ai_tools()
