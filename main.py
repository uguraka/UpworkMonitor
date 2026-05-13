# main.py
import time
import random
from upwork_scraper import run_upwork_monitor, create_search_queries
from telegram_bot import send_telegram_summary


def main():
    urls = create_search_queries("search_topics.txt")

    while True:
        print("\n" + "=" * 50)
        print("🚀 STARTING NEW UPWORK SWEEP")
        print("=" * 50)

        # 1. Run the scraper and catch the returned list in memory
        new_jobs = run_upwork_monitor(urls)

        # 2. If the list isn't empty, pass it to the Telegram module
        if new_jobs:
            send_telegram_summary(new_jobs)

        # 3. The Master Delay (Between full cycles)
        # Randomize between 5 and 10 minutes to stay totally under the radar
        delay_seconds = random.uniform(600, 1200)
        print(f"\n🛑 Cycle complete. Master sleep for {delay_seconds / 60:.1f} minutes...")
        time.sleep(delay_seconds)


if __name__ == "__main__":
    main()