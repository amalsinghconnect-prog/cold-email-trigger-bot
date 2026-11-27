import os
import json
import feedparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Connect to Google Sheets (Free via Google Cloud Service Account)
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = json.loads(os.environ["GCP_SERVICE_ACCOUNT_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
sheet = gspread.authorize(creds).open("Cold_Email_Bot_2026").worksheet("Leads")

# 2. Fetch Trigger Feed (Example: Google News RSS for expansion/deal triggers in India)
feed_url = "https://news.google.com/rss/search?q=%22cloud+consulting%22+AND+(%22deal%22+OR+%22expansion%22)+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
feed = feedparser.parse(feed_url)

existing_companies = sheet.col_values(3)  # Column C

for entry in feed.entries[:10]:
    title = entry.title
    company = title.split(" - ")[-1] if " - " in title else "Target Firm"
    if company not in existing_companies:
        # Append new trigger row for enrichment
        sheet.append_row(["", "", company, "Expansion_News", title, "A", "", "", "", "NEEDS_ENRICHMENT", ""])
