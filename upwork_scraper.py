from seleniumbase import SB
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import os
import random

# --- Configuration ---
SEEN_JOBS_FILE = "seen_jobs.json"
NEW_JOBS_QUEUE_FILE = "new_jobs_queue.json"
ERROR_LOG_FILE = "scraper_errors.log"


def log_error(category, url, detail=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | [{category}] | {url}"
    if detail:
        line += f" | {detail}"
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"   ⚠ Logged to {ERROR_LOG_FILE}: {line}")


# --- State Management Functions ---

def load_seen_urls():
    """Loads previously seen job URLs into a set for fast lookup."""
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, 'r', encoding='utf-8') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                print("Warning: seen_jobs.json is corrupted. Starting fresh.")
                return set()
    return set()


def save_seen_urls(seen_urls):
    """Saves the updated set of URLs back to disk."""
    with open(SEEN_JOBS_FILE, 'w', encoding='utf-8') as f:
        # Convert set back to list for JSON serialization
        json.dump(list(seen_urls), f, indent=4)


def queue_new_jobs(new_jobs):
    """Appends new jobs to a queue file intended for the future Telegram sender."""
    if not new_jobs:
        return

    existing_queue = []
    if os.path.exists(NEW_JOBS_QUEUE_FILE):
        with open(NEW_JOBS_QUEUE_FILE, 'r', encoding='utf-8') as f:
            try:
                existing_queue = json.load(f)
            except json.JSONDecodeError:
                pass  # If it's empty or corrupted, we just start a new list

    # Add the newly discovered jobs to whatever is already waiting in the queue
    existing_queue.extend(new_jobs)

    with open(NEW_JOBS_QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_queue, f, indent=4, ensure_ascii=False)


# --- Extraction Function (From Previous Step) ---

def extract_job_data(html):
    """Parses Upwork HTML and returns a list of job dictionaries with dates."""
    soup = BeautifulSoup(html, 'html.parser')
    jobs = []

    job_tiles = soup.find_all('article', {'data-test': 'JobTile'})

    for tile in job_tiles:
        title_tag = tile.find('h2', class_='job-tile-title')
        if not title_tag:
            continue

        link_tag = title_tag.find('a')
        title_text = title_tag.get_text(strip=True)
        link = "https://www.upwork.com" + link_tag['href'] if link_tag else "N/A"

        date_tag = tile.find('small', {'data-test': 'job-pubilshed-date'})
        date_text = date_tag.get_text(strip=True).replace("Posted", "").strip() if date_tag else "Unknown"

        desc_container = tile.select_one('[data-test*="JobDescription"]')
        if not desc_container:
            desc_container = tile.find('p', class_='text-body-sm')

        description = desc_container.get_text(separator=' ', strip=True) if desc_container else "No description..."

        jobs.append({
            'title': title_text,
            'link': link,
            'date': date_text,
            'description': description[:300] + "..."
        })

    return jobs


# --- Main Logic ---

def run_upwork_monitor(urls):
    # 1. Load historical state
    seen_urls = load_seen_urls()
    new_jobs_found_this_run = []

    with SB(uc=True, test=True, headless=False) as sb:
        for url in urls:
            topic = url.split('q=')[-1].split('&')[0]
            print(f"\n--- Checking Search: {topic} ---")

            for attempt in range(2):
                try:
                    sb.uc_open_with_reconnect(url, reconnect_time=5)
                    sb.uc_gui_click_captcha()
                    sb.wait_for_element('article', timeout=15)
                    html = sb.get_page_source()
                    latest_jobs = extract_job_data(html)

                    for job in latest_jobs:
                        if job['link'] == "N/A":
                            continue
                        if job['link'] not in seen_urls:
                            print(f"[🌟 NEW] {job['title']}")
                            new_jobs_found_this_run.append(job)
                            seen_urls.add(job['link'])
                        else:
                            print(f"[Skipping] {job['title']} (Already seen)")

                    break

                except BaseException as e:
                    if isinstance(e, KeyboardInterrupt):
                        raise
                    err_str = str(e).lower()
                    if "captcha" in err_str or "cloudflare" in err_str:
                        category = "CAPTCHA FAIL"
                    elif "timeout" in err_str or "timed out" in err_str:
                        category = "TIMEOUT"
                    else:
                        category = "ERROR"

                    if attempt == 0:
                        retry_sleep = random.uniform(15, 30)
                        print(f"   [{category}] Attempt 1 failed: {e}. Retrying in {retry_sleep:.0f}s...")
                        time.sleep(retry_sleep)
                    else:
                        print(f"   [{category}] Attempt 2 failed: {e}. Skipping URL.")
                        log_error(category, url, str(e)[:200])

            time.sleep(random.uniform(5, 10))

    # 3. Save state and RETURN the new jobs
    if new_jobs_found_this_run:
        print(f"\n💾 Saving {len(new_jobs_found_this_run)} new jobs to seen database...")
        save_seen_urls(seen_urls)
        return new_jobs_found_this_run  # <--- Return it to main.py
    else:
        print("\n💤 No new jobs found this run.")
        return []  # <--- Return an empty list

def create_search_queries(search_topics_file: str = "search_topics.txt"):
    search_queries = []
    with open(search_topics_file, 'r', encoding='utf-8') as f:
        for line in f:
            search_topic = line.strip()
            if not search_topic:
                continue
            search_query = f"https://www.upwork.com/nx/search/jobs/?nbs=1&q={search_topic}&sort=recency"
            search_queries.append(search_query)
    return search_queries


if __name__ == "__main__":
    search_queries = create_search_queries()

    run_upwork_monitor(search_queries)