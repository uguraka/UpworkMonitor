Upwork Job Monitor & Telegram Alerter

A stealthy, automated job scraping pipeline built for Upwork. This tool monitors specific upwork searches and sends real-time summaries to a Telegram bot.

🚀 Features

    Anti-Bot Bypass: Utilizes SeleniumBase in UC (Undetected Chrome) mode to navigate Cloudflare Turnstile protection.

    Stealthy Behavior: Implements randomized human-like delays and user-agent spoofing to mimic real browser usage.

    State Persistence: Maintains a seen_jobs.json database to ensure you are never notified about the same job twice.

    Silent Initialization: On the first run, the script builds a baseline of existing jobs without spamming your phone.

    Telegram Integration: Delivers clean, HTML-formatted job summaries with direct links to your personal Telegram bot.

🛠️ Tech Stack

    Python 3.12+

    SeleniumBase (UC Mode): For browser automation.

    BeautifulSoup4: For fast HTML parsing.

    Requests: For Telegram API interaction.

    Git: For version control.

📋 Prerequisites

    Google Chrome: Must be installed on your system.

    Telegram Bot: Created via @BotFather.

    Chat ID: Your personal Telegram User ID (6065955283).

⚙️ Installation & Setup

    Clone the repository:
    git clone https://github.com/uguraka/UpworkMonitor.git
    cd UpworkMonitor

    Create and activate a virtual environment:
    python -m venv .venv
    source .venv/bin/activate

    Install dependencies:
    pip install seleniumbase beautifulsoup4 requests

    Configure Search Topics:
    Create search_topics.txt and add your terms (one per line).

    Configure Telegram Credentials:
    Update BOT_TOKEN and CHAT_ID in .env or telegram_bot.py.

🖥️ Usage

Run the orchestrator script:
python main.py

⚠️ Disclaimer

This project is for educational purposes. Automated scraping may violate Upwork's Terms of Service. Use responsibly.