import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_summary(jobs_list):
    """Compiles all jobs into a single summary message."""
    if not jobs_list:
        return

    print(f"📲 Telegram Module: Sending 1 digest message containing {len(jobs_list)} jobs...")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Start building the massive string
    message = f"🌟 <b>{len(jobs_list)} NEW UPWORK JOBS</b> 🌟\n\n"

    for i, job in enumerate(jobs_list, 1):
        # We just include the title, time, and link to keep it compact
        message += f"<b>{i}.</b> <a href='{job['link']}'>{job['title']}</a> ({job['date']})\n\n"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("   -> ✅ Summary digest sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"   -> ❌ Failed to send summary. Error: {e}")


# --- Quick Test Block ---
# You can run this file directly to test if your Bot Token and Chat ID are working
if __name__ == "__main__":
    test_jobs = [{
        "title": "Test Bioinformatics Script",
        "date": "Just now",
        "description": "This is a test to make sure the uqursuzbot is securely connected to your phone.",
        "link": "https://www.upwork.com"
    }]
    send_telegram_summary(test_jobs)