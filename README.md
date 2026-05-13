# Upwork Job Monitor & Telegram Alerter

A stealthy, automated job scraping pipeline built for Upwork. This tool monitors specific Upwork searches and sends real-time summaries to a Telegram bot.

---

## 🚀 Features

- **Anti-Bot Bypass**  
  Utilizes `SeleniumBase` in UC (Undetected Chrome) mode to navigate Cloudflare Turnstile protection.

- **Stealthy Behavior**  
  Implements randomized human-like delays and user-agent spoofing to mimic real browser usage.

- **State Persistence**  
  Maintains a `seen_jobs.json` database to ensure you are never notified about the same job twice.

- **Silent Initialization**  
  On the first run, the script builds a baseline of existing jobs without spamming your phone.

- **Telegram Integration**  
  Delivers clean, HTML-formatted job summaries with direct links to your personal Telegram bot.

---

## 🛠️ Tech Stack

- **Python 3.12+**
- **SeleniumBase (UC Mode)** — Browser automation
- **BeautifulSoup4** — Fast HTML parsing
- **Requests** — Telegram API interaction
- **Git** — Version control

---

## 📋 Prerequisites

Before running the project, make sure you have:

- **Google Chrome** installed
- A **Telegram Bot** created via `@BotFather`
- Your personal **Telegram Chat ID**

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/uguraka/UpworkMonitor.git
cd UpworkMonitor
```

### 2. Create and activate a virtual environment

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install seleniumbase beautifulsoup4 requests
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

---

## ▶️ Usage

Run the monitor:

```bash
python main.py
```

The script will:

1. Launch a stealth browser session
2. Monitor configured Upwork searches
3. Detect newly posted jobs
4. Send Telegram alerts for unseen jobs

---

## 📁 Project Structure

```text
UpworkMonitor/
├── main.py
├── seen_jobs.json
├── requirements.txt
├── .env
└── README.md
```

---

## 🔒 Notes

- The first run initializes the local job database silently.
- Chrome must remain installed and up to date.
- Avoid aggressive polling intervals to reduce detection risk.

---

## 📜 License

This project is licensed under the MIT License.