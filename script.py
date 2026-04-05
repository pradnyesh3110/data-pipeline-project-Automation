import feedparser
import pandas as pd
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

# ✅ Environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

# ✅ Sources
SOURCES = {
    "Show HN": "https://hnrss.org/showhn",
    "Reddit_SideProject": "https://www.reddit.com/r/SideProject/new/.rss",
    "ProductHunt": "https://www.producthunt.com/feed"
}

# ✅ Email Function
def send_email():
    if not os.path.exists("output.csv"):
        print("CSV not found, skipping email.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Weekly AI Tools Report'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg.set_content('Attached is your weekly AI tools report.')

    with open('output.csv', 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='csv', filename='output.csv')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print("Email sent successfully!")

# ✅ Scraper Function
def fetch_tools():
    tool_list = []
    agent = "Mozilla/5.0"

    ALLOW_KEYWORDS = ['ai', 'tool', 'bot', 'gpt', 'app', 'saas', 'automation', 'built', 'github']
    REJECT_KEYWORDS = ['crisis', 'trump', 'nasa', 'war', 'killed', 'arrested', 'hospital', 'sport', 'ncaa']

    for name, url in SOURCES.items():
        print(f"Scanning {name}...")
        feed = feedparser.parse(url, agent=agent)

        for entry in feed.entries:
            title = entry.title.lower()

            if any(k in title for k in ALLOW_KEYWORDS):
                if not any(rk in title for rk in REJECT_KEYWORDS):
                    tool_list.append({
                        "tool_name": entry.title,
                        "link": entry.link,
                        "source": name,
                        "date_found": datetime.now().strftime("%Y-%m-%d")
                    })

    new_data = pd.DataFrame(tool_list)

    # ✅ Handle empty case (IMPORTANT FIX)
    if new_data.empty:
        print("No new tools found. Skipping CSV and email.")
        return

    # ✅ Merge with existing CSV
    if os.path.exists("output.csv"):
        try:
            old_data = pd.read_csv("output.csv")
            combined = pd.concat([old_data, new_data], ignore_index=True)
            final_data = combined.drop_duplicates(subset=['link'])
        except:
            final_data = new_data
    else:
        final_data = new_data

    final_data.to_csv("output.csv", index=False)
    print(f"Saved {len(new_data)} new tools.")

    # ✅ Send email AFTER CSV is created
    send_email()

# ✅ Main Execution
if __name__ == "__main__":
    fetch_tools()
