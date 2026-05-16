import requests
import threading
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SEEN_JOBS_FILE = "seen_jobs.json"
LAST_RUN_FILE = "last_run.txt"


# --- Outbound notifications ---

def send_no_jobs_message():
    _send_reply("🔍 Sweep complete — no new jobs found.")


def send_telegram_summary(jobs_list):
    """Compiles all jobs into a single summary message."""
    if not jobs_list:
        return

    print(f"📲 Telegram Module: Sending 1 digest message containing {len(jobs_list)} jobs...")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    message = f"🌟 <b>{len(jobs_list)} NEW UPWORK JOBS</b> 🌟\n\n"
    for i, job in enumerate(jobs_list, 1):
        message += f"<b>{i}.</b> <a href='{job['link']}'>{job['title']}</a> ({job['date']})\n\n"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("   -> ✅ Summary digest sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"   -> ❌ Failed to send summary. Error: {e}")


def _send_reply(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=10,
        )
    except requests.exceptions.RequestException:
        pass


# --- Two-way bot controller ---

class BotController:
    def __init__(self, pause_event: threading.Event, force_search_event: threading.Event = None, topics_file: str = "search_topics.txt"):
        self._pause_event = pause_event
        self._force_search_event = force_search_event
        self._topics_file = topics_file
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)

    def start(self):
        self._thread.start()
        print("🤖 Telegram bot controller started (polling for commands).")

    def _get_updates(self, offset):
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset
            resp = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
                params=params,
                timeout=40,
            )
            resp.raise_for_status()
            return resp.json().get("result", [])
        except requests.exceptions.RequestException:
            time.sleep(5)
            return []

    def _poll_loop(self):
        offset = None
        while True:
            updates = self._get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                message = update.get("message", {})
                # Only process messages from the authorised chat
                if str(message.get("chat", {}).get("id", "")) != str(CHAT_ID):
                    continue
                text = message.get("text", "").strip()
                if text.startswith("/"):
                    self._handle_command(text)

    def _handle_command(self, text: str):
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if command == "/pause":
            self._pause_event.set()
            _send_reply("⏸ Monitor <b>paused</b>. Send /resume to continue.")
            print("⏸ Paused via Telegram command.")

        elif command == "/resume":
            self._pause_event.clear()
            _send_reply("▶️ Monitor <b>resumed</b>. Next sweep will start shortly.")
            print("▶️ Resumed via Telegram command.")

        elif command == "/add":
            if not arg:
                _send_reply("Usage: /add &lt;search topic&gt;")
                return
            with open(self._topics_file, "a", encoding="utf-8") as f:
                f.write(f"\n{arg}")
            _send_reply(f"✅ Added topic: <b>{arg}</b>\nTakes effect on the next sweep.")
            print(f"✅ Added search topic via Telegram: {arg}")

        elif command == "/status":
            seen_count = 0
            if os.path.exists(SEEN_JOBS_FILE):
                try:
                    with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as f:
                        seen_count = len(json.load(f))
                except (json.JSONDecodeError, OSError):
                    pass

            last_run = "never"
            if os.path.exists(LAST_RUN_FILE):
                try:
                    with open(LAST_RUN_FILE, "r") as f:
                        last_run = f.read().strip()
                except OSError:
                    pass

            state = "⏸ Paused" if self._pause_event.is_set() else "▶️ Running"
            _send_reply(
                f"📊 <b>Status</b>\n"
                f"State: {state}\n"
                f"Seen jobs: {seen_count}\n"
                f"Last sweep: {last_run}"
            )

        elif command == "/search":
            if self._force_search_event is None:
                _send_reply("⚠️ Manual search not available.")
                return
            if self._force_search_event.is_set():
                _send_reply("🔍 A manual search is already queued — hang tight.")
                return
            self._force_search_event.set()
            _send_reply("🔍 Manual search triggered. Results coming soon...")
            print("🔍 Manual search triggered via Telegram.")

        else:
            _send_reply("Unknown command. Available: /pause, /resume, /add &lt;topic&gt;, /status, /search")


# --- Quick connectivity test ---
if __name__ == "__main__":
    test_jobs = [{
        "title": "Test Bioinformatics Script",
        "date": "Just now",
        "description": "This is a test to make sure the bot is connected.",
        "link": "https://www.upwork.com"
    }]
    send_telegram_summary(test_jobs)
