import os
import time
import random
import threading
from datetime import datetime
from upwork_scraper import run_upwork_monitor, create_search_queries, log_error
from telegram_bot import send_telegram_summary, BotController


def main():
    pause_event = threading.Event()
    bot = BotController(pause_event, topics_file="search_topics.txt")
    bot.start()

    while True:
        # Honour /pause command — check in small increments so /resume is responsive
        while pause_event.is_set():
            print("⏸ Paused. Waiting for /resume...")
            time.sleep(60)

        print("\n" + "=" * 50)
        print("🚀 STARTING NEW UPWORK SWEEP")
        print("=" * 50)

        try:
            with open("last_run.txt", "w") as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Reload topics each cycle so /add takes effect without a restart
            urls = create_search_queries("search_topics.txt")
            new_jobs = run_upwork_monitor(urls)

            if new_jobs:
                send_telegram_summary(new_jobs)

        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                raise
            print(f"\n💥 Unhandled error in main loop: {e}")
            log_error("MAIN LOOP", "N/A", str(e)[:200])

        delay_seconds = random.uniform(600 * 3, 1200 * 3)
        print(f"\n🛑 Cycle complete. Master sleep for {delay_seconds / 60:.1f} minutes...")
        time.sleep(delay_seconds)


if __name__ == "__main__":
    main()
