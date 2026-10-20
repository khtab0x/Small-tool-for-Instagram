# Fast Instagram Comments Cleaner Bot

A Python-based Telegram bot that automates deletion of Instagram comments from the Instagram Activity Center using Playwright. The bot provides a simple Telegram control panel so you can start/stop cleaning, adjust batch size, set your Instagram `sessionid`, and capture live screenshots of the browser.

This project is intended for managing your own Instagram account and should be used responsibly and in compliance with Instagram's terms, platform policies, and applicable laws.

## Features

- Telegram-based control panel with inline buttons
- Bulk comment deletion using a headless browser
- Adjustable batch sizes (5, 10, 15, 20, 25)
- Live screenshot support while the browser is running
- Automatic browser cleanup when operations stop
- Privacy-focused behavior: the `sessionid` message is deleted immediately after saving

## Requirements

- Python 3.8+
- Telegram Bot Token from @BotFather
- Instagram `sessionid` cookie from your authenticated browser session
- Chromium browser support via Playwright

## Repository Structure

- `app.py` — main Telegram bot and automation logic
- `requirements.txt` — project dependencies
- `start.bat` — Windows launcher that installs dependencies and starts the bot

## Installation

1. Clone the repository:

```bash
git clone https://github.com/khtab0x/Small-tool-for-Instagram.git
cd Small-tool-for-Instagram
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# or
venv\Scripts\activate      # Windows
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install the browser runtime for Playwright:

```bash
playwright install chromium
```

## Configuration

Open `app.py` and replace the placeholder token:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

with your actual Telegram bot token.

## Getting the Instagram Session ID

You need a valid Instagram `sessionid` cookie to authenticate the browser session.

Typical ways to get it:

- Open Instagram in your browser
- Open Developer Tools
- Go to Application / Storage > Cookies
- Find the `sessionid` cookie for `instagram.com`
- Copy the value and save it in the Telegram bot when prompted

Important: Treat this value as sensitive data. Never share it publicly or commit it to version control.

## Usage

Run the bot:

```bash
python app.py
```

On Telegram:

1. Start the bot with `/start`
2. Tap `Set Session ID`
3. Paste your Instagram `sessionid`
4. Tap `Start fast cleaning`
5. Optionally adjust batch size or request a live screenshot

## Behavior Notes

- The bot automates activity in a headless browser and interacts with Instagram pages in real time.
- If the `sessionid` is invalid or expired, the automation will stop and ask you to re-enter it.
- If Instagram changes its page structure or selectors, the script may need updates.

## Security and Compliance

- Use only on accounts you own or are authorized to manage.
- Never expose credentials, cookies, tokens, or screenshots in public repositories or logs.
- Respect Instagram's terms and conditions and avoid abusive or excessive automation.
- The project does not guarantee uninterrupted functionality due to changes in Instagram's web UI.

## Troubleshooting

### Browser not starting

Make sure Chromium is installed:

```bash
playwright install chromium
```

### Session ID invalid

- Regenerate the cookie in your browser
- Ensure you are logged in to the correct Instagram account
- Try again with a fresh session

### Bot not responding

- Verify that `BOT_TOKEN` is set correctly
- Ensure the bot has been started with `python app.py`
- Check terminal output for Python errors

## Windows Quick Start

If you are on Windows, you can use the bundled launcher:

```bat
start.bat
```

This script installs dependencies and launches the bot automatically.

## Disclaimer

This project is for educational and automation experimentation purposes. It is not affiliated with, endorsed by, or sponsored by Instagram or Telegram. Use it responsibly and in compliance with the applicable platform policies.
