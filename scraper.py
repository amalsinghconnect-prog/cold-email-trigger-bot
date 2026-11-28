import os
import json
import feedparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Connect to Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = json.loads(os.environ["GCP_SERVICE_ACCOUNT_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
sheet = gspread.authorize(creds).open("Cold_Email_Bot_2026").worksheet("Leads")

# 2. Multiple Targeted Trigger Feeds (Hiring + Deal Wins in India)
feeds = [
    ("Hiring_Trigger", "https://news.google.com/rss/search?q=(%22Bid+Manager%22+OR+%22Pre-Sales%22+OR+%22Presales%22)+AND+(%22hiring%22+OR+%22Bengaluru%22+OR+%22India%22)+when:14d&hl=en-IN&gl=IN&ceid=IN:en"),
    ("Deal_Win_Trigger", "https://news.google.com/rss/search?q=(%22IT+services%22+OR+%22digital+transformation%22+OR+%22cloud%22)+AND+(%22wins+deal%22+OR+%22multi-year+contract%22+OR+%22partnership%22)+AND+%22India%22+when:14d&hl=en-IN&gl=IN&ceid=IN:en"),
    ("Consulting_Expansion", "https://news.google.com/rss/search?q=(%22consulting%22+OR+%22BFSI%22+OR+%22enterprise+solutions%22)+AND+(%22expansion%22+OR+%22new+office%22+OR+%22leadership%22)+AND+%22Bengaluru%22+when:14d&hl=en-IN&gl=IN&ceid=IN:en")
]

existing_triggers = sheet.col_values(5)  # Deduplicate using Column E (Trigger_Detail)

for trigger_type, url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries[:15]:
        # Strip the news publisher name off the end so only the clean headline remains
        clean_headline = entry.title.rsplit(" - ", 1)[0]
        trigger_text = f"{clean_headline} ({entry.link})"
        
        if trigger_text not in existing_triggers:
            sheet.append_row([
                "",               # Col A: First_Name (you fill after checking LinkedIn)
                "",               # Col B: Email (you fill)
                "Check Headline", # Col C: Company (replace with target company name)
                trigger_type,     # Col D: Trigger_Type
                trigger_text,     # Col E: Trigger_Detail + Article Link
                "A",              # Col F: AB_Variant
                "", "", "",       # Col G-I: AI-generated Subject & Emails
                "NEEDS_ENRICHMENT",
                ""
            ])
            existing_triggers.append(trigger_text)
