# Upwork Job Monitor & Telegram Alerter

Monitors Upwork searches on a schedule and sends new job summaries to a Telegram bot. Uses SeleniumBase in UC (Undetected Chrome) mode to bypass Cloudflare Turnstile.

---

## Features

- **Cloudflare bypass** via SeleniumBase UC mode
- **Deduplication** — `seen_jobs.json` tracks seen job URLs so you're never notified twice
- **Telegram bot commands** — pause, resume, add topics, and trigger manual searches at runtime
- **Docker support** — runs headless with Xvfb, state survives container restarts via bind mounts

---

## Prerequisites

- A Telegram bot token from `@BotFather`
- Your personal Telegram chat ID

For local runs: Google Chrome installed.  
For Docker: nothing extra — Chrome is bundled in the image.

---

## Setup

### 1. Clone

```bash
git clone https://github.com/uguraka/UpworkMonitor.git
cd UpworkMonitor
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
```

### 3. Add search topics

Create `search_topics.txt` with one keyword or phrase per line:

```
python
machine learning pipeline
data engineering
```

Each line becomes a separate Upwork search URL.

---

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Chrome will open a visible window (required for UC anti-detection). The script sleeps 8 hours on first startup — set `SKIP_INITIAL_SLEEP=true` to skip this during development.

---

## Running with Docker

The Docker image bundles Chrome and runs it via Xvfb (no display required on the host).

```bash
# seen_jobs.json must exist as a file before the first run
# (Docker would create it as a directory otherwise, crashing the app)
touch seen_jobs.json

docker-compose up --build
```

`seen_jobs.json` and `search_topics.txt` are bind-mounted so state and topics survive container restarts. `SKIP_INITIAL_SLEEP=true` is already set in `docker-compose.yml`.

Logs live inside the container:

```bash
docker exec <container_name> cat /app/last_run.txt
```

---

## Telegram bot commands

Commands are accepted only from the configured `CHAT_ID`.

| Command | Effect |
|---|---|
| `/status` | Reports state (running/paused), seen job count, last sweep time |
| `/pause` | Stops sweeps after the current one finishes |
| `/resume` | Restarts sweeps |
| `/search` | Triggers an immediate sweep without waiting for the next interval |
| `/add <topic>` | Appends a topic to `search_topics.txt`; takes effect next sweep |

---

## Project structure

```
UpworkMonitor/
├── main.py               # Orchestrator — schedule loop, wires modules together
├── upwork_scraper.py     # SeleniumBase scraper + deduplication
├── telegram_bot.py       # Outbound notifications + inbound command polling
├── search_topics.txt     # One search keyword/phrase per line
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
└── README.md
```

---

## License

MIT
